**QuickStart**
====================

Gomaps! A Google Maps web scraper for querying places on Google Maps and scraping the metadata of that search (No API key needed). This package also does geocoding, reverse geocoding and address validation! It's essentially a lite version of the Google Maps Places API. Results of a query include the following:

* Place Name
* Place Google Maps URL
* Place Address
* Place Coordinates (lattitude/longitude)
* Place Website
* Place Phone Number
* Place Star Rating (★★★★★)
* Place Open Hours
* Place Popular Times

That's right! This can also scrape Google Maps **Popular Times** data!
For more information about Google's popular times data, refer to this support post: https://support.google.com/business/answer/6263531?hl=en.

Installation
------------

.. code-block:: bash

   $ pip install gomaps

Usage
-----

There are two main functions to this Python package. To start, import the functions from the `gomaps` package.

:py:func:`~gomaps.maps_search`
++++++++++++++++++++++++++++++

>>> from gomaps import maps_search
>>> results = maps_search("Tops Diner") # Returns a list like object
GoogleMapsResults([<gomaps.*GoogleMaps* object; Place-Name: Tops Diner>])

The function ``maps_search()`` is returning a :py:class:`~gomaps.GoogleMapsResults` object that contains all the places that were found in the scrape. *In this case* only one place was found since the inquiry for "Tops Diner" was specific enough to have only **one** result.

.. code-block:: python

   results[0].get_values() # Populates the object's attributes & returns a dictionary
   '''
   {
     'title': 'Tops Diner',
     'url': 'https://www.google.com/maps/place/Tops+Diner/@40.7506065,-74.1639023,17z/data=!4m2!3m1!1s0x89c2547b4ec3235b:0x7342f11f69197f92!8m2!3d40.7506065!4d-74.1639023',
     'address': '500 Passaic Ave, East Newark, NJ 07029',
     'coords': ('40.7506065', '-74.1639023'),
     'website': 'https://www.thetopsdiner.com/',
     'phone_number': '(973) 481-0490',
     'rating': 4.6,
     'open_hours': {'Currently': 'Closed - Opens 8AM',
                    'Hours': {'Friday': '8AM–11PM', 'Saturday': '8AM–11PM', 'Sunday': '8AM–11PM',
                              'Monday': '8AM–11PM', 'Tuesday': '8AM–11PM', 'Wednesday': '8AM–11PM', 'Thursday': '8AM–11PM'}
                   }
     'popular_times': {
                       'Sunday': ['0% busy at 6 AM', '0% busy at 7 AM', '19% busy at 8 AM', '35% busy at 9 AM', '48% busy at 10 AM',
                       '52% busy at 11 AM', '49% busy at 12 PM', '44% busy at 1 PM', '45% busy at 2 PM', '49% busy at 3 PM',
                       '52% busy at 4 PM', '52% busy at 5 PM', '57% busy at 6 PM', '70% busy at 7 PM', '78% busy at 8 PM',
                       '66% busy at 9 PM', '39% busy at 10 PM', '0% busy at 11 PM'],
                       'Monday':  ...
                       }
   }
   '''

Notice we index *results* with zero (``results[0]``), in order to reference the first :py:class:`~gomaps.GoogleMaps` object of the container. From there, one is able to call the :py:meth:`~gomaps.GoogleMaps.get_values` member function of the :py:class:`~gomaps.GoogleMaps` object.

Reason why I have a separate function to get the rest of the attributes is for speed optimization. Upon initialization, a :py:class:`~gomaps.GoogleMaps` object only has the place's *url*, *coordinates*, and *title* attributes.