<a href="https://pypi.org/project/gomaps">
  <img src="https://img.shields.io/pypi/v/gomaps.svg" alt="latest release" />
</a>

# The-Gomaps-Python-Package

Gomaps! A Google Maps API for querying places on Google Maps and scraping the metadata of that search. Results of a query include the following:

* Place Name
* Place Google Maps URL
* Place Address
* Place Coordinates (lattitude/longitude)
* Place Website
* Place Phone Number
* Place Star Rating
* Place Open Hours

There is also another feature within this package that scrapes Google Maps __Popular Times__ data!

<h2><b>Documentation:</b></h2>
<a href="https://gomaps.readthedocs.io/en/latest/">https://gomaps.readthedocs.io/</a>

<h2><b>Quickstart:</b></h2>

To start, import the functions from the `gomaps` package.
```python
from gomaps import maps_search

result = maps_search("Tops Diner") # Returns a list of GoogleMaps objects
# GoogleMapsResults([<gomaps.GoogleMaps object; Place-Name: Tops Diner>])

result[0].get_values() # Populates the object's attributes & returns a dictionary
'''
{
  'title': 'Tops Diner',
  'url': 'https://www.google.com/maps/place/Tops+Diner/@40.7506065,-74.1639023,17z/data=!4m2!3m1!1s0x89c2547b4ec3235b:0x7342f11f69197f92!8m2!3d40.7506065!4d-74.1639023',
  'address': '500 Passaic Ave, East Newark, NJ 07029',
  'coords': ('40.7506065', '-74.1639023'),
  'website': 'https://www.thetopsdiner.com/',
  'phone_number': '(973) 481-0490',
  'rating': '4.6',
  'open_hours': {'Currently': 'Closed - Opens 8AM',
                 'Hours': {'Friday': '8AM–11PM', 'Saturday': '8AM–11PM', 'Sunday': '8AM–11PM',
                           'Monday': '8AM–11PM', 'Tuesday': '8AM–11PM', 'Wednesday': '8AM–11PM', 'Thursday': '8AM–11PM'}
                }
}
'''

from gomaps import popular_times

result = popular_times("Tops Diner", "chromedriver.exe") # See 'Drivers' section below regarding the 'chromedriver.exe' argument
'''
{
  'Sunday': ['0% busy at 6 AM.', '0% busy at 7 AM.', '20% busy at 8 AM.', '34% busy at 9 AM.', '49% busy at 10 AM.',
             '59% busy at 11 AM.', '62% busy at 12 PM.', '56% busy at 1 PM.', '47% busy at 2 PM.', '41% busy at 3 PM.',
             '45% busy at 4 PM.', '57% busy at 5 PM.', '70% busy at 6 PM.', '74% busy at 7 PM.', '66% busy at 8 PM.',
             '47% busy at 9 PM.', '27% busy at 10 PM.', '0% busy at 11 PM.'],
  'Monday': ...
}
'''
```


**Drivers:**

Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it's in your PATH, e. g., place it in /usr/bin or /usr/local/bin.

Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH.

Other supported browsers will have their own drivers available. Links to some of the more popular browser drivers follow. *(Note: PhantomJS is another alternative)*

|          |                                                                       |
|----------|-----------------------------------------------------------------------|
| Chrome:  | https://sites.google.com/a/chromium.org/chromedriver/downloads        |
| Edge:    | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |
| Firefox: | https://github.com/mozilla/geckodriver/releases                       |
| Safari:  | https://webkit.org/blog/6900/webdriver-support-in-safari-10/          |

*source: https://pypi.org/project/selenium/*

# Copyright
Copyright (c) 2020 The Python Packaging Authority. Released under the MIT License.
