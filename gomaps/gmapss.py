# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: gmapss
Functionality Purpose: Acquire google maps data of a place based on query
Version: Beta
'''
#8/9/20

import requests, signal, time, os, sys, re
import pyppdf.patch_pyppeteer
from requests_html import HTMLSession
from urllib.parse import quote_plus, unquote_plus

# Optimize speed

class GoogleMaps:
   '''A response object from a Google Maps request

   This class is initialized with a search string (query) and returns
   the result of the query. It also resolves the new redirected Google Maps URL.

   :param query: A search string that's assigned to the '?q=' URL argument.
   :param session: An HTMLSession object from the requests_html Python package.
   :type query: str
   :type session: requests_html.HTMLSession

   :returns: A single GoogleMaps object already containing the queried place's url, title, and lat/long coordinates
   '''
   __mq = "https://www.google.com/maps?q="
   __sq = "https://www.google.com/search?q="
   __resp = None

   def __init__(self, query: str, session=None):
      if session != None:
         self.__sesh = session
      else:
         self.__sesh = HTMLSession()
      self.oq = re.sub(self.__mq, '', query.replace('+', ' '))
      self.query = self.__mq + quote_plus(self.oq)
      self.__resp = requests.get(self.query)
      url_components = re.search(
         r'https://www.google.com/maps/preview/place/.+?\\"', self.__resp.text)
      self.url = self.title = None
      self.coords = self.coordinates = (None,None)
      self.__set_url(url_components); del(self.__resp)
   def __repr__(self):
      if self.url == None:
         return f"<gomaps.GoogleMaps object; Place Not Found>"
      return f"<gomaps.GoogleMaps object; Place-Name: {self.title}>"
   def __iter__(self):
      return iter(self.values)
   def __getitem__(self, key):
      return self.values[key]

   def __set_url(self, url_exists):
      if url_exists:
         prefix = re.sub(r"\?q=", "/place/", self.__mq).replace('+', "\+")
         path = re.search(fr'{prefix}.+?/data.+?\\"', self.__resp.text).group()
         path = re.sub(r"\\\\u003d", '=', path)
         coords = re.search(r"@-?\d\d?\.\d{4,8},-?\d\d?\.\d{4,8}",
                            url_exists.group()).group()
         self.coords = self.coordinates = tuple(coords.strip('@').split(','))
         path = re.sub(r"/data", f"/{coords},17z/data", path)
         self.url = path[:-11] + "!8m2!3d" + re.sub(r",", "!4d", coords.strip('@'))
         title = re.search(r"(?<=https://www.google.com/maps/place/)\w+.*?/@",
                                self.url).group().strip("/@")
         self.title = unquote_plus(title)
   def __set_attrs(self, query: str):
      resp = self.__sesh.get(self.__sq + quote_plus(query)); resp.html.render()
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
         self.values["title"] = self.title
         self.values["url"] = self.url
         self.values["address"] = self.address
         self.values["coords"] = self.coords
         self.values["website"] = self.website
         self.values["phone_number"] = self.phone_number
         self.values["rating"] = self.rating
         self.values["open_hours"] = self.open_hours

   def get_values(self):
      self.address = self.website = None; self.values = {}
      self.phone_number = self.rating = None; self.open_hours = {}
      self.__set_attrs(self.oq)
      self.__set_values()
      return self.values

class GoogleMapsResults:
   '''A response object containing GoogleMaps objects as a result of the request

   This class is initialized with a search string (query) and returns
   the result(s) within a list-like object.

   :param query: A search string that's assigned to the '?q=' URL argument.
   :param page_num: The number refering to the page of the results to be web scraped.
   :param delay: An integer specifying the time in seconds to wait after each request.
   :param log: If True, prints the places' GoogleMaps object as they're discovered.
   :type query: str
   :type page_num: int
   :type delay: int
   :type log: bool

   :returns: A list-like object containing GoogleMaps objects as a result of the query.
   '''
   __mq = "https://www.google.com/maps?q="
   __sq = "https://www.google.com/search?q="
   __n_a = "There are no local results matching your search!"
   __results = []

   def __init__(self, query: str, page_num=1, delay=10, log=False):
      self.oq = re.sub(self.__sq, '', query.replace('+', ' '))
      self.query = self.__sq + quote_plus(self.oq)
      self.__pn = page_num; self.delay = delay
      self.__sesh = HTMLSession(); self.url = None
      self.__resp = GoogleMaps(self.oq, self.__sesh)
      if self.__resp.url != None: # Check if query only yields single result
         self.__results.append(self.__resp); del(self.__resp)
      else:
         try:
            self._place_names = self._get_place_names(self.oq) or [self.__n_a]
            if self._place_names[0] != self.__n_a:
               for name in self._place_names:
                  result = GoogleMaps(name)
                  time.sleep(self.delay)
                  self.__results.append(result)
                  if log:
                     print(result)
            else:
               self.__results = self._place_names
         except KeyboardInterrupt:
            print("Interrupted Scrape!")
            try:
               sys.exit(0)
            except SystemExit:
               os._exit(0)
   def __repr__(self):
      return f"GoogleMapsResults({self.__results})"
   def __iter__(self):
      return iter(self.__results)
   def __getitem__(self, key):
      return self.__results[key]

   def _get_place_names(self, query: str) -> list:
      q = self.__sq + quote_plus(query); names = []
      resp = self.__sesh.get(q); resp.html.render()
      next_page = "&#rlfi=start:"; Q = quote_plus(query).replace('+','\+')
      href = re.search(fr"/search\?q={Q}&amp;npsic.+?\"",
                            resp.html.html)
      self.url = list_link = "https://www.google.com" +\
                 href.group().replace("&amp;", '&')
      if self.__pn > 1:
         idx = 20*(int(self.__pn)-1)
         next_page += str(idx)
         list_link += next_page
      subs = '|'.join(query.split(' '))
      expr = fr"\\\\u0026q\\\\u003d[A-Z].*?(?:{subs})?.*?"\
             "\\\\u0026ludocid"
      resp = self.__sesh.get(list_link)
      gathering = re.findall(expr, resp.html.html)
      for match in gathering:
         parsed = re.sub(r"(\\\\u0026q\\\\u003d|\\\\u0026ludocid)", '', match)
         name = unquote_plus(parsed)
         names.append(name.replace("\\x27", "'"))
      if len(names) != 0:
         return names

   def list(self) -> list:
      return self.__results

def __keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)
signal.signal(signal.SIGINT, __keyboardInterruptHandler)

def maps_search(q: str, page_num: int=1, delay: int=10,
                log: bool=False, single: bool=False): # Returns list unless single is True
   '''Searches for a place(s) on Google Maps & returns the results

   :param q: The query string used to search Google Maps.
   :param page_num: The number refering to the page of the results to be web scraped.
   :param delay: The number specifying the time in seconds to wait after each request.
   :param log: If True, prints the found results as they occur.
   :param single: If True, only returns the single GoogleMaps object directly.

   .. warning:: delay cannot be less than 3 seconds, otherwise bot will be detected and blocked for too many requests

   :returns: Returns a GoogleMapsResults object containing GoogleMaps objects from the search
   '''
   if single:
      return GoogleMaps(q)
   if re.search(r"^.+\..+$", q) and ' ' not in q:
      q = re.sub(r"(https?://)?www\.google\.com/(search|maps)\?q=",
                 '', q)
      q = unquote_plus(q)
   if delay < 3:
      delay = 3
   return GoogleMapsResults(q, page_num, delay, log)
