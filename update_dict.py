#!/usr/bin/env python3

import json
import requests

url = "https://docs.google.com/spreadsheets/d/1Dy-gQNEYOOk2yKbq_IaX8T24ygRfksAcf1aiuMS5S40/export?format=tsv"

result = {}
response = requests.get(url)
for row in response.text.split("\n")[1:]:
    code, ch1, ch2, ch3, ch4, desc = row.strip().split("\t")
    if not code:
        continue
    result[code[1:-1]] = [ch1, ch2, ch3, ch4]

with open("scctools/eia608codes.py", "w") as f:
    f.write("EIA608CODES = " + json.dumps(result, indent=4))
