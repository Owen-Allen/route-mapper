
import pandas as pd
import json

'''
{
    NUMBER: #, 
    ROUTE:  ordered array[{STOP_ID, NAME, STOP_CODE}, ..] 
    }
'''

def construct_bus_json(route_number, data):

    bus = dict()

    bus["ROUTE_NUMBER"] = route_number

    ordered_list_of_dics = []
    for index, row in data.iterrows():
        cur = dict()
        cur["STOP_ID"] = row["STOP_ID"]
        cur["NAME"] = row["NAME"]
        cur["STOP_CODE"] = row["STOP_CODE"]
        ordered_list_of_dics.append(cur)

    bus["STOPS"] = ordered_list_of_dics

    with open(str(route_number) + ".json", "w") as f:
        json.dump(bus, f)
    

def read_txt(route):
    data = pd.read_csv(str(route) + ".txt", header=None)
    data.columns = ["STOP_ID", "NAME", "STOP_CODE"]
    return data


if __name__ == "__main__":
    d = read_txt(6)
    construct_bus_json(6, d)

    d = read_txt(11)
    construct_bus_json(11, d)

    d = read_txt(14)
    construct_bus_json(14, d)

        