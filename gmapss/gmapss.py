# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: gmapss
Functionality Purpose: Acquire google maps data of a place based on query
Version: Alpha 0.0.6
'''
#8/4/20

import requests, time, json, os, sys, re
import pyppdf.patch_pyppeteer
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.request import urlparse, urlretrieve
from urllib.parse import quote_plus, unquote_plus

# Put single result in list by default
# Account for multiple results (just return titles, urls, coords & w/e else)
# Index with "var a=document.body.offsetWidth,b=" for optimization
# Prep for package production
# Optimize speed

class GoogleMapsSearch:
   '''
   This class is initialized with a search string (query) and returns
   the result(s) of the query. It resolves the new url to allow web scraping
   '''
   __q = "https://www.google.com/maps?q="
   __s = "https://www.google.com/search?q="
   __resp = None

   def __init__(self, query: str):
      query = query.replace('+', ' ').strip(self.__q)
      self.query = self.__q + quote_plus(query)
      self.__resp = requests.get(self.query)
      self.__results = [0] # if multiple results get multiple urls
      url_components = re.search(
         r'https://www.google.com/maps/preview/place/.+?\\"', self.__resp.text)
      if not self.__multiple_results():
         self.url = self.title = self.address = self.website = None
         self.phone_number = self.rating = None; self.open_hours = {}
         self.coords = self.coordinates = (None,None); self.values = {}
         self.__set_url(url_components)
         self.__set_attrs(query); del(self.__resp)
      self.__set_values()
   def __repr__(self):
      if len(self.__results) == 1:
         return f"<gmapss.GoogleMapsSearch object; Place Name: {self.title}>"
      return f"GoogleMapsSearchResults({self.__results})"
   def __iter__(self):
      if len(self.__results) == 1:
         return iter(self.values)
      return iter(self.__results)
   def __getitem__(self, key):
      if len(self.__results) == 1:
         return self.values[key]
      return self.__results[key]

   def __multiple_results(self):
      return False
   def __set_url(self, url_exists):
      if url_exists:
         prefix = re.sub(r"\?q=", "/place/", self.__q).replace('+', "\+")
         path = re.search(fr'{prefix}.+?/data.+?\\"', self.__resp.text).group()
         path = re.sub(r"\\\\u003d", '=', path)
         coords = re.search(r"@-?\d\d?\.\d{4,8},-?\d\d?\.\d{4,8}",
                            url_exists.group()).group()
         self.coords = self.coordinates = tuple(coords.strip('@').split(','))
         path = re.sub(r"/data", f"/{coords},17z/data", path)
         self.url = path[:-11] + "!8m2!3d" + re.sub(r",", "!4d", coords.strip('@'))
   def __set_attrs(self, query: str):
      session = HTMLSession()
      resp = session.get(self.__s + quote_plus(query)); resp.html.render()
      self.title = resp.html.find("em", first=True).text
      try:
         address = re.search(r"Address</a>: </span>.+?</span>",
                             resp.html.html)
         self.address = re.sub(r"Address</a>: </span>.+?>", '',
                               address.group()).strip("</span>")
      except (TypeError, AttributeError):
            pass
      try:
         website = re.search(r"Web Result with Site Links.+?onmousedown",
                             resp.html.html)
         self.website = re.sub(r"Web Result with Site Links.+?href=\"", '',
                               website.group()).strip("\" onmousedown")
      except (TypeError, AttributeError):
         pass
      try:
         phone = re.search(r"Phone</a>: </span>.+?</span>", resp.html.html)
         self.phone_number = re.search(r"\(?\d{3}\)? \d{3}-\d{4}", phone.group()).group()
      except (TypeError, AttributeError):
         pass
      try:
         rating = re.search(r"Rated \d\.?\d? out of 5", resp.html.html)
         self.rating = rating.group().strip(" out of 5").strip("Rated ")
      except (TypeError, AttributeError):
         pass
      try:
         hours = re.search(r"Hours</a>: </span>.+?</table>", resp.html.html)
         current = re.search(r"(Opens|Close[sd])( soon)?</b>...((Opens|Closes) \d{1,2}(AM|PM))",
                             resp.html.html)
         self.open_hours["Currently"] = f"{current.group(1)} - {current.group(3)}"
         self.__set_hours(hours.group())
      except (TypeError, AttributeError):
         pass
   def __set_hours(self, hours: str):
      self.open_hours["Hours"] = {}
      table = re.search(r"<td.+</td>", str(hours)).group().strip("</td>")
      parsed = re.sub(r"(<td)? class=\"\w+\">", '', table)
      dow = re.sub(r"</td><td>", ' ', parsed).split("</td></tr><tr>")
      for row in dow:
         day = row.split(' ')[0]
         open_times = row.split(' ')[1]
         self.open_hours["Hours"][day] = open_times
      
   def __set_values(self):
      if len(self.__results) == 1:
         self.values["title"] = self.title
         self.values["url"] = self.url
         self.values["address"] = self.address
         self.values["coords"] = self.coords
         self.values["website"] = self.website
         self.values["phone_number"] = self.phone_number
         self.values["rating"] = self.rating
         self.values["open_hours"] = self.open_hours
      else:
         self.results = self.__results

def main():
   url = "Sopranos Pizza"
   url = "Tops Diner"
   resp = GoogleMapsSearch(url)
   print("\nOutput:", resp)

if __name__ == "__main__":
   main()
