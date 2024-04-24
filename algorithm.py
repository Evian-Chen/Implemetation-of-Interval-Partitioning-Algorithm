"""
This program randomly generates 1000 lectures to be managed into several classrooms.
The aim is to find the minimun number of the classrooms and arrange all the lectures
efficiently. Suppose the time range of every lecture is from 9:00 to 18:00, then there
are 18 time slots.
"""

import random, csv
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

FILE = "lectures.txt"
NEWFILE = "manyLectures.txt"
DATANUM = 1000

# turn time into indexes
# 9:00 -> 1, 9:30 -> 2, 10:00 -> 3,... etc. 
def indexing(data):
    time = data.split(':')
    start = (int(time[0])-9) * 2
    start += 1 if int(time[1][0]) == 3 else 0
    finish = (int(time[1].split('-')[1])-9) * 2
    finish += 1 if int(time[2][0]) == 3 else 0
    return (start, finish)

# this funciton should generate DATANUM lectures and time and write them into a txt
def randomDataGenerator():                  
    with open(NEWFILE, 'w') as f:
        for i in range(DATANUM):
            start = random.randrange(0, 17)
            finish = random.randrange(1, 18)
            while finish <= start:
                finish = random.randrange(0, 18)
            startstr = f"09:{start%2*3}0" if start <= 2 else f"{start//2+9}:{start%2*3}0"
            finishstr = f"09:{finish%2*3}0" if finish <= 2 else f"{finish//2+9}:{finish%2*3}0"
            s = f"Lecture {i}:   {startstr}-{finishstr}\n"
            f.write(s)


#=============== file reading ===============#

randomDataGenerator()

lectures = dict()                           # {lecture: (s, f), lecture: (s, f), ...}
with open(NEWFILE, 'r') as file:
    for line in file:
        data = line.split()
        s, f = indexing(data[2])
        lectures[data[1][:-1]] = (s, f)

# sort lectures based on the starting time of each lecture
lectures = dict(sorted(lectures.items(), key=lambda item: item[1][0]))


#=============== greedy algorithm ===============#

priority = list()                              
schedule = defaultdict(list)                   # {room1: [lectures], room2: [lectures],...}
room = 0                                       # room is depth

start = time.time()                            # start time stamp

for lecture, timeInterval in lectures.items():         # greedy algorithm
    if not priority:                           # for the first data
        schedule[room].append(lecture)         # add lecture to the schedule
        priority.append((timeInterval[1], room))       # add finish time of the lecture and the toom to priority queue
    else:
        if timeInterval[0] < priority[0][0]:           # there's no avalible classroom
            room += 1                          # create a new room
            schedule[room].append(lecture)
            priority.append((timeInterval[1], room))   # update priority queue
        else:
            room_inedx = priority[0][1]
            schedule[room_inedx].append(lecture)
            priority.append((timeInterval[1], room_inedx))
            priority = priority[1:]
        priority.sort()                        # put the smallest finish time at first

end = time.time()                              # end time stamp

print(f"This algorithm takes {end-start} secs for arranging {DATANUM} lectures.")


#=============== make csv ===============#

filenames = ["classroom"]                                 # field names for csv
for i in range(9, 18):
    timeSplice1 = f"09:00" if i < 10 else f"{i}:00"
    timeSplice2 = f"09:30" if i < 10 else f"{i}:30"
    filenames.extend([timeSplice1, timeSplice2])

with open("data.csv", "w", newline='') as csvfile:        # write schedule into csv format
    fieldname = filenames
    writer = csv.DictWriter(csvfile, fieldnames=fieldname)
    writer.writeheader()
    for room, l in schedule.items():                      # make a dict for each classroom
        ongoingLecture = {"classroom": f"room {room+1}"}
        for lectureName in l:
            start, finish = lectures[lectureName]
            for j in range(start, finish+1):
                field = f"09:{j%2*3}0" if j <= 1 else f"{j//2+9}:{j%2*3}0"
                ongoingLecture[field] = int(lectureName)  # add lecture to the corresponding classroom 
        writer.writerow(ongoingLecture)


#=============== plot heatmap ===============#

df_csv = pd.read_csv("data.csv", index_col=0)
print(df_csv)                                             # show schedule on terminal

# Transpose the dataframe to have time slots as rows and classrooms as columns
df = df_csv.T

# Calculate the suitable font size
num_rows, num_cols = df.shape
max_font_size = min(200 // max(num_rows, num_cols), 12)  # Limit maximum font size to 12

# Plotting
plt.figure(figsize=(12, 6))

# Plot a heatmap
sns.heatmap(df, cmap='viridis', annot=True, cbar=False, annot_kws={"size": max_font_size})

# Add labels
plt.title('Classroom Schedule')
plt.xlabel('Classroom')
plt.ylabel('Time Slot')

# Show the plot
plt.tight_layout()
plt.show()