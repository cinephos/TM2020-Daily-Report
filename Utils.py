#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 23:15:34 2023

@author: cinephos
"""

import re
import struct
import binascii
import os
import csv


# The function style_strip has been taken from the following repository
# https://github.com/PyPlanet/PyPlanet/blob/master/pyplanet/utils/style.py
# I have kept only the STRIP_ALL method, and reoved original comments.
# I have added two more functions beneath.

STRIP_ALL = dict(letters='wnoitsgz<>', part=r'\$[lh]\[.+\]|\$[lh]|\$[0-9a-f]{3}')
"""
Strip all custom maniaplanet styles + formatting.
"""

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

# This function exists in order to avoid complicated for / if nested loops. 
# Saves the data from the map list to the map file.

def write_csv_file(maps_filef,my_maps_dataf):
    file = open(maps_filef, 'w', newline='')
    csvwrite = csv.writer(file, lineterminator=os.linesep)
    csvwrite.writerows(my_maps_dataf)
    file.close()

