**API Documentation**
=====================

Main Classes
------------

GoogleMaps class
++++++++++++++++

.. py:class:: gomaps.GoogleMaps(query: str, fields=[], session=None)

   A response object from a Google Maps request

   This class is initialized with a search string (query) and returns
   the result of the query. It also resolves the new redirected Google Maps URL.

   :param q: A search string that's assigned to the '?q=' URL argument.
   :param fields: Specify which data points to scrape.
   :param session: An HTMLSession object from the requests_html Python package.
   :type q: str
   :type fields: list
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
   .. py:attribute:: popular_times

      The Google Maps `Popular Times <https://support.google.com/business/answer/6263531?hl=en>`_ data for 7 days of the week. Returns a dictionary.
   .. py:attribute:: values

      Returns a dictionary with all the attributes of the place listed above. (Note: Only populated after ``get_values()`` member function is called)

   .. py:method:: get_values

      This sends an additional request, populates the rest of the attributes, then returns a Python dictionary of all the attributes.

   .. admonition:: Tip

      The GoogleMaps object's attributes can be accessed via the dot operator or key indexing. (ex: ``result[coords]`` or ``result.coords``)

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

      The newly redirected URL of the place on Google Maps *(available upon initialization as long as there's only a single result)*
   .. py:attribute:: delay

      The number specifying the time in seconds to wait after each request.

   .. py:method:: list

      Returns the GoogleMapsResults object as an actual Python list


Main Functions
--------------

.. py:function:: gomaps.maps_search(q: str, page_num=1, delay=10, log=False, single=False, fields=[])

   Searches for a place(s) on Google Maps & returns the results

   :param q: The query string used to search Google Maps.
   :param page_num: The number refering to the page of the results to be web scraped.
   :param delay: The number specifying the time in seconds to wait after each request.
   :param log: If True, prints the found results as they occur.
   :param single: If True, only returns the single GoogleMaps object directly.
   :param fields: If ``single=True``, specify which data points to scrape.

   .. warning:: delay cannot be less than 5 seconds, otherwise bot will be detected and blocked for too many requests

   :returns: Returns a GoogleMapsResults object containing GoogleMaps objects from the search

   :example: >>> results = gomaps.maps_search("Tops Diner")
             >>> place = results[0].get_values()
             >>> place.rating
             4.6

.. admonition:: Tip

   The following functions are overloaded. That being said the functions with ``data`` as a parameter can take an HTML string as input for ``data`` as well as a normal query string.

.. py:function:: gomaps.geocoder(location: str, reverse: bool=False)

   Searches for the lattitude & longitude coordinates of a location.
   Reverse geocoding searches for the location of coordinates

   :param location: A place name, address or lat/long coordinates
   :param reverse: If True, uses reverse geocoder

   .. admonition:: Note

      This function doesn't scrape *everything*. As a result, it is especially lightweight as opposed to using maps_search

   :returns: Returns a tuple of lat/long coordinates or address of the location if ``reverse=True``'''

   :example: >>> result = gomaps.geocoder("Tops Diner")
             >>> result
             ('40.7506065', '-74.1639023')



.. py:function:: gomaps.get_url(data: str)

   Searches for full Google Maps URL of a location

   :param data: A place name, address or lat/long coordinates

   :returns: Returns a string of the redirected URL

.. py:function:: gomaps.get_title(data: str)

   Searches for the title or name of a location

   :param data: A place name, address or lat/long coordinates

   :returns: Returns a string of the location's title



.. py:function:: gomaps.get_address(data: str, validate: bool=False)

   Searches for the full address of a location

   :param data: A place name, address or lat/long coordinates
   :param validate: If True, attempts to validate address

   :returns: Returns a string of the location's address

.. py:function:: gomaps.get_website(data: str)

   Searches for the website (if any) of a location

   :param data: A place name

   :returns: Returns a string of the location's website



.. py:function:: gomaps.get_phone_number(data: str)

   Searches for the phone number (if any) of a location

   :param data: A place name

   :returns: Returns a string of the location's phone number

.. py:function:: gomaps.get_rating(data: str)

   Searches for the rating (if any) of a location

   :param data: A place name

   :returns: Returns a float of the location's rating



   .. py:function:: gomaps.get_open_hours(data: str)

   Searches for the open hours (if any) of a location

   :param data: A place name

   :returns: Returns a string of the location's open hours

.. py:function:: gomaps.get_popular_times(data: str)

   Searches for the Google Maps popular times (if any) of a location

   :param data: A place name

   :returns: Returns a string of the location's popular times