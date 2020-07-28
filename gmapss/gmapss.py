# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: gmapss
Functionality Purpose: Acquire google maps data to utilize for web scraping
Version: Alpha 0.0.2
'''
#7/28/20

import requests, time, json, os, sys, re
from bs4 import BeautifulSoup
from urllib.request import urlparse, urlretrieve
from urllib.parse import quote_plus, unquote_plus

class GoogleMapsSearch:
   '''
   This class is initialized with a search string (query) and returns
   the result(s) of the query. It resolves the new url to allow web scraping
   '''

   __q = "https://www.google.com/maps?q="
   __resp = None

   def __init__(self, query: str):
      query = query.replace('+', ' ').strip(self.__q)
      self.query = self.__q + quote_plus(query)
      self.__resp = requests.get(self.query)
      url_components = re.search(r'https://www.google.com/maps/preview/place/.+?\\"', self.__resp.text)
      self.url = None; self.results = []
      if url_components:
         prefix = re.sub(r"\?q=", "/place/", self.query).replace('+', "\+")
         path = re.search(fr"{prefix}/data.+?\"", self.__resp.text).group()
         path = re.sub(r"\\\\u003d", '=', path)
         coords = re.search(r"@-?\d\d?\.\d{4,8},-?\d\d?\.\d{4,8}",
                            url_components.group()).group()
         path = re.sub(r"/data", f"/{coords},17z/data", path)
         self.url = path[:-11] + "!8m2!3d" + re.sub(r",", "!4d", coords.strip('@'))
   def __repr__(self):
      return f"<GoogleMapsSearch - query: {self.query}>"
   def __iter__(self):
      return iter(self.results)
   def __getitem__(self, key):
      return self.results[key]

def main():
   url = "https://www.google.com/maps?q=Tops+Diner"
   resp = GoogleMapsSearch(url)
   resp = requests.get(resp.url)
   print(resp.url)
##   with open("test.html", 'w') as f:
##      f.write(str(resp.text.encode("utf-8")))

if __name__ == "__main__":
   main()
