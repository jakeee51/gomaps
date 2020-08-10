**API Documentation**
=====================

Main Classes
------------

GoogleMaps class
++++++++++++++++

.. py:class:: gomaps.GoogleMaps(query: str, session=None)

   A response object from a Google Maps request

   This class is initialized with a search string (query) and returns
   the result of the query. It also resolves the new redirected Google Maps URL.

   :param query: A search string that's assigned to the '?q=' URL argument.
   :param session: An HTMLSession object from the requests_html Python package.
   :type query: str
   :type session: requests_html.HTMLSession

   :returns: A single GoogleMaps object already containing the queried place's url, title, and lat/long coordinates

   .. py:attribute:: oq

      The original query string
   .. py:attribute:: query

      The URL string that a request was sent to. (example: ``'https://www.google.com/maps?q=Tops+Diner'``)
   .. py:attribute:: title

      The title or name of the place found *(available upon initialization)*
   .. py:attribute:: url

      The newly redirected URL of the place on Google Maps *(available upon initialization)*
   .. py:attribute:: coordinates

      The lattitude and longitude coordinates of the place store in tuple. (ex: ``('40.7506065', '-74.1639023')`` *(available upon initialization)*
   .. py:attribute:: coords

      Alternative for referencing *'coordinates'* attribute
   .. py:attribute:: address

      The full address of the place
   .. py:attribute:: phone_number

      The phone number (otherwise returns None)
   .. py:attribute:: website

      The website (otherwise returns None)
   .. py:attribute:: rating

      The star rating ranging from 0.0-5.0 (otherwise returns None)
   .. py:attribute:: open_hours

      The open hours of operation of the place. Returns a dictionary.
   .. py:attribute:: values

      Returns a dictionary with all the attributes of the place listed above. (Note: Only populated after ``get_values()`` member function is called)

   .. py:method:: get_values

      This sends an additional request to the new url attribute, populates the rest of the attributes, then returns a Python dictionary of all the attributes.

GoogleMapsResults class
+++++++++++++++++++++++

.. py:class:: gomaps.GoogleMapsResults(query: str, page_num=1, delay=10, log=False)

   A response object containing GoogleMaps objects as a result of the request

   This class is initialized with a search string (query) and returns
   the result(s) within a list-like object.

   :param query: A search string that's assigned to the '?q=' URL argument.
   :param page_num: The number refering to the page of results to be web scraped.
   :param delay: An integer specifying the time in seconds to wait after each request.
   :param log: If True, prints the places' GoogleMaps object as they're discovered.
   :type query: str
   :type page_num: int
   :type delay: int
   :type log: bool

   :returns: A list-like object containing GoogleMaps objects as a result of the query.

   .. py:attribute:: oq

      The original query string
   .. py:attribute:: query

      The URL string that a request was sent to. (example: ``'https://www.google.com/search?q=Tops+Diner'``)
   .. py:attribute:: url

      The newly redirected URL of the place on Google Maps *(available upon initialization)*
   .. py:attribute:: delay

      The number specifying the time in seconds to wait after each request.

   .. py:method:: list

      Returns the GoogleMapsResults object as an actual Python list


Main Functions
--------------

.. autofunction:: gomaps.maps_search

   Searches for a place(s) on Google Maps & returns the results

   :param q: The query string used to search Google Maps.
   :param page_num: The number refering to the page of results to be web scraped.
   :param delay: The number specifying the time in seconds to wait after each request.
   :param log: If True, prints the found results as they occur.
   :param single: If True, only returns the GoogleMaps object directly. (Note: Must not be amiguous to result in multiple places found)
   :type q: str
   :type page_num: int
   :type delay: int
   :type log: bool
   :type single: bool

   .. warning:: *'delay'* cannot be less than 3 seconds, otherwise bot may be detected and blocked for too many requests

   :returns: Returns a GoogleMapsResults object containing GoogleMaps objects from the search. Otherwise, returns GoogleMaps object if ``single=True``.

   :example: >>> results = gomaps.maps_search("Tops Diner")
	         >>> place = results[0].get_values()
	         >>> place.rating
	         '4.6'


.. autofunction:: gomaps.popular_times

   This function searches for a location or place on Google Maps, and returns its popular times data.

   :param location: The name of a place used to search on Google Maps
   :param driver: The path to the web driver being utilized
   :param file: The file to write the popular times data to
   :param keep_driver_alive: If True, keeps driver application open so it doesn't have to close and reopen again in loop.
   :type location: str
   :type driver: str
   :type file: str
   :type keep_driver_alive: bool

   :returns: A dictionary of the popular times data with the days of the week as keys and the values being a list of times with the percentage of how busy that place is at said time.

   :example: ``gomaps.popular_times("Tops Diner", "chromedriver.exe")``


.. autofunction:: gomaps.get_query_link

   This function returns a new link to query Google Maps

   :param place: Name of a place to be queried on Google Maps
   :type place: str

   :returns: The Google Maps URL to be send a request to

   :example: >>> get_query_link("Tops Diner")
             "https://www.google.com/maps?q=Tops+Diner"


.. autofunction:: gomaps.append_df_to_xl

   This function appends data to an Excel file

   :param file_name: Excel file name to write to
   :param data: Python Pandas DataFrame
   :type file_name: str
   :type data: pandas.DataFrame