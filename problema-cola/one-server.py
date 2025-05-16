from scipy.stats import expon
import csv
import sys

arrival_times = []
queuing_exit_times = []
consult_exit_times = []
change_points = []
queue_length_tracker = [] #indexed to change_points list
max_time = 480
arrival_time_mean = 12
queuing_time_mean = 5
consult_time_mean = 20
sim_name = sys.argv[1]

def crit_point_calc():
    start_time = 0
    while True:
        arrival_time = expon.rvs(loc = 0, scale = arrival_time_mean, size = 1) 
        #print(arrival_time)
        start_time += arrival_time
        #print(start_time)

        if start_time >= max_time:
            break
        
        if len(arrival_times) == 0:
            arrival_times.append(arrival_time)
        else:
            arrival_times.append(arrival_times[-1] + arrival_time)
        #print (arrival_times)

    #print(arrival_times)

    for id, time in enumerate(arrival_times):
        queuing_time = expon.rvs(loc = 0, scale = queuing_time_mean, size = 1) 
        consult_time = expon.rvs(loc = 0, scale = consult_time_mean, size = 1)

        if id == 0 or time > consult_exit_times[id - 1] or time > queuing_exit_times[id - 1] and time + queuing_time > consult_exit_times[id - 1]:
            queuing_exit_times.append(time + queuing_time)
            consult_exit_times.append(queuing_exit_times[id] + consult_time)
        elif time > queuing_exit_times[id - 1]:
            queuing_exit_times.append(time + queuing_time)
            consult_exit_times.append(consult_exit_times[id - 1] + consult_time)
        else:
            queuing_exit_times.append(queuing_exit_times[id - 1] + queuing_time)
            consult_exit_times.append(consult_exit_times[id - 1] + consult_time)

    #print(queuing_exit_times)
    #print(consult_exit_times)

def plot_system():
    i = 0
    
    while i < len(arrival_times):
        if arrival_times[i] == consult_exit_times[i]:
            change_points.append(arrival_times[i])
        else:
            change_points.append(arrival_times[i])
            change_points.append(consult_exit_times[i])
        
        i += 1
   
    change_points.sort()
    
    #print(change_points)

    for id, time in enumerate(change_points):
        if id == 0:
            queue_length_tracker.append(1)
        elif arrival_times.count(time) > 0 and queuing_exit_times.count(time) > 0:
            queue_length_tracker.append(queue_length_tracker[id - 1])
        elif arrival_times.count(time) > 0:
            queue_length_tracker.append(queue_length_tracker[id - 1] + 1)
        else:
            queue_length_tracker.append(queue_length_tracker[id - 1] - 1)

def data_write():
    with open(sim_name + '_inflection_points.csv', 'w') as f:
        datawriter = csv.writer(f, delimiter = ',')

        datawriter.writerow(['arrival times', 'queuing exit times', 'consult exit times'])

        i = 0
        while i < len(arrival_times):
            datawriter.writerow([arrival_times[i], queuing_exit_times[i], consult_exit_times[i]])
            i += 1

    with open(sim_name + '_queue_length_OT.csv', 'w') as f:
        datawriter = csv.writer(f, delimiter = ',')

        datawriter.writerow(['time', 'queue length'])

        i = 0
        while i < len(change_points):
            datawriter.writerow([change_points [i], queue_length_tracker[i]])
            i += 1

def main():
    crit_point_calc()
    plot_system()
    data_write()

if __name__=="__main__":
    main()


