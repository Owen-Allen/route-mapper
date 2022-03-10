
import json

import numpy as np
import pandas as pd

import requests



with open('../key.json') as f:
    data = json.load(f)
    appID = data["APPLICATION_ID"]
    apiKey = data["APPLICATION_KEY"]


def compute_time_between_stops(STOP1, STOP2):
    return


def query_stop(STOP_CODE):
    global appID, apiKey
    query = {"appID": appID, "apiKey" : apiKey, "stopNo" : STOP_CODE}
    response = requests.get("https://api.octranspo1.com/v2.0/GetNextTripsForStop", params=query).json()

    with open("test.json", "w") as f:
        json.dump(response, f)
    return response



if __name__ == "__main__":
    print(query_stop(8789))
    print(query_stop(7024))


