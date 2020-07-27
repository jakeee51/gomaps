# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: gmapss
Functionality Purpose: Acquire google maps data to utilize for web scraping
Version: Alpha 0.0.1
'''
#7/27/20

import requests, time, os, sys, re

class GoogleMapsSearch:
   pass

def main():
   url = "https://www.google.com/maps?q=Tops+Diner"
   resp = requests.get(url, allow_redirects=True)
   print(resp.url)
   with open("test.html", 'w') as f:
      f.write(resp.text)

if __name__ == "__main__":
   main()
