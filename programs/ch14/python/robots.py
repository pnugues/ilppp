"""
Properties of robots extracted from wikidata
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
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>'''

# Instances of robots
query_instances = '''
SELECT  ?item ?itemLabel 
WHERE
{
     ?item wdt:P31 wd:Q11012. # a robot
     OPTIONAL {
        ?item rdfs:label ?itemLabel 
        FILTER (lang(?itemLabel) = "en") .
    }
}
LIMIT 100'''

# Superclass of robots
query_superclass = '''
SELECT  ?item ?itemLabel 
WHERE 
{
     wd:Q11012 wdt:P279 ?item. # a robot
     OPTIONAL {
        ?item rdfs:label ?itemLabel 
        FILTER (lang(?itemLabel) = "en") .
    }
}
LIMIT 100'''

# Subclasses of robots
query_subclasses = '''
SELECT  ?item ?itemLabel 
WHERE
{
     ?item wdt:P279 wd:Q11012. # a robot
     OPTIONAL {
        ?item rdfs:label ?itemLabel 
        FILTER (lang(?itemLabel) = "en") .
    }
}
LIMIT 100'''

# Parts of robots
query_parts = '''
SELECT  DISTINCT ?item ?itemLabel 
WHERE 
{
     {?item wdt:P361 wd:Q11012.}
     UNION
     {wd:Q11012 wdt:P527 ?item.}
     OPTIONAL {
        ?item rdfs:label ?itemLabel 
        FILTER (lang(?itemLabel) = "en") .
    }
}
LIMIT 100'''

for query in [query_instances, query_superclass, query_subclasses, query_parts]:
    query = prefixes + query
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    # print(data)

    robot = []
    for item in data['results']['bindings']:
        robot.append({
            'item': item.get('item', {}).get('value'),
            'name': item.get('itemLabel', {}).get('value')
        })

    df = pd.DataFrame(robot)
    # print(len(df))
    print(df, '\n')
