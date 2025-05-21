from process import Process







# to validate the input numbers 
def validate_int(val):
    try:
        x = int(val)
        if x >= 0:
            return x  
        else:
            print("Error: The number must be non-negative.")
            return None
    except ValueError:
        print("Error: Invalid input. Please enter a valid non-negative integer.")
        return None







# return the shortest remaining process to use in the algo
def get_shortest_remaining_process(process_list, current_time):
    ready_processes = []

    for process in process_list:
        if process.arrival_time <= current_time and process.remaining_time > 0:
            ready_processes.append(process)

    if len(ready_processes) == 0:
        return None

    shortest = ready_processes[0]
    for process in ready_processes:
        if process.remaining_time < shortest.remaining_time:
            shortest = process

    return shortest





# exec the algo nad return the gant chart contain the process over every second (pid,start,end_time)
def srtf(process_list):
    time =0
    processes_completed =0
    number_of_processes =len(process_list)
    gant =[]

    while processes_completed<number_of_processes:
        ready_queue =[]

        for process in process_list:
            if process.arrival_time <= time:
                ready_queue.append(process)
        if ready_queue==[]:
            gant.append(("idle",time,time+1))
            time+=1
            continue
        else:
            process = get_shortest_remaining_process(ready_queue,time)
            
            if process.start_time == -1:
                process.start_time =time
            
            process.remaining_time -=1
            gant.append((process.id,time,time+1))
            
            if process.remaining_time == 0:
                process.termination_time=time+1
                processes_completed+=1
                
        time+=1
    return gant







# return processes that user entered process[id,AT,BT]
def processes_input_from_user():
    processes=[]
    NP=int(input("Enter number of processes : "))
    for i in range(1,NP+1):
        while True:
            AT = validate_int(input(f"Enter the arrival time of process {i}: "))
            if AT is not None:
                break 
        
        while True:
            BT = validate_int(input(f"Enter the burst time for process {i}: "))
            if BT is not None:
                break  
        processes.append(Process(f"P{i}", AT, BT))
    return processes









# return avgs[avg WT,avg TT, avg RT]
def avgs(processes):
    sum_waiting_time=0
    sum_turnaround_time=0
    sum_response_time=0
    lenth =0
    avgs=[]
    for proc in processes:
        sum_waiting_time+=proc.waiting_time()
        sum_response_time+=proc.response_time()
        sum_turnaround_time+=proc.turnaround_time()
        lenth +=1
    avgs.append(sum_waiting_time/lenth)
    avgs.append(sum_turnaround_time/lenth)
    avgs.append(sum_response_time/lenth)
    return avgs








# for testing
def test_srtf(process_list):
    # process_list[id, arrival_time, burst_time]
    
    gantt_chart = srtf(process_list) 
    print("Gantt Chart: ", gantt_chart)

    for process in process_list:
        print(f"Process {process.id}:")
        print(f"- Turnaround Time: {process.turnaround_time()}")
        print(f"- Waiting Time: {process.waiting_time()}")
        print(f"- Response Time: {process.response_time()}")
    print("-------------------------------------------\n")
    avg_values=avgs(process_list)
    print(f"avg waitnig time ={avg_values[0]}")
    print(f"avg turnaround time ={avg_values[1]}")
    print(f"avg response time ={avg_values[2]}")









# filter gant data (pid,start,end_time)
def filter_gant(gant_data):
    new_gant=[]
    prev_id,st,end=gant_data[0]
    for i in range(1,len(gant_data)):
        cur_id,cur_st,cur_en=gant_data[i]
        if cur_id==prev_id and end==cur_st:
            end=cur_en
        else:
            new_gant.append((prev_id,st,end))
            prev_id = cur_id
            st=cur_st
            end=cur_en
    new_gant.append((prev_id, st, end))
    return new_gant
        