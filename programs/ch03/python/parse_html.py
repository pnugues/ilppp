"""
Parse a Wikipedia page
"""
__author__ = "Pierre Nugues"

import bs4
import requests
from urllib.parse import urljoin

url_en = 'https://en.wikipedia.org/wiki/Aristotle'
html_doc = requests.get(url_en).text
parse_tree = bs4.BeautifulSoup(html_doc, 'html.parser')

print(parse_tree.title)
# <title>Aristotle - Wikipedia, the free encyclopedia</title>
print(parse_tree.title.text)
# Aristotle - Wikipedia, the free encyclopedia
print(parse_tree.h1.text)
# Aristotle

headings = parse_tree.find_all('h2')
print([heading.text for heading in headings])
# ['Contents', 'Life', 'Thought', 'Loss and preservation of his works', 'Legacy', 'List of works', 'Eponyms', 'See also', 'Notes and references', 'Further reading', 'External links', 'Navigation menu']

# We extract the links
links = parse_tree.find_all('a', href=True)

# The labels
print([link.text for link in links])
# The links
print([link.get('href') for link in links])
# The absolute addresses
try:
    print([urljoin(url_en, link['href']) for link in links])
except Exception as ex:
    print(type(ex))
