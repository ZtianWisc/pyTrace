import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
from collections import defaultdict
from zplot import *

# directory = os.fsencode('google.map.traces')
THOUSAND = 1000

'''
Read a file, and load start time, end time, browser name, 
and number of bytes accessed into data structures.
'''
def load_file(file_name: str, start_time: List[int], end_time: List[int], accessed_sizes):
    with open(file_name) as fp:
        browser_name = None
        base_time = 0
        line = fp.readline()
        while line:
            line = fp.readline()
            if len(line) < 2:
                break
            (stime, etime, UID, PID, D, BLOCK, SIZE, COMM, PATHNAME) = line.split()
            stime = int(stime)
            etime = int(etime)
            if not base_time:
                base_time = stime
            if not browser_name:
                browser_name = COMM
            accessed_time = (stime - base_time) // THOUSAND
            accessed_sizes[accessed_time] += int(SIZE)
            start_time.append(int(stime))
            end_time.append(int(etime))
    for i in range(len(start_time)):
        start_time[i] = (start_time[i] - base_time) // THOUSAND
        end_time[i] = (end_time[i] - base_time) // THOUSAND
    return browser_name

'''
Draw cumulative distribution function
'''
def draw_CDF():
    file_names = [
        "chrome.bingmaps.log", 
        "safari.bingmaps.log", 
        "firefox.bingmaps.log",
        "chrome.googlemaps.log", 
        "safari.googlemaps.log", 
        "firefox.googlemaps.log"]
    browser_s = []
    accessed_sizes_s = []
    start_time_s = []
    end_time_s = []
    for i in range(len(file_names)):
        file_names[i] = "./traces/" + file_names[i]

    for file_name in file_names:
        browser = None
        accessed_sizes = defaultdict(int)
        start_time = []
        end_time = []
        browser = load_file(file_name, start_time, end_time, accessed_sizes)
        browser_s.append(browser)
        accessed_sizes_s.append(accessed_sizes)
        start_time_s.append(start_time)
        end_time_s.append(end_time)
    assert(len(browser_s)
           == len(accessed_sizes_s)
           == len(start_time_s)
           == len(end_time_s)
           == len(file_names))

    total_time = 0
    for end_times in end_time_s:
        total_time = max(end_times[-1], total_time)
    X_axis = [i for i in range(total_time)]
    for i in range(len(file_names)):
        browser = browser_s[i] # browser name, for labeling
        accessed_sizes = accessed_sizes_s[i]
        start_time = start_time_s[i]
        end_time = end_time_s[i]
        Y_axis = [0 for j in range(total_time)]   
        for time in accessed_sizes.keys():
            Y_axis[time] = accessed_sizes[time]
        # aggregate
        for j in range(1, len(Y_axis)):
            Y_axis[j] = Y_axis[j] + Y_axis[j-1]
        plt.plot(X_axis, Y_axis, label=file_names[i][9:])
    plt.xlabel('Time (ms)')
    plt.ylabel('CDF (bytes)')
    plt.legend()
    plt.show()
    return

# draw_histogram
def load_files_size(file_name: str, read_files, write_files):
    browser = None
    with open(file_name) as fp:
        line = fp.readline()
        while(line):
            line = fp.readline()
            if len(line) < 2:
                break
            (stime, etime, UID, PID, D, BLOCK, SIZE, COMM, PATHNAME) = line.split()
            if browser == None:
                browser = COMM
            if D == "W":
                write_files[PATHNAME].append(float(SIZE))  # access number  acess size
            elif D == "R":
                read_files[PATHNAME].append(float(SIZE))
    return browser

def draw_histogram():
    file_names = [
        "chrome.bingmaps.log", 
        "safari.bingmaps.log", 
        "firefox.bingmaps.log",
        "chrome.googlemaps.log", 
        "safari.googlemaps.log", 
        "firefox.googlemaps.log"]
    for i in range(len(file_names)):
        file_names[i] = "./traces/" + file_names[i]
    #read_files_size_s = []
    #write_files_size_s = []
    #browser_s = []

    for file_name in file_names:
        read_files = defaultdict(list)
        write_files = defaultdict(list)
        browser = load_files_size(file_name, read_files, write_files)
        #read_files_size_s.append(read_files_size)
        #write_files_size_s.append(write_files_size)
        #browser_s.append(browser)
        read_files_number = defaultdict(list)
        read_files_size = defaultdict(list)
        for k, v in read_files.items():
            read_files_number[k] = len(v)
            read_files_size[k] = sum(v)
        
        write_files_number = defaultdict(list)
        write_files_size = defaultdict(list)
        for k, v in write_files.items():
            write_files_number[k] = len(v)
            write_files_size[k] = sum(v)

        plt.bar(np.array(list(read_files_size.keys())), np.array(list(read_files_number.values())), width=0.1, alpha = 0.8)
        plt.xticks(size = 'small', rotation = 60)
        plt.title(file_name + '(read file size)')
        plt.xlabel('file_name')
        plt.ylabel('access number')
        plt.show()
    
    # plot 
    #for file_name in file_names:




# draw interval
def load_files_interval(file_name):
    max_time = 0
    min_time = sys.maxsize
    interval_file = open(file_name[9:] + '_horizontalintervals.data', 'w+')
    interval_file.write("# nodes min max\n")
    browser = None
    base_time = 0
    files_interval = defaultdict(list)
    with open(file_name) as fp:
        line = fp.readline()
        while(line):
            line = fp.readline()
            if len(line) < 2:
                break
            (stime, etime, UID, PID, D, BLOCK, SIZE, COMM, PATHNAME) = line.split()
            stime = int(stime)
            etime = int(etime)
            if not base_time:
                base_time = stime
            stime = (stime - base_time) // THOUSAND
            etime = (etime - base_time) //THOUSAND
            if browser == None:
                browser = COMM
            if(stime < min_time):
                min_time = stime
            if(etime > max_time):
                max_time = etime
            files_interval[PATHNAME].append((stime, etime))
            #print (len(files_interval[PATHNAME]))
            #interval_file.write(PATHNAME + " ")
            #interval_file.write(str(stime) + " ")
            #interval_file.write(str(etime) + "\n")
    i = 0
    for key in files_interval:
        i += 1
        itvs = len(files_interval[key])
        #print (itvs)
        for j in range(itvs):
            #print (files_interval[key][j][0])
            interval_file.write(str(i) + " ")
            interval_file.write(str(files_interval[key][j][0]) + " ")
            interval_file.write(str(files_interval[key][j][1]) + "\n")

    return (min_time, max_time)
    
def draw_interval():
    file_names = [
        "chrome.bingmaps.log", 
        "safari.bingmaps.log", 
        "firefox.bingmaps.log",
        "chrome.googlemaps.log", 
        "safari.googlemaps.log", 
        "firefox.googlemaps.log"]
    for i in range(len(file_names)):
        file_names[i] = "./traces/" + file_names[i]
    
    for file_name in file_names:
        max_time = 0
        min_time = sys.maxsize
        (min_tmp, max_tmp) = load_files_interval(file_name)
        if(min_tmp < min_time): 
            min_time = min_tmp
        if(max_tmp > max_time):
            max_time = max_tmp
        print(file_name[9:] + '_horizontalintervals.data')
        t = table(file_name[9:] + '_horizontalintervals.data')
        for i in range(len(file_name)):
            if file_name[i] == '.':
                file_name = file_name[:i] + '_' + file_name[i+1:] 
        canvas = postscript(file_name[9:] + 'horizontalintervals.eps')
        print (t.getmax('nodes'))
        d = drawable(canvas, coord=[20, 20], xrange=[min_time, max_time],
                    yrange=[0, t.getmax('nodes')])
        axis(d, xtitle='Time (ms)', xauto=[min_time, max_time, 10000],
            ytitle='Nodes', yauto=[0, t.getmax('nodes'), t.getmax('nodes')//10])

        # ylofield and yhifield specify the interval range
        p = plotter()
        p.horizontalintervals(d, t, yfield='nodes', xlofield='min', xhifield='max')

        canvas.render()
    
if __name__=="__main__":
    #draw_CDF()
    #draw_histogram()
    draw_interval()
 
