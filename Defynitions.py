#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 15:43:47 2023

@author: cinephos
"""

# This is the directory where the project's files are locally.
# In this directory the new files will be created.

working_dir = " "

# This is the name of the local file where creation date, map uid and PB
# from every map in autosaves dir are stored. This file must be the same
# with the one defined in Definitions.cs

autosaves = "Autosaves_db.txt"

# This is the file where data of maps played are stored locally. It is created and maintained
# by the project.

my_maps = "My_maps_txt.txt"

# This is the file where the PBs are stored. 

my_PBs = "My_PBs_db.txt"

# These are your Ubisoft credentials. 
# You need to replace the asterisks with the string (without the quotes) which is 
# produced by the following console command
#base64.b64encode(b'email:password').decode()

credetials = 'Basic ****'

# This string is recommended by openplanet instructions. Use someting like:
# 'my awesome project / whoiam / myemail address' in case Nadeo has to cantact you.

useragent = ' '
