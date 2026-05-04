import urllib.request
import urllib.parse
import json

query = """
SELECT ?festival ?festivalLabel ?date ?bandLabel WHERE {
  ?festival wdt:P361 wd:Q1137962.
  ?festival p:P710 ?statement.
  ?statement ps:P710 ?band.
  OPTIONAL { ?statement pq:P585 ?date. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 20
"""
url = "https://query.wikidata.org/sparql?query=" + urllib.parse.quote(query) + "&format=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        for result in data["results"]["bindings"]:
            print(result.get("festivalLabel", {}).get("value"), " | ", 
                  result.get("bandLabel", {}).get("value"), " | ", 
                  result.get("date", {}).get("value"))
except Exception as e:
    print(e)
