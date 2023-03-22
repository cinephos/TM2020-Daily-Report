#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 20:38:50 2023

@author: cinephos
"""

# The class TmApi is taken from the following repository
# https://github.com/Tomczan/discord-bot-trackmania-matchmaking/blob/main/trackmaniaAPI.py
# Contain the functions that enable communication and data retrieval.
# The functions get_map_info and get_maps_info have been added by myself.

import requests
import base64
import http.client
import json
import Defynitions
#from decouple import config


class TmApi:
    ticket = ''
    refresh_ticket = ''
    ticket_level1 = ''
    ticket_level2 = ''

    # uplay token
    def level0(self):
        conn = http.client.HTTPSConnection("public-ubiservices.ubi.com")
        payload = ""
        headers = {
            'Content-Type': 'application/json',
            #'Basic base64.b64encode(b'email:password').decode()',
            'Authorization': Defynitions.credetials,
            # Trackmania ID
            'Ubi-AppId': '86263886-327a-4328-ac69-527f0d20a237',
            'User-Agent': Defynitions.useragent
        }
        conn.request("POST", "/v3/profiles/sessions", payload, headers)
        res = conn.getresponse()
        data = res.read()
        decoded_data = data.decode("utf-8")
        response = json.loads(decoded_data)
        return response

    # nadeo token v1
    def level1(self, ticket):
        headers = {
            "Authorization": "ubi_v1 t=" + ticket,
            'User-Agent': Defynitions.useragent
        }
        nadeo_accesstoken = requests.post(
            "https://prod.trackmania.core.nadeo.online/v2/authentication/token/ubiservices", headers=headers
        )
        return nadeo_accesstoken.json()

    # nadeo token v2
    def level2(self, token):
        payload = {
            'audience': 'NadeoLiveServices'
        }
        headers = {
            "Authorization": "nadeo_v1 t=" + token,
            'User-Agent': Defynitions.useragent
        }
        nadeo_services = requests.post(
            "https://prod.trackmania.core.nadeo.online/v2/authentication/token/nadeoservices", headers=headers, data=payload
        )
        return nadeo_services.json()

    def get_ticket_level_2(self):
        try:
            response_level0 = self.level0()
            response_level1 = self.level1(response_level0['ticket'])
            response_level2 = self.level2(response_level1['accessToken'])
        except:
            return "Couldnt get a response from apis"
        if response_level2:
            self.ticket_level1 = response_level0['ticket']
            self.ticket_level2 = response_level1['accessToken']
            self.ticket = response_level2['accessToken']
            self.refresh_ticket = response_level2['refreshToken']
            return response_level2

    def get_new_refresh_ticket(self):
        url = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/refresh"
        headers = {
            'Authorization': 'nadeo_v1 t=' + self.refresh_ticket,
            'User-Agent': Defynitions.useragent
        }
        try:
            refresh_ticket = requests.post(url, headers=headers)
            print("Refresh ticket: ", type(refresh_ticket))
            refresh_ticket = refresh_ticket.json()
            print("Refresh ticket: ", type(refresh_ticket))
        except:
            return 'Could not connect with api, try to use "get_ticket" before.'
        if refresh_ticket:
            self.ticket = refresh_ticket['accessToken']
            self.refresh_ticket = refresh_ticket['refreshToken']
            return refresh_ticket
 
# This function request a sibgle map info.
       
    def get_map_info(self, map_id):
        url = "https://live-services.trackmania.nadeo.live/api/token/map/" + map_id
        headers = {
            'Authorization': 'nadeo_v1 t=' + self.ticket,
            'User-Agent': Defynitions.useragent
        }
        try:
            map_info = requests.get(url, headers=headers)
            return map_info.json()
        except:
            return 'Could not connect with api and get map info.'

# This function request multiple maps info. The argument is a string with the map uids
# seperated by a comma. The string must include maximum 100 maps.
 
    def get_maps_info(self, request_arg):
        url = "https://live-services.trackmania.nadeo.live/api/token/map/get-multiple?mapUidList=" + request_arg
        headers = {
            'Authorization': 'nadeo_v1 t=' + self.ticket,
            'User-Agent': Defynitions.useragent
        }
        try:
            maps_info = requests.get(url, headers=headers)
            return maps_info.json()
        except:
            return 'Could not connect with api and get player info.'
        