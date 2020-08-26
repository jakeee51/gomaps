# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: gomaps
Functionality Purpose: Acquire google maps data to utilize for web scraping
Version: Beta
'''

name = "gomaps"
from .gmapss import GoogleMaps, GoogleMapsResults, maps_search
from .utils import geocoder, get_url, get_title, get_address, get_website,\
     get_phone_number, get_rating, get_open_hours, get_popular_times
