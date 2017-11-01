#!/usr/bin/env python
"""This script combines the json files for each year into a single data set"""
import io
import json
import requests

COMBINED_JSON = {}
GEOCODED_JSON = {}
URL_BASE = 'https://maps.google.com/maps/api/geocode/json'
API_KEY = 'AIzaSyCGpG15mvCafMGJ-ujhMGolgOXr_YoabUQ'

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
for record, value in COMBINED_JSON.iteritems():
    params = {
        'key': API_KEY,
        'address': record
    }
    r = requests.get(URL_BASE, params)
    result = r.json()['results'][0]['geometry']['location']

    GEOCODED_JSON[record] = {}
    GEOCODED_JSON[record]['magnitude'] = value['magnitude']
    GEOCODED_JSON[record]['latitude'] = result['lat']
    GEOCODED_JSON[record]['longitude'] = result['lng']

print GEOCODED_JSON
with open('parsed-results.json', 'wb') as outfile:
    json.dump(GEOCODED_JSON, outfile)
