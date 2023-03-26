#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 23:15:34 2023

@author: cinephos
"""

import binascii
import csv
import datetime
import os
import re
import struct
import time

import Defynitions
import TrackmaniaAPI

# The function style_strip has been taken from the following repository
# https://github.com/PyPlanet/PyPlanet/blob/master/pyplanet/utils/style.py
# I have kept only the STRIP_ALL method, and reoved original comments.

STRIP_ALL = dict(letters='wnoitsgz<>', part=r'\$[lh]\[.+\]|\$[lh]|\$[0-9a-f]{3}')

# Strip all custom maniaplanet styles + formatting.

def style_strip(text, *strip_methods, strip_styling_blocks=True, keep_reset=False, keep_color_reset=False):
	
	if not strip_methods:
		strip_methods = [STRIP_ALL]
	regex = None
	letters = ''
	parts = []
	for payload in strip_methods:
		if isinstance(payload, str):
			regex = payload
			break
		elif isinstance(payload, dict):
			if 'letters' in payload:
				letters += payload['letters']
			if 'part' in payload:
				parts.append(payload['part'])

	if keep_reset:
		letters = letters.replace('z', '')
	if keep_color_reset:
		letters = letters.replace('g', '')
	if strip_styling_blocks:
		letters += '<>'

	if not regex:
		regex = r'(\$[{letters}]{parts})+'.format(
			letters=letters,
			parts='|{}'.format('|'.join(parts)) if len(parts) > 0 else ''
		)

	# Strip and return.
	return re.sub(regex, '', text, flags=re.IGNORECASE)


# This function exists in order to avoid complicated for / if nested loops. 
# Writes map info retrieved by the API request to the local list.

def write_maps_data (kf,resultf, my_maps_dataf):
    if any (resultf[kf]['uid'] in (match := nested_list) for nested_list in my_maps_dataf):
        row = my_maps_dataf.index(match)
        my_maps_dataf[row][1] = 'True'
        my_maps_dataf[row][2] = resultf[kf]['name']
        my_maps_dataf[row][3] = style_strip(resultf[kf]['name'])
        my_maps_dataf[row][4] = resultf[kf]['authorTime']
        my_maps_dataf[row][5] = resultf[kf]['goldTime']
        my_maps_dataf[row][6] = resultf[kf]['silverTime']
        my_maps_dataf[row][7] = resultf[kf]['bronzeTime']   
    return my_maps_dataf  


# This functions creates / updates the local maps file

def CheckPoint_2():
    
# This is the Autosaves_file

    Autosaves_file = Defynitions.working_dir + '/' + Defynitions.autosaves

# This is the My_maps_txt.file

    maps_file = Defynitions.working_dir + '/' + Defynitions.my_maps

# Open the autosaves file
    
    file = open(Autosaves_file, "r")

# Transfer data to a temporary list
    
    temp_data = list(csv.reader(file))

# Strip the header line from data and crate the autosaves list

    autosaves_data = temp_data[1:len(temp_data)][:]
    
# Close the autosaves file

    file.close()
    
# If the maps file doesn't exist, create an empty maps list

    if not (os.path.isfile(maps_file)):
        print("Local maps file doesn't exist. It is created.")
        my_maps_data = []
        
# If the local maps file exists, its data are loaded to the maps list. The file's header is removed.     
        
    else:
        file = open(maps_file, "r")
        temp_data = list(csv.reader(file))
        my_maps_data = temp_data[1:len(temp_data)][:]
        file.close()

# For each line of the autosaves list, check if the map is found in maps list.
# If not, then append a new line to the maps list with column 'exists' equals to 'False'

    for i in range(len(autosaves_data)):
        if not any(autosaves_data[i][1] in (match := nested_list) for nested_list in my_maps_data):    
            my_maps_line = [autosaves_data[i][1], 'False', ' ', ' ', 0, 0, 0, 0]
            my_maps_data.append(my_maps_line)

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
# of 100 map uids each.

    for i in range(0,len(maps_false),100):
        argstring.append(','.join(maps_false[j] for j in range(i, min(i + 100, len(maps_false)))))

# the following line executes the API request and stores the json object returned 

    for i in range(len(argstring)):
        result = api.get_maps_info(argstring[i]).get('mapList')
    
# It is necassary to sleep 2 seconds between API requests to avoid flood NADEO server with requests.
    
        time.sleep(2)
        print(len(result), " new maps were added to the maps file.")
        
# The following line stores data received to the maps list
    
        for j in range(len(result)):
            my_maps_data = write_maps_data(j, result, my_maps_data)
            
# This is the header of the maps file. 

    my_maps_header = ['Map_id', 'exists', 'Map_name', 'Map_name_stripped', 'a_time', 'g_time', 's_time', 'b_time']
    
# Open the maps file
    
    file = open(maps_file, 'w', newline='')
    csvwrite = csv.writer(file, lineterminator=os.linesep)
    
# Write the header to the map file
    
    csvwrite.writerow(my_maps_header)
    
# Write the data to the map file
    
    csvwrite.writerows(my_maps_data)

# Close the map file
    
    file.close()       
    
    return   


# This function creates / updates the PBs file
    
def CheckPoint_3():

# This is the Autosaves_file

    Autosaves_file = Defynitions.working_dir + '/' + Defynitions.autosaves

# Open the autosaves file and transfer data to a list

    file = open(Autosaves_file, "r")
    autosaves_data = list(csv.reader(file))
    file.close()

# find max_date in autosaves_data

    max_date = max(row_data[0] for row_data in autosaves_data[1:len(autosaves_data)])

# transform the date into a date string

    date_as_string = datetime.datetime.fromtimestamp(int(max_date))

# stringdate will be used as extension to the filename

    stringdate = date_as_string.strftime('_%y%m%d_%H%M')

# remove the header from autosaves data and sort the remaining data list

    data_list = autosaves_data[1:len(autosaves_data)][:]
    data_list.sort(key =lambda x: x[0])

# This is the My_Pbs text.file

    my_PBs_file = Defynitions.working_dir + '/' + Defynitions.my_PBs

# if Pbs file doesn't exist,

    if not (os.path.isfile(my_PBs_file)):
        print("PBs local file doesn't exist. It is created.")

# This the header of the PBs file.
        
        my_PBs_header = ['Unix_date','map_ID','PB_ms']
        
# Create the file and write the header
        file = open(my_PBs_file, 'w', newline='')
        csvwrite = csv.writer(file, lineterminator=os.linesep)
        csvwrite.writerow(my_PBs_header)
        file.close()
        
# Create an empty PBs list
        
        my_PBs_data =[]
        
# Set last date to zero.
        
        last_date = 0
    
# If the PBs file exists
    
    else:
        
# transfer its data to the PBs list, and remove the header from the list
        
        file = open(my_PBs_file, "r")
        temp_data = list(csv.reader(file))
        my_PBs_data = temp_data[1:len(temp_data)][:]    

# Set last date as the newest entry of the PBs list  
   
        last_date = int(max(row_data[0] for row_data in my_PBs_data[1:len(my_PBs_data)]))
        
# Close the PBs file
        
        file.close()

# Reset the PBs list

    my_PBs_data = []
    
# Check each entry of the data list and transfer data to the PBs list,
# if their date is newer than last date.    

    for i in range(len(data_list)) :
        if int(data_list[i][0]) > last_date: my_PBs_data.append(data_list[i])  

# Open the PBs file and append new data from PBs list
    
    file = open(my_PBs_file, 'a', newline='')
    csvwrite = csv.writer(file, lineterminator=os.linesep)
    csvwrite.writerows(my_PBs_data)
    file.close()   

# Rename autosaves file and add the time stamp to its name.
 
    os.rename(Autosaves_file, Autosaves_file[:-4] + stringdate + Autosaves_file[-4:]) 
 
    return
