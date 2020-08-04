import pyppdf.patch_pyppeteer
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

session = HTMLSession()
##url = "https://www.google.com/maps/place/Tops+Diner/@40.7506065,-74.166091,17z/data=!4m5!3m4!1s0x89c2547b4ec3235b:0x7342f11f69197f92!8m2!3d40.7506065!4d-74.1639023"
##url = "https://finance.yahoo.com/quote/NFLX/options?p=NFLX"
##url = "https://www.google.com/maps?q=Tops+Diner"
url = "https://www.google.com/search?q=Tops+Diner"

r = session.get(url)
r.html.render()
#resp = requests.get(url)

with open("test2.html", 'w', encoding="utf-8") as f:
   f.write(str(r.html.html))
