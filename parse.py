import pandas as pd
import json

from Graph import Graph
from Node import Node
from Bus import Bus

from datetime import datetime


ROUTE_NUMBERS = [7, 6, 10, 14]


TRIP_IDS = {
    7: ["83445871-JAN22-JANDA22-Weekday-03", "83445877-JAN22-JANDA22-Weekday-03"],
    6: ["83479758-JAN22-JANDA22-Weekday-04", "83479759-JAN22-JANDA22-Weekday-04"],
    10: ["83480772-JAN22-JANDA22-Weekday-04", "83480774-JAN22-JANDA22-Weekday-04"],
    14: ["83446728-JAN22-JANDA22-Weekday-03", "83447050-JAN22-JANDA22-Weekday-03"]
}


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

def add_extra_paths(G):
    print("ADDING EXTRA PATHS")

    # SUNNYSIDE EXTENSION
    # CONNECT 6683, 6785 6776, 6775, 6773
    sunnyside = [6683, 6785, 6776, 6775, 6773]
    # these nodes already have an edges going the opposite way

    for i in range(0, len(sunnyside) - 1):
        n1 = G.get_node_with_code(sunnyside[i])
        n2 = G.get_node_with_code(sunnyside[i + 1])

        # get the existing weight from n2 to n1
        edge = n2.outgoing_edges[n1]
        # use that weight for the edge from n1 to n2
        n1.add_edge(n2, [edge[0], edge[1]])

    # BANK STREET DETOUR
    # If bank street is very busy, the bus can make a detour
    # From Bank / Gladstone -> Metcalfe / Gladstone -> Metcalfe / Somerset -> Metcalfe / Queen

    # ALL EDGE WEIGHTS WERE FOUND USING GOOGLE MAPS

    bank_gladstone = G.get_node_with_code(8798)
    metcalfe_gladstone = G.get_node_with_code(7672)
    bank_gladstone.add_edge(metcalfe_gladstone, [60, 0])
    metcalfe_gladstone.add_edge(bank_gladstone, [60, 0])



    metcalfe_somerset = Node("METCALFE / SOMSERSET", 1) # this stop doesn't exist
    metcalfe_somerset.pos = (-75.692233, 45.416985)
    G.add_node(metcalfe_somerset)
    metcalfe_gladstone.add_edge(metcalfe_somerset, [60, 0])
    metcalfe_somerset.add_edge(metcalfe_gladstone, [60, 0])


    metcalfe_queen = G.get_node_with_code(1512)
    metcalfe_somerset.add_edge(metcalfe_queen, [120,0])
    metcalfe_queen.add_edge(metcalfe_somerset, [120,0])

def check_path(buses):
    for bus in buses:
        print("in loop")
        if bus.name == "7 St-Laurent":
            print(bus)
            print("NORMAL PATH")
            print(bus.path)
            print("MODIFIED PATH")
            print(bus.modified_path)


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

    add_extra_paths(graph)
    print(buses[0].path)