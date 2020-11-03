import json
# import predict
from pyorbital.orbital import Orbital
import numpy
import pandas
from datetime import datetime

# def callback(sid, msg):
#     print("update")
#     tle_dir = msg["tle_dir"]
#     satellites = msg["satellites"] # {"type":"NOAA", "name":"NOAA 15"}
#     max_time = msg["max_time"]     # hours
#     station_location = msg["station_location"] # { "lat" : 0, "lon" : 0, "alt" : 0 }
#     min_elevation = msg["min_elevation"]
#     all_transitions = []
#     for sat in satellites:
#         sat_type = sat["type"]
#         sat_name = sat["name"]
#         # orbital = Orbital(sat, tle_file="{}/{}/{}.tle".format(tle_dir, sat_type, sat_name))
#         time_now = datetime.now()
#         # passes = orbital.get_next_passes(time_now, max_time, station_location["lon"], station_location["lat"], station_location["alt"], horizon=min_elevation)

#         all_transitions += [{"type":sat_type, "name":sat_name, "rise_time":pas[0], "fall_time":pas[1], "duration":pas[2]} for pas in passes]

def predict_next_passes(tle_dir: str, satellites: list[dict], station_location: dict, min_elevation: float, for_next_hours: int) -> list:
    all_transitions = []
    time_now_utc = datetime.utcnow()

    for sat in satellites:
        sat_type = sat["type"]
        sat_name = sat["name"]

        orbital = Orbital(sat, tle_file="{}/{}/{}.tle".format(tle_dir, sat_type, sat_name))
        passes = orbital.get_next_passes(time_now, for_next_hours, station_location["lon"], station_location["lat"], station_location["alt"], horizon=min_elevation)

        all_transitions += [{"type":sat_type, "name":sat_name, "rise_time":pas[0], "fall_time":pas[1], "duration":pas[1] - pas[0]} for pas in passes]
        
    
    return all_transitions

