"""
Extraction of cat names, replicating an example from https://query.wikidata.org/
"""
__author__ = "Pierre Nugues"

import requests
import pandas as pd

pd.options.display.max_rows = 10000
pd.options.display.max_columns = 80
pd.options.display.width = 200

prefixes = '''PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>'''

query = '''
SELECT ?entity ?population 
WHERE 
{
  ?entity rdfs:label "Busan"@en .
  ?entity wdt:P1082 ?population.

}'''

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': prefixes + query, 'format': 'json'}).json()

# print(data)
cities = []
for item in data['results']['bindings']:
    # print(item)
    cities.append({
        'id': item['entity']['value'],
        'name': item.get('population', {}).get('value')})

df = pd.DataFrame(cities)
print(len(df))
print(df)
