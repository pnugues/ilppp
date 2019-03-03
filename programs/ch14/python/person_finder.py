"""
An example of SPARQL query to find a person in wikidata, by date of birth and death,
tell his/her occupation, and cause of death, if known
"""
__author__ = "Pierre Nugues"

import requests
import pandas as pd
from collections import OrderedDict

pd.options.display.max_rows = 10000
pd.options.display.max_columns = 80
pd.options.display.width = 200

prefixes = '''PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>'''

query = '''
SELECT ?human ?human_label ?dob ?dod ?occ_label ?cod_label
WHERE
{
    ?human wdt:P31 wd:Q5.
    ?human wdt:P569 ?dob. 
    ?human wdt:P570 ?dod.
    FILTER(YEAR(?dob) = 1450).
    FILTER(YEAR(?dod) = 1500).
    OPTIONAL {   
        ?human rdfs:label ?human_label.
        FILTER (lang(?human_label) = "en").
    }
    OPTIONAL {
        ?human wdt:P106 ?occ.
        ?occ rdfs:label ?occ_label.
        FILTER (lang(?occ_label) = "en").
    }
    OPTIONAL {
        ?human wdt:P509 ?cod.
        ?cod rdfs:label ?cod_label.
        FILTER (lang(?cod_label) = "en").
    }
}
LIMIT 100'''

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
data = requests.get(url, params={'query': prefixes + query, 'format': 'json'}).json()

persons = []
for item in data['results']['bindings']:
    persons.append(OrderedDict({
        'id': item['human']['value'],
        'name': item.get('human_label', {}).get('value'),
        'date of birth': item.get('dob', {}).get('value'),
        'date of death': item.get('dod', {}).get('value'),
        'occupation': item.get('occ_label', {}).get('value'),
        'cause of death': item.get('cod_label', {}).get('value')
    }))

df = pd.DataFrame(persons)
print(len(df))
print(df)
