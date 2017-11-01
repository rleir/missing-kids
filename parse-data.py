#!/usr/bin/env python
"""This script combines the json files for each year into a single data set"""
import io
import json
import requests

COMBINED_JSON = {}

FILE_INPUT = io.open('missingkids.json')
FILE_RAW = FILE_INPUT.read()
PARSED_JSON = json.loads(FILE_RAW)

# Create a dictionary of all of the cities, states, and magnitude for geocoding
for record in PARSED_JSON['persons']:
    location = record['missingCity'] + ', ' + record['missingState'] + ', USA'
    if not location in COMBINED_JSON:
        COMBINED_JSON[location] = {}
        COMBINED_JSON[location]['magnitude'] = 1
    else:
        COMBINED_JSON[location]['magnitude'] = COMBINED_JSON[location]['magnitude'] + 1

# For each city, call Google API to geocode results
for record in COMBINED_JSON:
    r = requests.get('https://google.com')
    print r.raw
print COMBINED_JSON
with open('parsed-results.json', 'wb') as outfile:
    json.dump(COMBINED_JSON, outfile)
