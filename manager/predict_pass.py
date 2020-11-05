import json
# import predict
from pyorbital.orbital import Orbital
import numpy
import pandas
from datetime import datetime
import time
import threading
# def callback(sid, msg):
#     print("update")
#     tle_dir = msg["tle_dir"]
#     satellites = msg["satellites"] # {"type":"NOAA", "name":"NOAA 15"}
#     max_time = msg["max_time"]     # hours
#     station_location = msg["station_location"] # { "lat" : 0, "lon" : 0, "alt" : 0 }
#     min_elevation = msg["min_elevation"]
#     all_passes = []
#     for sat in satellites:
#         sat_type = sat["type"]
#         sat_name = sat["name"]
#         # orbital = Orbital(sat, tle_file="{}/{}/{}.tle".format(tle_dir, sat_type, sat_name))
#         time_now = datetime.now()
#         # passes = orbital.get_next_passes(time_now, max_time, station_location["lon"], station_location["lat"], station_location["alt"], horizon=min_elevation)

#         all_passes += [{"type":sat_type, "name":sat_name, "rise_time":pas[0], "fall_time":pas[1], "duration":pas[2]} for pas in passes]

def predict_next_passes(tle_dir: str, satellites: dict, station_location: dict, min_elevation: float, for_next_hours: int) -> list:
    all_passes = []
    time_now_utc = datetime.utcnow()

    for sat_name in satellites:
        sat = satellites[sat_name]
        sat_type = sat["type"]

        orbital = Orbital(sat, tle_file="{}/{}/{}.tle".format(tle_dir, sat_type, sat_name))
        passes = orbital.get_next_passes(time_now, for_next_hours, station_location["lon"], station_location["lat"], station_location["alt"], horizon=min_elevation)

        all_passes += [{"type":sat_type, "name":sat_name, "rise_time":pas[0], "fall_time":pas[1], "duration":pas[1] - pas[0]} for pas in passes]
    all_passes.sort(key=lambda t: t["rise_time"])    
    
    return all_passes

def check_datetime(time_to_check: datetime, datetimes: list[datetime]) -> bool:
    return (datetime >= min(datetimes)) and (datetime <= max(datetimes))

def check_datetime2(datetimes_1: list[datetime], datetimes_2: list[datetime]) -> bool:
    return check_datetime(datetimes_1[0], datetimes_2) and check_datetime(datetimes_1[1], datetimes_2) or \
        check_datetime(datetimes_2[0], datetimes_1) and check_datetime(datetimes_2[1], datetimes_1)

def remove_passes_time_colisions(all_passes: list[dict], satellites_d: dict) -> list[dict]:
    filtered_passes = set()

    for i in range(len(all_passes)):
        for j in range(len(all_passes)):
            sat_p_min = min(lambda x: satellites_d[x["name"]]["priority"], [all_passes[i], all_passes[j]])
            if check_datetime2([all_passes[i]["rise_time"], all_passes[i]["fall_time"]], [all_passes[j]["rise_time"], all_passes[j]["fall_time"]]):
                filtered_passes.add(sat_p_min)
            else:
                filtered_passes.add(all_passes[i])
                filtered_passes.add(all_passes[j])


    return sorted(list(filtered_passes), key=lambda t: t["rise_time"])

def get_passes_of_sat_type(all_passes: list[dict], sat_type: str) -> list[dict]:
    ans = list(filter(lambda t: t["type"] == sat_type, all_passes))
    return ans

def get_passes_of_sat_name(all_passes: list[dict], sat_name: str) -> list[dict]:
    ans = list(filter(lambda t: t["name"] == sat_name, all_passes))
    return ans

def do_predict(tle_dir: str, satellites: dict, station_location: dict, min_elevation: float, for_next_hours: int, prev_predict: list = []) -> list[dict]:
    st_time = time.time()
    ans = [] + prev_predict
    ans += predict_next_passes(tle_dir, satellites, station_location, min_elevation, for_next_hours)
    ans = remove_passes_time_colisions(ans, satellites)

    print("predicted", len(ans), "passes of", len(satellite.items()), "satellites" f"in {time.time()-st_time}s.")
    return ans


