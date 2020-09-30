"""
Extraction of occupations of Obama from wikidata
__author__ = "Pierre Nugues"
"""
import requests
import pandas as pd

pd.options.display.max_rows = 10000
pd.options.display.max_columns = 80
pd.options.display.width = 200

prefixes = '''PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
'''

# Q22686 Donald Trump
# Q76 Barack Obama
english_query = '''
SELECT DISTINCT ?item ?itemLabelOcc (lang(?itemLabel) as ?lang)
WHERE 
{
    wd:Q76 p:P106 ?occupation .
    ?occupation ps:P106 ?item .
    ?item rdfs:label ?itemLabelOcc .
    FILTER (lang(?itemLabelOcc) = "en") .
}
LIMIT 1000'''

multilingual_query = '''
SELECT DISTINCT ?item ?itemLabelOcc (lang(?itemLabel) as ?lang)
WHERE 
{
    wd:Q76 p:P106 ?occupation .
    ?occupation ps:P106 ?item .
    ?item rdfs:label ?itemLabelOcc . 
}
LIMIT 1000'''

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': prefixes + english_query, 'format': 'json'}).json()
# print(data)

profession = []
for item in data['results']['bindings']:
    profession.append({
        'id': item.get('item', {}).get('value'),
        'occupation': item.get('itemLabelOcc', {}).get('value'),
        'lang': item.get('itemLabelOcc', {}).get('xml:lang'),
    })

df = pd.DataFrame(profession)
print(df)

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': prefixes + multilingual_query, 'format': 'json'}).json()
# print(data)

profession = []
for item in data['results']['bindings']:
    profession.append({
        'id': item.get('item', {}).get('value'),
        'occupation': item.get('itemLabelOcc', {}).get('value'),
        'lang': item.get('itemLabelOcc', {}).get('xml:lang'),
    })

df = pd.DataFrame(profession)
print(df)
