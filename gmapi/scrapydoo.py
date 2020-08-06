# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: busytimes
Functionality Purpose: Web scrape Google Maps Popular Times data
Version: Beta
'''
#8/6/20

from openpyxl import Workbook, load_workbook
from datetime import datetime
from urllib.request import urlopen, urlparse, urlretrieve
from urllib.parse import quote_plus, unquote_plus
import GeoLiberator as GL
import re
import pandas as pd
import os
import time
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
