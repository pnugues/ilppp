"""
Extraction of Busan population
"""
__author__ = "Pierre Nugues"

import requests
import pandas as pd

pd.options.display.max_rows = 10000
pd.options.display.max_columns = 80
pd.options.display.width = 200

query = '''prefix dbo:	<http://dbpedia.org/ontology/>
prefix foaf:	<http://xmlns.com/foaf/0.1/>

SELECT ?entity ?population
WHERE
{
  ?entity foaf:name "Busan Metropolitan City"@en.
  ?entity dbo:populationTotal ?population.
}'''

url = 'https://dbpedia.org/sparql'
data = requests.get(url, params={'query': query, 'format': 'json'}).json()

population = []
for item in data['results']['bindings']:
    # print(item)
    population.append({
        'entity': item['entity']['value'],
        'population': item.get('population', {}).get('value')})

df = pd.DataFrame(population)
print(len(df))
print(df)
