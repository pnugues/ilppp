"""
Extraction of occupations from wikidata
__author__ = "Pierre Nugues"
"""
import requests
import pandas as pd

pd.options.display.max_rows = 10000
pd.options.display.max_columns = 80
pd.options.display.width = 200

query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?item ?itemLabel ?_subclass_of ?_subclass_ofLabel
WHERE {
  ?item wdt:P31 wd:Q28640; # instance of Profession
        wdt:P279 ?_subclass_of. # subclass of
  OPTIONAL {
    ?item rdfs:label ?itemLabel filter (lang(?itemLabel) = "sv") .
  }
  OPTIONAL {
    ?_subclass_of rdfs:label ?_subclass_ofLabel filter (lang(?_subclass_ofLabel) = "sv") .
  }
}'''

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': query, 'format': 'json'}).json()

profession = []
for item in data['results']['bindings']:
    profession.append({
        'id': item['item']['value'],
        'name': item.get('itemLabel', {}).get('value'),
        'subclass': item.get('_subclass_ofLabel', {}).get('value')})

df = pd.DataFrame(profession)
print(len(df))
print(df)
