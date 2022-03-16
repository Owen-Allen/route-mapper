import pandas as pd
import json

from Graph import Graph
from Node import Node
from Bus import Bus

from datetime import datetime

# ROUTE_NUMBERS = [6, 7, 10, 11, 14]


ROUTE_NUMBERS = [7, 6, 10, 14]


ROUTE_DIRECTIONS = {
    # 5: ["Billings Bridge", "Rideau"],
    # 6: ["Rockcliffe", "Greenboro"],
    # 7: ["St-Laurent", "Carleton"],
    # 10: ["Hurdman", "Lyon"],
    # 11: ["Parliament ~ Parlement", "Bayshore"],
    # 14: ["Tunney's Pasture", "St-Laurent"],
    # 15: ["Parliament ~ Parlement", "Blair"]
}
# 7667 Bank Flora
# 8798 Bank Gladstone
# 7665 BANK / GILMOUR
# 2484,"BANK / GLOUCESTER"

TRIP_IDS = {
    7: ["83445871-JAN22-JANDA22-Weekday-03", "83445877-JAN22-JANDA22-Weekday-03"],
    6: ["83479758-JAN22-JANDA22-Weekday-04", "83479759-JAN22-JANDA22-Weekday-04"],
    10: ["83480772-JAN22-JANDA22-Weekday-04", "83480774-JAN22-JANDA22-Weekday-04"],
    14: ["83446728-JAN22-JANDA22-Weekday-03", "83447050-JAN22-JANDA22-Weekday-03"]
}

# TRIP_IDS = {
#     7: [83445871, 83445877], 
#     6: [83479758, 83479759],
#     10: [83480772, 83480774]
# }


df_stops = pd.read_csv("data/google_transit/stops.txt") # USED TO GATHER STOP NAME AND STOP CODE

def get_stop_name_and_code(stop):
    return df_stops.loc[df_stops["stop_id"] == stop["stop_id"]]["stop_name"].iloc[0], df_stops.loc[df_stops["stop_id"] == stop["stop_id"]]["stop_code"].iloc[0]

def get_stop_location(stop):
    lat = df_stops.loc[df_stops["stop_id"] == stop["stop_id"]]["stop_lat"].iloc[0]
    lon = df_stops.loc[df_stops["stop_id"] == stop["stop_id"]]["stop_lon"].iloc[0]
    return (lon, lat)

def create_nodes_from_stops(stops_for_trip, G):
    bus_path = []
    for index, cur_stop in stops_for_trip.iterrows():
        if index == stops_for_trip.index[-1]: # last stop
            # print("LAST")
            break
        else:
            next_stop = stops_for_trip.loc[index + 1]

            cur_name, cur_code = get_stop_name_and_code(cur_stop)
            cur_node = G.get_node(cur_name, cur_code)

            next_name, next_code = get_stop_name_and_code(next_stop)
            next_node = G.get_node(next_name, next_code)

            if cur_node is None:
                cur_node = Node(name=cur_name, code=cur_code)
                cur_node.pos = get_stop_location(cur_stop)
                G.add_node(cur_node)

            if cur_node not in bus_path:
                bus_path.append(cur_node)

            if next_node is None:
                next_node = Node(name=next_name, code=next_code)
                G.add_node(next_node)
                next_node.pos = get_stop_location(next_stop)
            
            # if next_node not in bus_path:
            #     bus_path.append(next_node)
        
            if cur_node.code != next_node.code: # no self loops
                d1 = datetime.strptime(cur_stop["departure_time"], "%H:%M:%S")
                d2 = datetime.strptime(next_stop["departure_time"], "%H:%M:%S")

                dif = d2 - d1
                edge_weight = dif.seconds

                if(edge_weight == 0):
                    edge_weight = 30

                if "BANK" in cur_name or "SOMERSET" in cur_name:
                    # CONGESTION AFFECTED PATH
                    cur_node.add_edge(next_node, [lambda x: edge_weight +(x * edge_weight / 5), 0])
                else:
                    cur_node.add_edge(next_node, [edge_weight, 0])
    return bus_path

def construct_g_b():
    G = Graph()
    buses = []

    df_trips = pd.read_csv("data/google_transit/trips.txt")
    df_stop_times = pd.read_csv("data/google_transit/stop_times.txt")

    for route in ROUTE_NUMBERS:
        for trip_id in TRIP_IDS[route]:  # 7 Carleton vs 7 St-Laurent
            trip = df_trips.loc[df_trips['trip_id'] == trip_id].iloc[0]
            bus = Bus(name = f"{route} {trip['trip_headsign']}")

            print(f"{route} {trip['trip_headsign']}")

            stops_for_trip = df_stop_times.loc[df_stop_times["trip_id"] == trip_id]
            
            path_codes = []

            bus_path = create_nodes_from_stops(stops_for_trip, G)
            bus.set_path(bus_path)

            if route != 14:
                buses.append(bus)
    
    return G, buses


def construct_graph_and_buses():
    G = Graph()
    buses = []

    df_trips = pd.read_csv("data/google_transit/trips.txt")

    df_stop_times = pd.read_csv("data/google_transit/stop_times.txt")

    for route in ROUTE_NUMBERS:
        for direction in ROUTE_DIRECTIONS[route]:  # 7 Carleton vs 7 St-Laurent
            print(f"{route} {direction}")
            trip = \
                df_trips.loc[
                    (df_trips['route_id'] == str(route) + "-332") & (df_trips['trip_headsign'] == direction)].iloc[
                    0]
            trip_id = trip.at["trip_id"]

            trip_stops = df_stop_times.loc[df_stop_times['trip_id'] == trip_id]
            
            bus = Bus(name= str(route) + trip.at["trip_headsign"])
            path = []
            for i in trip_stops.index:

                if i != trip_stops.index[len(trip_stops.index) - 1]: # not at last stop
                    # Create node i and node i + 1 if not already created
                    id_1 = df_stop_times.loc[i].at["stop_id"]
                    n1 = G.get_node_with_id(id_1)
                    if n1 is None:
                        n1 = Node(name=id_1, id=id_1)
                        G.add_node(n1)

                    id_2 = df_stop_times.loc[i + 1].at["stop_id"]
                    n2 = G.get_node_with_id(id_2)
                    if n2 is None:
                        n2 = Node(name=id_2, id=id_2)
                        G.add_node(n2)

                    d1 = datetime.strptime(df_stop_times.loc[i].at["departure_time"], "%H:%M:%S")
                    d2 = datetime.strptime(df_stop_times.loc[i + 1].at["departure_time"], "%H:%M:%S")

                    dif = d2 - d1
                    edge_weight = dif.seconds

                    if edge_weight == 0:
                        edge_weight = 30

                    n1.add_edge(n2, [edge_weight, 0])

                    # bus.add_node_to_path(n1)
                    # bus.add_node_to_path(n2)

                    path.append(n1)
                else:
                    id = df_stop_times.loc[i].at["stop_id"]
                    print("IN ELSE")
                    print(trip_id)
                    print(id)
                    n = G.get_node_with_id(id)
                    path.append(n)
            
            # print(f"this is the path {path}")
            bus.set_path(path)
            buses.append(bus)
            # print(bus)
            break
    return G, buses


def compute_node_edges(G, routes, buses):
    # Use the bus number (7 -> 7-332) to get a trip_id from trips.txt
    #               EX 7-322 -> 83446041
    # Now with that trip_id parse stop_times.txt to get the time of arrival for each stop
    # We can use the difference in the time of arrival to calculate the edge weights.

    df_trips = pd.read_csv("data/google_transit/trips.txt")

    df_stop_times = pd.read_csv("data/google_transit/stop_times.txt")

    nodes = G.get_nodes()

    for route in routes:  # construct a graph using the routes of all buses
        bus = Bus(str(route["route_number"]))

        trip = df_trips.loc[df_trips['route_id'] == str(route["route_number"]) + "-332"].iloc[0]
        trip_id = trip.loc["trip_id"]

        print(trip_id)

        trip_stops = df_stop_times.loc[df_stop_times['trip_id'] == trip_id]
        for index in trip_stops.index:  # the stop at index connects to stop at index + 1
            if index == trip_stops.index[len(trip_stops.index) - 1]:  # if we're at the end of the array
                # avoids out of bounds
                last_stop_id = df_stop_times.loc[index].at["stop_id"]
                last_stop = G.get_node_with_id(last_stop_id)
                if last_stop:
                    bus.add_node_to_path(last_stop)
                else:
                    print(f"Could not find last stop for bus {bus.name}")
            else:
                d1 = datetime.strptime(df_stop_times.loc[index].at["departure_time"], "%H:%M:%S")
                d2 = datetime.strptime(df_stop_times.loc[index + 1].at["departure_time"], "%H:%M:%S")

                dif = d2 - d1
                edge_weight = dif.seconds // 60
                # Get those nodes from the graph
                from_node = G.get_node_with_id(df_stop_times.loc[index].at["stop_id"])
                to_node = G.get_node_with_id(df_stop_times.loc[index + 1].at["stop_id"])

                if from_node is None:
                    print("THIS SHOULD NEVER HAPPEN, YOUR GRAPH G HASN'T CREATED THE from_node FOR THIS STOP")
                if to_node is None:
                    print("THIS SHOULD NEVER HAPPEN, YOUR GRAPH G HASN'T CREATED THE to_node FOR THIS STOP")

                from_node.add_edge(to_node, [edge_weight, 0])
                bus.add_node_to_path(from_node)

        buses.append(bus)




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

    with open("data/" + str(route_number) + ".json", "w") as f:
        json.dump(bus, f)



def name_stops(g):
    df_stops = pd.read_csv("data/google_transit/stops.txt")
    for node in g.get_nodes():
        stop_name = df_stops.loc[df_stops['stop_id'] == node.id].iloc[0].at["stop_name"]
        node.id = stop_name
        node.name = stop_name



if __name__ == "__main__":
    graph, buses = construct_g_b()


    # for bus in buses:
        # print(bus)
        # for node in bus.path:
            # print(f"{node}, edges {node.outgoing_edges}")

    for node in graph.nodes:
        if len(node.outgoing_edges) == 0:
            print(node.name)




    # name_stops(g)

    # print("done creating buses")

    # for bus in b:
    #     print(bus)
    #     print(bus.path)

    # for node in g.get_nodes():
    #     print(node.id)


    

    # construct_bus_json(6)

    # construct_bus_json(7)

    # construct_bus_json(11)

    # construct_bus_json(14)
