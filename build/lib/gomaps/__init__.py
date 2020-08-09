# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: gomaps
Functionality Purpose: Acquire google maps data to utilize for web scraping
Version: Beta
'''

name = "gomaps"
from .gmapss import GoogleMaps, GoogleMapsResults, maps_search
from .busytimes import popular_times, get_query_link, append_df_to_xl
