# Implemetation-of-Interval-Partitioning-Algorithm

## Overview
This program randomly generates 1000 lectures to be managed into several classrooms.
The aim is to find the minimun number of the classrooms and arrange all the lectures
efficiently. Suppose the time range of every lecture is from 9:00 to 18:00, then there
are 18 time slots.

After all lectures are generated, this program will arrange all the lectures into several classrooms using greedy algorithm and output the result to a csv file. In the end, the csv file will be drawn as heatmap using pandas and matplotlib.

![figure1](https://github.com/Evian-Chen/Implemetation-of-Interval-Partitioning-Algorithm/blob/main/Figure_1.png)

## Analysis
In greedy algorithm, the main loop iterates through all the lectures once. Within each iteration, it performs the following operations:
     
     - Checking if the priority queue is empty: O(1)
     
     - Appending a new room and lecture to the schedule: O(1)
     
     - Appending a new element to the priority queue: O(log R), where R is the number of rooms in the priority queue
     
     - Removing the smallest element from the priority queue: O(log R)
     
     - Sorting the priority queue: O(R log R) (Python built-in sort takes O(N log N) on average)
     
     - The overall time complexity of the main loop is O(N log R), where N is the number of lectures and R is the number of rooms.


The total time complexity is O(N log N + N log R). Usually, we take the biggest coefficient. Hence, the time complexity of this greedy algorithm is O(N log N).
