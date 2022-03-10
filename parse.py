
import pandas as pd
import json


from Graph import Graph
from Node import Node
from Bus import Bus

from datetime import datetime

'''
{
    NUMBER: #, 
    ROUTE:  ordered array[{STOP_ID, NAME, STOP_CODE}, ..] 
    }
'''

ROUTE_NUMBERS = [6,7,11,14]

def compute_node_edges(G, routes, buses):
    # Use the bus number (7 -> 7-332) to get a trip_id from trips.txt
    #               EX 7-322 -> 83446041
    # Now with that trip_id parse stop_times.txt to get the time of arrival for each stop
    # We can use the difference in the time of arrival to calculate the edge weights.

    df_trips = pd.read_csv("data/google_transit/trips.txt")

    df_stop_times = pd.read_csv("data/google_transit/stop_times.txt")

    nodes = G.get_nodes()

    for route in routes: # construct a graph using the routes of all buses
        bus = Bus(route["route_number"])

        trip = df_trips.loc[df_trips['route_id'] == str(route["route_number"]) + "-332"].iloc[0]
        trip_id = trip.loc["trip_id"]

        trip_stops = df_stop_times.loc[df_stop_times['trip_id'] == trip_id]
        for index in trip_stops.index: # the stop at index connects to stop at index + 1
            if index == trip_stops.index[len(trip_stops.index) - 1]: # if we're at the end of the array
                # avoids out of bounds
                last_stop_id = df_stop_times.loc[index].at["stop_id"]
                last_stop = G.get_node_with_id(last_stop_id)
                if last_stop:
                    bus.add_destination(last_stop)
                else:
                    print(f"Could not find last stop for bus {bus.name}")
            else:
                d1 = datetime.strptime(df_stop_times.loc[index].at["departure_time"], "%H:%M:%S")
                d2 = datetime.strptime(df_stop_times.loc[index + 1].at["departure_time"], "%H:%M:%S")

                dif = d2 - d1
                edge_weight = dif.total_seconds()
                if(edge_weight == 0): # LIAR
                    # print("round up to 30 seconds? not sure what to do here")
                    edge_weight = 30
                
                # Get those nodes from the graph
                from_node = G.get_node_with_id(df_stop_times.loc[index].at["stop_id"])
                to_node = G.get_node_with_id(df_stop_times.loc[index + 1].at["stop_id"])

                if from_node == None:
                    print("THIS SHOULD NEVER HAPPEN, YOUR GRAPH G HASNT CREATED THE from_node FOR THIS STOP")
                if to_node == None:
                    print("THIS SHOULD NEVER HAPPEN, YOUR GRAPH G HASNT CREATED THE to_node FOR THIS STOP")

                from_node.add_edge(to_node, edge_weight)
                bus.add_destination(from_node)
            
            buses.append(bus)
                            

        # Now we can iterate through all of the stops in stop_times.txt that serve this trip
        # and use their scheduled times to compute the travel cost




def construct_empty_nodes(G, routes):
    set_already_added = set() # multiple buses can share a stop.  Don't create that stop twice.

    for bus in routes:
        for stop in bus["stops"]:
            if stop["stop_id"] not in set_already_added:
                node = Node(stop["name"], stop["stop_id"])
                set_already_added.add(stop["stop_id"])
                G.add_node(node)


def construct_bus_json(route_number):
    
    data = pd.read_csv("data/txt/" + str(route_number) + ".txt", header=None)
    data.columns = ["stop_id", "name", "stop_code"]

    bus = dict()
    bus["route_number"] = route_number

    ordered_list_of_dics = []
    for index, row in data.iterrows():
        cur = dict()
        cur["stop_id"] = row["stop_id"]
        cur["name"] = row["name"]
        cur["stop_code"] = row["stop_code"]
        ordered_list_of_dics.append(cur)
        print(cur)
        break

    bus["stops"] = ordered_list_of_dics

    with open("data/" +str(route_number) + ".json", "w") as f:
        json.dump(bus, f)

def construct_graph_and_buses():
    routes = []
    buses = []
    for route_num in ROUTE_NUMBERS:
        with open("data/" + str(route_num) + ".json", "r") as f:
            routes.append(json.load(f))
    
    G = Graph()
    construct_empty_nodes(G, routes)
    compute_node_edges(G, routes, buses)        

    return G, buses
    


if __name__ == "__main__":
    
    construct_graph_and_buses()

    # construct_bus_json(6)

    # construct_bus_json(7)

    # construct_bus_json(11)

    # construct_bus_json(14)

        