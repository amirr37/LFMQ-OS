import matplotlib.pyplot as plt


class Processor:
    def __init__(self, process_id, request_time, service_time, priority=1):
        self.process_id = process_id
        self.request_time = request_time
        self.service_time = service_time
        self.remaining_time = service_time
        self.start_time = None
        self.response_time = None
        self.waiting_time = 0
        self.priority = priority  # Lower value indicates higher priority

    def execute(self, current_time, quantum=None):
        """
        Execute the process for either the quantum (if RR) or until completion.
        """
        if self.start_time is None:
            self.start_time = current_time
            self.response_time = current_time - self.request_time

        if quantum:
            executed_time = min(self.remaining_time, quantum)
            self.remaining_time -= executed_time
            return executed_time
        else:
            executed_time = self.remaining_time
            self.remaining_time = 0
            return executed_time

    def is_completed(self):
        """
        Check if the process has completed execution.
        """
        return self.remaining_time == 0

    def update_waiting_time(self, current_time):
        """
        Update the waiting time based on the current time.
        """
        self.waiting_time = current_time - self.request_time - (self.service_time - self.remaining_time)


def get_mlfq_config():
    # Step 1: Get the number of queues
    while True:
        try:
            num_queues = int(input("Enter the number of queues: "))
            if num_queues < 1:
                print("Number of queues must be at least 1.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # Step 2: Get the scheduling algorithm for each queue
    queue_algorithms = []
    valid_algorithms = {"RR", "FCFS", "LCFS", "PRIORITY"}
    queue_quantums = {}  # Dictionary to store quantum values for RR queues
    print(f"Valid algorithms: {', '.join(valid_algorithms)}")
    for i in range(1, num_queues + 1):
        while True:
            algo = input(f"Enter the scheduling algorithm for queue {i}: ").strip().upper()
            if algo in valid_algorithms:
                if algo == "RR":
                    while True:
                        try:
                            quantum = int(input(f"Enter the quantum for queue {i} (RR): "))
                            if quantum <= 0:
                                print("Quantum must be a positive integer.")
                                continue
                            queue_quantums[i] = quantum
                            break
                        except ValueError:
                            print("Invalid input. Please enter a positive integer.")
                queue_algorithms.append(algo)
                break
            else:
                print(f"Invalid algorithm. Please choose from: {', '.join(valid_algorithms)}")

    return num_queues, queue_algorithms, queue_quantums


def get_process_details(is_priority=False):
    while True:
        try:
            num_processes = int(input("Enter the number of processes: "))
            if num_processes < 1:
                print("Number of processes must be at least 1.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    processes = []
    print("Enter process details: request_time and service_time")
    for i in range(1, num_processes + 1):
        while True:
            try:
                if is_priority:
                    request_time, service_time, priority = map(
                        int, input(f"Process {i} (request_time service_time priority): ").split())
                    if priority < 0:
                        print("Priority must be non-negative.")
                        continue
                else:
                    request_time, service_time = map(int, input(f"Process {i} (request_time service_time): ").split())
                    priority = 1  # Default priority for non-priority algorithms

                if request_time < 0 or service_time <= 0:
                    print("Invalid values. Request time must be >= 0 and service time > 0.")
                    continue
                processes.append((request_time, service_time, priority))
                break
            except ValueError:
                print("Invalid input. Please enter integers separated by spaces.")

    return processes


def run_processor_simulation(processes, queue_algorithms, queue_quantums):
    time = 0
    ready_queue = []
    completed_processes = []
    gantt_chart = []

    for idx, algo in enumerate(queue_algorithms, 1):
        print(f"\nRunning Queue {idx} with {algo} Scheduling Algorithm...")

        while processes or ready_queue:
            # Add processes to ready queue when they arrive
            for process in sorted(processes, key=lambda p: p.request_time):
                if process.request_time <= time:
                    ready_queue.append(process)
                    processes.remove(process)

            # If ready queue is empty, increment time
            if not ready_queue:
                time += 1
                continue

            # For LCFS, pick the last process in the ready queue
            if algo == "LCFS":
                print([process.process_id for process in ready_queue])
                current_process = ready_queue.pop(-1)
            elif algo == "PRIORITY":
                # pass  # we handle current process in priority code section below
                ready_queue.sort(key=lambda p: (p.priority, p.request_time))
                # Pick the highest priority process
                current_process = ready_queue.pop(0)
            else:
                # For other algorithms, pick the first process in the ready queue
                current_process = ready_queue.pop(0)

            # Update waiting time for the process
            current_process.update_waiting_time(time)

            if algo == "RR":
                quantum = queue_quantums.get(idx, 4)  # Default to 4 if quantum isn't provided

                # If this is the first time the process starts, calculate response time
                if current_process.start_time is None:
                    current_process.start_time = time
                    current_process.response_time = time - current_process.request_time

                # Execute the process for either the quantum or the remaining time
                executed_time = min(quantum, current_process.remaining_time)
                start_time = time
                current_process.remaining_time -= executed_time
                time += executed_time  # Advance the time

                # Add any newly arriving processes to the ready queue
                for process in list(processes):
                    if process.request_time <= time:
                        ready_queue.append(process)
                        processes.remove(process)

                # Record execution interval for Gantt chart
                gantt_chart.append((current_process.process_id, start_time, time))

                # If the process is incomplete, re-add it to the ready queue
                if current_process.remaining_time > 0:
                    ready_queue.append(current_process)
                else:
                    completed_processes.append(current_process)

                # Update waiting time for other processes in the ready queue
                for process in ready_queue:
                    process.waiting_time += executed_time

            elif algo == "FCFS":
                # Record start time for Gantt chart
                start_time = time

                print(f" start running : {current_process.process_id} - time={time}")
                executed_time = current_process.execute(time)
                time += executed_time
                completed_processes.append(current_process)
                print(f" end running : {current_process.process_id} - time={time}")

                # Record execution interval for Gantt chart
                gantt_chart.append((current_process.process_id, start_time, time))

            elif algo == "LCFS":
                # Record start time for Gantt chart
                start_time = time

                print(f" start running : {current_process.process_id} - time={time}")
                executed_time = current_process.execute(time)
                time += executed_time
                completed_processes.append(current_process)
                print(f" end running : {current_process.process_id} - time={time}")

                # Record execution interval for Gantt chart
                gantt_chart.append((current_process.process_id, start_time, time))


            elif algo == "PRIORITY":
                # Sort by priority (ascending) and then by request_time (ascending) to break ties
                # ready_queue.sort(key=lambda p: (p.priority, p.request_time))
                # # Pick the highest priority process
                # current_process = ready_queue.pop(0)

                # Record start time for Gantt chart
                start_time = time
                executed_time = current_process.execute(time)
                time += executed_time
                completed_processes.append(current_process)
                # Record execution interval for Gantt chart
                gantt_chart.append((current_process.process_id, start_time, time))
                print(f"{current_process.process_id}-------------------")

    # Display process summary
    print("\nProcess Execution Summary:")
    for process in completed_processes:
        print(
            f"Process {process.process_id}: "
            f"Request Time = {process.request_time}, "
            f"Service Time = {process.service_time}, "
            f"Response Time = {process.response_time}, "
            f"Waiting Time = {process.waiting_time}, "
            f"Recursion Time = {process.service_time + process.waiting_time}"
        )

    # Generate Gantt chart
    generate_gantt_chart(gantt_chart)


def generate_gantt_chart(gantt_data):
    """
    Generate a Gantt chart based on the recorded execution intervals.
    :param gantt_data: List of tuples (process_id, start_time, end_time)
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # Generate bars for each process
    for process_id, start_time, end_time in gantt_data:
        ax.broken_barh([(start_time, end_time - start_time)], (process_id * 10, 8),
                       facecolors=('tab:blue'))

    # Labeling and formatting
    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_yticks([p * 10 + 4 for p, _, _ in gantt_data])
    ax.set_yticklabels([f"P{p}" for p, _, _ in gantt_data])
    ax.grid(True)

    plt.title("Gantt Chart")
    plt.show()


if __name__ == "__main__":
    num_queues, queue_algorithms, queue_quantums = get_mlfq_config()
    print(f"\nConfiguration Summary:")
    print(f"Number of Queues: {num_queues}")
    for idx, algo in enumerate(queue_algorithms, 1):
        if algo == "RR":
            print(f"Queue {idx}: {algo} (Quantum = {queue_quantums[idx]})")
        else:
            print(f"Queue {idx}: {algo}")

    is_priority = "PRIORITY" in queue_algorithms
    process_details = get_process_details(is_priority=is_priority)
    processes = [Processor(i + 1, req, serv, prio) for i, (req, serv, prio) in enumerate(process_details)]

    # Run simulation
    run_processor_simulation(processes[:], queue_algorithms, queue_quantums)
