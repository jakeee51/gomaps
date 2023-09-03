<a href="https://pypi.org/project/gomaps">
  <img src="https://img.shields.io/pypi/v/gomaps.svg" alt="latest release" />
</a>

<a href="https://pepy.tech/project/gomaps">
  <img src="https://static.pepy.tech/badge/gomaps" />
</a>

<a href="https://gomaps.readthedocs.io/en/latest/">
  <img src="https://readthedocs.org/projects/gomaps/badge/" />
</a>

<a href="https://travis-ci.com/github/jakeee51/gomaps">
  <img src="https://travis-ci.com/jakeee51/gomaps.svg?branch=master&status=passed" />
</a>

# The-Gomaps-Python-Package

Gomaps! A Google Maps web scraper for querying places on Google Maps and scraping the metadata of that search (No API key needed). This package also does geocoding, reverse geocoding and address validation! It's essentially a lite version of the Google Maps Places API. Results of a query include the following:

* Place Name
* Place Google Maps URL
* Place Address
* Place Coordinates (lattitude/longitude)
* Place Website
* Place Phone Number
* Place Star Rating
* Place Open Hours
* Place Popular Times

That's right! This can also scrape Google Maps __Popular Times__ data!
For more information about Google's popular times data, refer to this support post: https://support.google.com/business/answer/6263531?hl=en.

<h2><b>Documentation:</b></h2>
<a href="https://gomaps.readthedocs.io/en/latest/">https://gomaps.readthedocs.io/en/latest/</a>

<h2><b>Quickstart:</b></h2>
To start, import the functions from the *gomaps* package.

```python
from gomaps import maps_search

results = maps_search("Tops Diner") # Returns a list of GoogleMaps objects
# GoogleMapsResults([<gomaps.GoogleMaps object; Place-Name: Tops Diner>])

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
```

# Copyright
Copyright (c) 2024 The Python Packaging Authority. Released under the MIT License.
