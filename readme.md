# Multi-Level Feedback Queue (MLFQ) Scheduler Simulation
This project simulates the Multi-Level Feedback Queue (MLFQ) scheduling algorithm, supporting multiple scheduling policies, including RR (Round Robin), FCFS (First-Come-First-Serve), LCFS (Last-Come-First-Serve), and Priority Scheduling. The scheduler allows users to define the number of queues, their scheduling algorithms, and process details.

## Features
 -  Supports Round Robin (RR), First-Come-First-Serve (FCFS), Last-Come-First-Serve (LCFS), and Priority Scheduling.
 - Allows custom quantum values for RR queues.
 - Supports dynamic process arrival times and execution.
 - Visual representation of the execution through a Gantt Chart.
 - Calculates process metrics like response time, waiting time, and turnaround time.

## Requirements
 - Python 3.7+
 - Libraries: matplotlib

Install the required library using:

```bash
pip install matplotlib
```


## How It Works

### Step 1: Configure the MLFQ
The user provides:

1. The number of queues.
2. The scheduling algorithm for each queue (e.g., RR, FCFS, LCFS, or Priority). For RR, a quantum value is required.

### Step 2: Define Processes

The user enters:

1. The number of processes.
2. Each process's request time (arrival time), service time (execution duration), and priority (if Priority Scheduling is used).


### Step 3: Simulation
The scheduler simulates the execution of processes based on their arrival times and the selected scheduling algorithms.

### Step 4: Gantt Chart
A Gantt chart is displayed to visualize process execution timelines.


## How to Run

Clone this repository:

```bash
Copy code
git clone <repository_url>
cd <repository_directory>
```

Run the script:

```bash

Copy code
python main.py
```
