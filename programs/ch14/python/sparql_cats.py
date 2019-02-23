"""
Extraction of cat names, replicating an example from https://query.wikidata.org/
"""
__author__ = "Pierre Nugues"

import requests
import pandas as pd

pd.options.display.max_rows = 10000
pd.options.display.max_columns = 80
pd.options.display.width = 200

query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?item ?itemLabel WHERE {
    ?item wdt:P31 wd:Q146 .

    OPTIONAL {
        ?item rdfs:label ?itemLabel 
        filter (lang(?itemLabel) = "en") .
    }
}'''

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': query, 'format': 'json'}).json()

# print(data)
cats = []
for item in data['results']['bindings']:
    # print(item)
    cats.append({
        'id': item['item']['value'],
        'name': item.get('itemLabel', {}).get('value')})

df = pd.DataFrame(cats)
print(len(df))
print(df)
