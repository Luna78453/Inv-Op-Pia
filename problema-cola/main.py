from scipy.stats import expon
import csv

queue_length_tracker = []
arrival_times = []
queuing_exit_times = []
consult_exit_times = []
change_points = []
system_lengths = [] #indexed to change_points list
max_time = 480
arrival_time_mean = 12
queuing_time_mean = 5
consult_time_mean = 20
sim_name = ''

def crit_point_calc():
    start_time = 0
    while True:
        arrival_time = expon.rvs(loc = 0, scale = arrival_time_mean, size = 1) 
        start_time += arrival_time

        if start_time >= max_time:
            break

        arrival_times.append(start_time)

    for time in arrival_times:
        i = 0
        queuing_time = expon.rvs(loc = 0, scale = queuing_time_mean, size = 1) 
        consult_time = expon.rvs(loc = 0, scale = consult_time_mean, size = 1)

        if time == 0:
            continue
        elif i == 0:
            queuing_exit_times.append(time + queuing_time)
            consult_exit_times.append(queuing_exit_times[arrival_times.index(time)] + consult_time)
            i = 1
        elif time > consult_exit_times[arrival_times.index(time) - 1]:
            queuing_exit_times.append(time + queuing_time)
            consult_exit_times.append(queuing_exit_times[arrival_times.index(time)] + consult_time)
        elif time > queuing_exit_times[time.index() - 1]:
            queuing_exit_times.append(queuing_exit_times[arrival_times.index(time) - 1] + queuing_time)
            consult_exit_times.append(consult_exit_times[arrival_times.index(time)] + consult_time)
        else:
            queuing_exit_times.append(queuing_exit_times[arrival_times.index(time) - 1] + queuing_time)
            consult_exit_times.append(consult_exit_times[arrival_times.index(time) - 1] + consult_time)

def plot_system():
    i = 0
    
    while i < len(arrival_times):
        if arrival_times[i] == consult_exit_times[i]:
            change_points.append(arrival_times[i])
        else:
            change_points.append(arrival_times[i])
            change_points.append(consult_exit_times[i])

    for time in change_points:
        if time.index() == 0:
            system_lengths.append(1)
        elif arrival_times.count(time) == consult_exit_times.count(time):
            system_lengths.append(system_lengths[change_points.index(time) - 1])
        elif arrival_times.count(time) == 1:
            system_lengths.append(system_lengths[change_points.index(time) - 1] + 1)
        else:
            system_lengths.append(system_lengths[change_points.index(time) - 1] - 1)

def data_write():
    with open(sim_name + 'inflection_points.csv', 'w') as f:
        datawriter = csv.writer(f, delimiter = ',')

        datawriter.writerow(['arrival times', 'queuing exit times', 'consult exit times'])

        i = 0
        while i < len(arrival_times):
            datawriter.writerow([arrival_times[i], queuing_exit_times[i], consult_exit_times[i]])
            i += 1

    with open(sim_name + 'queue_length_OT.csv', 'w') as f:
        datawriter = csv.writer(f, delimiter = ',')

        datawriter.writerow(['time', 'queue length'])

        i = 0
        while i < len(change_points):
            datawriter.writerow([change_points [i], queue_length_tracker[i]])

def main():
    crit_point_calc()
    plot_system()
    data_write()

if __name__=="__main__":
    main()


