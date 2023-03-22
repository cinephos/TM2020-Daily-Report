#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 15:42:53 2023

@author: cinephos
"""

import os
import csv
import time
import TrackmaniaAPI
import Defynitions
import Utils




# This is the Autosaves_file

Autosaves_file = Defynitions.working_dir + '/' + Defynitions.autosaves

# This is the My_maps_txt.file

maps_file = Defynitions.working_dir + '/' + Defynitions.my_maps

# Open the autosaves file and transfer data to a list

file = open(Autosaves_file, "r")
autosaves_data = list(csv.reader(file))
file.close()

# if my_maps file doesn't exist, then create an empty list with header. Else, load the file to a list.

if not (os.path.isfile(maps_file)):
    print("Maps local file doesn't exist. I have created it.")
    my_maps_data =[]
    my_maps_header = ['Map_id', 'exists', 'Map_name', 'Map_name_stripped', 'a_time', 'g_time', 's_time', 'b_time']
    my_maps_data.append(my_maps_header)
else:
    file = open(maps_file, "r")
    my_maps_data = list(csv.reader(file))
    file.close()

# The following lines create a new entry in the maps list for every autosaves data list entry 
# on a map not played before.
# Column 'exists' = 'False' indicates that there are no data in local map file.

for i in range(len(autosaves_data)-1):
    if not any(autosaves_data[i+1][1] in (match := nested_list) for nested_list in my_maps_data):    
        my_maps_line = [autosaves_data[i+1][1], 'False', ' ', ' ', 0, 0, 0, 0]
        my_maps_data.append(my_maps_line)

# The map list is transferred to the local file.

file = open(maps_file, 'w', newline='')
csvwrite = csv.writer(file,lineterminator=os.linesep)
csvwrite.writerows(my_maps_data)
file.close()

# Create a list with all map uid in map list for which data do not exist in local map file.
# Condition column 'exists' == 'False'


maps_false = []
for i in range(len(my_maps_data)):
    if my_maps_data[i][1] == "False":
        maps_false.append(my_maps_data[i][0])
        
# create object to work with TrackmaniaAPI

api = TrackmaniaAPI.TmApi()

# get_ticket_levet_2 return level_2 ticket

api.get_ticket_level_2()

# This is the argument list of the API request

argstring = []

# the following line constructs string members of the argument list with a maximum
# of 100 map uids each,

for i in range(0,len(maps_false),100):
    argstring.append(','.join(maps_false[j] for j in range(i, min(i + 100, len(maps_false)))))

# the following line executes the API request and stores the json object returned 

for i in range(len(argstring)):
    result = api.get_maps_info(argstring[i]).get('mapList')
    
# It is necassary to sleep 2 seconds between API requests to avoid flood NADEO server with requests
    
    time.sleep(2)
    
# The following line stores data received to the maps list
    
    for j in range(len(result)):
        my_maps_data = Utils.write_maps_data(j, result, my_maps_data)
        
#The following line writes the map list data to the map file.
        
Utils.write_csv_file(maps_file,my_maps_data)        
    
