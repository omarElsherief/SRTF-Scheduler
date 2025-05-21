class Process:
    def __init__(self,id,arrival_time,burst_time):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.termination_time = 0
        self.start_time = -1

    def turnaround_time(self):
        return self.termination_time - self.arrival_time 
    def waiting_time(self):
        return self.termination_time-(self.arrival_time + self.burst_time)
    def response_time(self):
        return self.start_time - self.arrival_time


























# process attribuets id,Arrival Time and Burst Time
# funcs get Average Waiting, Turnaround, and Response Times. get id get Arrival Time and Burst Time