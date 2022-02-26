
import json

import numpy as np
import pandas as pd

import requests

with open('key.json') as f:
    data = json.load(f)
    appID = data["APPLICATION_ID"]
    apiKey = data["APPLICATION_KEY"]


print(appID)
print(apiKey)
query = {"appID": appID, "apiKey" : apiKey, "stopNo" : 6665}
response = requests.get("https://api.octranspo1.com/v2.0/GetNextTripsForStopAllRoutes", params=query)

print(response.json())

    