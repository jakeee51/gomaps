# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: gmapss (Google Maps Search)
Functionality Purpose: Acquire google maps data of a place based on query
Version: Beta
'''
#5/25/20

# &gws_rd=cr -> implement optional redirects

import signal, time, os, sys, re
from .utils import *

def __keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)
signal.signal(signal.SIGINT, __keyboardInterruptHandler)

class InvalidFieldsError(Exception):
   pass

class GoogleMaps:
   '''A response object from a Google Maps request

   This class is initialized with a search string (query) and returns
   the result of the query. It also resolves the new redirected Google Maps URL.

   :param q: A search string that's assigned to the '?q=' URL argument.
   :param fields: Specify which data points to scrape.
   :param session: An HTMLSession object from the requests_html Python package.
   :type q: str
   :type fields: list
   :type session: requests_html.HTMLSession

   :returns: A single GoogleMaps object already containing the queried place's url, title, and lat/long coordinates
   '''
   __mq = "https://www.google.com/maps?q="
   __sq = "https://www.google.com/search?q="
   __resp = None
   VALID_FIELDS = ["title", "url", "coords", "coordinates", "address",
                   "website", "phone_number", "rating", "open_hours", "popular_times"]

   def __init__(self, q: str, fields: list=[], url_args: str='', session=None):
      if session != None:
         self.__sesh = session
      else:
         self.__sesh = HTMLSession()
      self.oq = re.sub(fr"({self.__mq}|{self.__sq})", '', q.replace('+', ' '))
      self.query = self.__mq + quote_plus(self.oq)
      self.__resp = requests.get(self.query)
      url_components = re.search(
         r'https://www.google.com/maps/preview/place/.+?\\"', self.__resp.text)
      self.url = self.title = self.__fields_valid = None
      if len(fields) != 0:
         self.__fields_valid = self.__fields_check(fields)
         if self.__fields_valid:
            self.__attribute_fields(fields)
            self.__set_url(url_components); del(self.__resp)
            self.get_values(fields)
      else:
         self.coords = self.coordinates = (None,None)
         self.__set_url(url_components); del(self.__resp)
   def __repr__(self):
      if self.__fields_valid:
         return f"{self.values}"
      elif self.url == None:
         return f"<gomaps.GoogleMaps object; Place Not Found>"
      else:
         return f"<gomaps.GoogleMaps object; Place-Name: {self.title}>"
   def __iter__(self):
      return iter(self.values)
   def __getitem__(self, key):
      return self.values[key]

   def __fields_check(self, fields: list=[]) -> bool:
      if len(fields) > 10:
         raise InvalidFieldsError("Too many fields specified!")
      for field in fields:
         if field in self.VALID_FIELDS:
            pass
         else:
            raise InvalidFieldsError("1 or more of the fields entered are invalid!\n"\
                                     "Check self.VALID_FIELDS for reference.")
      return True
   def __attribute_fields(self, fields: list=[]):
      for attr in fields:
         if attr == "open_hours":
            self.open_hours = {}
         elif attr == "popular_times":
            self.popular_times = {}
         elif attr in self.VALID_FIELDS[2:4]:
            self.coords = self.coordinates = (None,None)
         else:
            if attr not in self.__dict__:
               self.__dict__[attr] = None
   def __set_url(self, url_exists: re): # set the url, title & coords attributes
      if url_exists:
         try:
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
         except AttributeError:
            pass
   def __set_attrs(self, query: str, fields: list=[]):
      resp = self.__sesh.get(self.__sq + quote_plus(query)); resp.html.render(timeout=30)
      if self.__fields_valid and len(fields) != 0:
         attrs_switch(self, resp.html.html, fields)
      else:
         self.address = get_address(resp.html.html)
         self.website = get_website(resp.html.html)
         self.phone_number = get_phone_number(resp.html.html)
         self.rating = get_rating(resp.html.html)
         hours_results = get_open_hours(resp.html.html)
         if hours_results[1] != None:
            self.open_hours["Currently"] = hours_results[1]
         if hours_results[0] != None:
             self.__set_hours(hours_results[0])
         ptimes = get_popular_times(resp.html.html)
         if ptimes != None:
            self.__set_pop_times(ptimes)
   def __set_hours(self, hours: str):
      self.open_hours["Hours"] = {}
      table = re.search(r"<td.+</td>", str(hours)).group().strip("</td>")
      parsed = re.sub(r"(<td)? class=\"\w+\">", '', table)
      dow = re.sub(r"</td><td>", ' ', parsed).split("</td></tr><tr>")
      for row in dow:
         if len(row) > 24:
            row = re.sub(r"<div>.+?</div>", '', row)
         row = re.sub(r"<div><span", '', row)
         day = row.split(' ')[0]
         open_times = row.split(' ')[1]
         self.open_hours["Hours"][day] = open_times
   def __pop_hours(self) -> tuple:
      pop_hours = tuple()
      for hour in range(6, 24):
         if hour < 12:
            pop_hours += ("% busy at " + str(hour) + " AM",)
         elif hour == 12:
            pop_hours += ("% busy at 12 PM",)
         else:
            pop_hours += ("% busy at " + str(hour-12) + " PM",)
      return pop_hours
   def __set_pop_times(self, ptimes: list):
      days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
      i = 0
      for day in ptimes:
         prep = day.replace(',', "{},")
         times = prep.format(*self.__pop_hours()).strip(',')
         self.popular_times[days[i]] = times.split(','); i += 1
   def __set_values(self, fields: list=[]):
      if self.__fields_valid and len(fields) != 0:
         self.values = values_switch(self, fields)
      else:
         self.values["title"] = self.title
         self.values["url"] = self.url
         self.values["coords"] = self.coords
         self.values["address"] = self.address
         self.values["website"] = self.website
         self.values["phone_number"] = self.phone_number
         self.values["rating"] = self.rating
         self.values["open_hours"] = self.open_hours
         self.values["popular_times"] = self.popular_times

   def get_values(self, fields: list=[]):
      if self.__fields_valid and len(fields) != 0:
         self.values = {}
         self.__set_attrs(self.oq, fields)
         self.__set_values(fields)
         return self.values
      else:
         self.address = self.website = None; self.values = {}
         self.phone_number = self.rating = None; self.open_hours = {}
         self.popular_times = {}
         self.__set_attrs(self.oq)
         self.__set_values()
         return self.values

class GoogleMapsResults:
   '''A response object containing GoogleMaps objects as a result of the request

   This class is initialized with a search string (query) and returns
   the result(s) within a list-like object.

   :param q: A search string that's assigned to the '?q=' URL argument.
   :param page_num: The number refering to the page of the results to be web scraped.
   :param delay: An integer specifying the time in seconds to wait after each request.
   :param log: If True, prints the places' GoogleMaps object as they're discovered.
   :type q: str
   :type page_num: int
   :type delay: int
   :type log: bool

   :returns: A list-like object containing GoogleMaps objects as a result of the query.
   '''
   __mq = "https://www.google.com/maps?q="
   __sq = "https://www.google.com/search?q="
   __n_a = "There are no local results matching your search!"
   __results = []

   def __init__(self, q: str, page_num: int=1, url_args: str='',
                delay: int=10, log: bool=False):
      self.oq = re.sub(self.__sq, '', q.replace('+', ' '))
      self.query = self.__sq + quote_plus(self.oq)
      self.__pn = page_num; self.delay = delay
      self.__sesh = HTMLSession(); self.url = None
      self.__resp = GoogleMaps(self.oq, session=self.__sesh)
      if self.__resp.url != None: # Check if query only yields single result
         self.__results.append(self.__resp)
         self.url = self.__resp.url; del(self.__resp)
      else:
         try:
            self._place_names = self._get_place_names(self.oq) or [self.__n_a]
            if self._place_names[0] != self.__n_a:
               for name in self._place_names:
                  result = GoogleMaps(name, session=self.__sesh)
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
      expr = fr"/search\?q={Q}&amp;npsic.+?\""
      href = re.search(expr, resp.html.html)
      if not href:
          Q = query.replace(' ','\+')
          expr = fr"/search\?q={Q}&amp;npsic.+?\""
          href = re.search(expr, resp.html.html)
          if not href:
              return None
      self.url = list_link = "https://www.google.com" +\
                 href.group().replace("&amp;", '&').strip('"')
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

def maps_search(q: str, page_num: int=1, delay: int=10, url_args: str='',
                log: bool=False, single: bool=False, fields: list=[]): # Returns list unless single is True
   '''Searches for a place(s) on Google Maps & returns the results

   :param q: The query string used to search Google Maps.
   :param page_num: The number refering to the page of the results to be web scraped.
   :param delay: The number specifying the time in seconds to wait after each request.
   :param log: If True, prints the found results as they occur.
   :param single: If True, only returns the single GoogleMaps object directly.
   :param fields: If ``single=True``, specify which data points to scrape.

   .. warning:: delay cannot be less than 5 seconds, otherwise bot will be detected and blocked for too many requests

   :returns: Returns a GoogleMapsResults object containing GoogleMaps objects from the search
   '''
   if single or len(fields) > 0:
      return GoogleMaps(q, fields=fields)
   if re.search(r"^.+\..+$", q) and ' ' not in q:
      q = re.sub(r"(https?://)?www\.google\.com/(search|maps)\?q=",
                 '', q)
      q = unquote_plus(q)
   if delay < 5:
      delay = 5
   return GoogleMapsResults(q, page_num=page_num, delay=delay, log=log)
