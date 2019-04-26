# STIME          TIME             UID   PID D    BLOCK   SIZE       COMM PATHNAME

import os
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
from collections import defaultdict

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

# TODO:
def draw_histogram():
    return


if __name__=="__main__":
    draw_CDF()
    draw_histogram()
    
    '''
    files_number = len(files_size)
    files_size_sum = 0
    for key in files_size:
        files_size_sum =  files_size_sum + files_size[key]
    #print (list(files_size.keys()))
    #print (np.array(list(files_size.values()))[:,0])  
    plt.bar(np.array(list(files_size.keys())), np.array(list(files_size.values()))[:,0])
    plt.xlabel('file_name')
    plt.ylable('access number')
    plt.show()
    '''
