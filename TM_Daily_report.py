#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 11:13:58 2023

@author: cinephos
"""

import csv
import datetime
import os

import Defynitions
import Utils


# This is the Autosaves_file

Autosaves_file = Defynitions.working_dir + '/' + Defynitions.autosaves

# This is the My_maps_txt.file

maps_file = Defynitions.working_dir + '/' + Defynitions.my_maps

# This is the My_Pbs text.file

my_PBs_file = Defynitions.working_dir + '/' + Defynitions.my_PBs


# If there is a new Autosaves file in the directory, the Cheeckpoint_2 and
# Checkpoint_3 functions must be run.

if (os.path.isfile(Autosaves_file)):    
    Utils.CheckPoint_2()
    Utils.CheckPoint_3()

# Open the local PBs file and move all data to a list.

file = open(my_PBs_file, "r")
temp_data = list(csv.reader(file))

# Strip the header line.

my_PBs = temp_data[1:len(temp_data)][:]

# Close the local PBs file.

file.close()

# Open the local maps file and move all data to a list

file = open(maps_file, "r")
temp_data = list(csv.reader(file))

# Strip the header line.

my_maps_data = temp_data[1:len(temp_data)][:]

# Close the local maps file.

file.close()

# Determine the current date and time in seconds.

now_date = datetime.datetime.now()
now_seconds = int(now_date.timestamp())

# Determne the date and time exactly 24 hours ago.

yesterday_seconds = now_seconds - 86400
yesterday_date = datetime.datetime.fromtimestamp(yesterday_seconds)

# Create a list with all new PBs recorder in the past 24 hours

PBs_24h = []
for i in range(len(my_PBs)):
     if int(my_PBs[i][0]) > yesterday_seconds:
         PBs_24h.append(my_PBs[i])

# Inform user if no PBs were found in the last 24 hours.

if len(PBs_24h) == 0:
    print("No new PBs in the last 24h")
else:
    for i in range(len(PBs_24h)):

# Print map details and PBs of the records found.
        
        mapID = PBs_24h[i][1]
        Utils.print_map_details(mapID, my_maps_data, my_PBs)

# Ask the user if he wants more data from stored PBs. Only 'Y' and 'y' are valid replies.
    
print(' ')
print('Type \'Y\' or \'y\' if you wish to print more PBs: ', end = '')  
x = input()

# The while loop is revisited each time the user inputs 'Y' or 'y'

while (x == 'Y' or x == 'y'):
    
# Input of a string contained in the name of the file (after manialib format is stripped)
    
    print('Type a string contained in map name(s): ', end = '' )
    y = input()
    
# Set an empty list for the found maps.
    
    maps_found = []
    
# Search the map file for maps containing the input string.
    
    for i in range(len(my_maps_data)):
        if (y in my_maps_data[i][3]):maps_found.append([my_maps_data[i][0], my_maps_data[i][3]])
    if len(maps_found) == 0:
        
# Inform the user that no maps were found.
        
        print("No maps with string ", y, ".")
    else:
        
# Sort the maps according to their name
        
        maps_found.sort(key =lambda x: x[1])
        for i in range(len(maps_found)):
            
# Print map details and PBs.
            
            mapID = maps_found[i][0]
            Utils.print_map_details(mapID, my_maps_data, my_PBs)
            
# Ask user if he wants to revisit the while loop
            
    print(' ')
    print('Type \'Y\' or \'y\' if you wish to print more PBs: ', end = '')  
    x = input()
    
