
import json

import numpy as np
import pandas as pd

import requests

# with open('../key.json') as f:
#     data = json.load(f)
#     appID = data["APPLICATION_ID"]
#     apiKey = data["APPLICATION_KEY"]


# print(appID)
# print(apiKey)
# query = {"appID": appID, "apiKey" : apiKey, "stopNo" : 6655}
# response = requests.get("https://api.octranspo1.com/v2.0/GetNextTripsForStop", params=query).json()

# with open("14.json", "w") as f:
#     json.dump(response, f)

# print(response.json())

def get_stop_id(filename):
    text = ""
    with open(filename, 'r') as f:
        text = f.read()
    print(text)


if __name__ == "__main__":
    parsetxt("7.txt")

