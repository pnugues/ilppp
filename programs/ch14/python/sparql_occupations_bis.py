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

SELECT DISTINCT ?occupation ?itemLabelOcc
WHERE {
  ?item  wdt:P31 wd:Q5 .
  ?item wdt:P106 ?occupation .
  OPTIONAL {
    ?occupation rdfs:label ?itemLabelOcc filter (lang(?itemLabelOcc) = "en") .
  }  
}
LIMIT 1000'''

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': query, 'format': 'json'}).json()

profession = []
for item in data['results']['bindings']:
    profession.append({
        'id': item.get('occupation', {}).get('value'),
        'occupation': item.get('itemLabelOcc', {}).get('value')})

df = pd.DataFrame(profession)
print(len(df))
print(df)
