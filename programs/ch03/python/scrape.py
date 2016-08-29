"""
Downloading a Wikipedia page
"""
__author__ = "Pierre Nugues"
import requests

url_en = 'https://en.wikipedia.org/wiki/Aristotle'
url_fr = 'https://fr.wikipedia.org/wiki/Aristote'
html_doc = requests.get(url_en).text
print(html_doc)
