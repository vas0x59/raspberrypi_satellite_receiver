import json
# import predict
from pyorbital.orbital import Orbital
# import numpy
# import pandas
from datetime import datetime
import time
import threading
import socketio
from typing import *

sio = socketio.Client()

def predict_next_passes(tle_dir: str, satellites: dict, station_location: dict, min_elevation: float, for_next_hours: int) -> list:
    all_passes = []
    time_now_utc = datetime.utcnow()

    for sat_name in satellites:
        sat = satellites[sat_name]
        sat_type = sat["type"]

        orbital = Orbital(sat_name, tle_file="{}/{}/{}.tle".format(tle_dir, sat_type, sat_name))
        passes = orbital.get_next_passes(time_now_utc, for_next_hours, station_location["lon"], station_location["lat"], station_location["alt"], horizon=min_elevation)

        all_passes += [{"type": sat_type, "name": sat_name, "rise_time": pas[0], "fall_time": pas[1], "duration": (pas[1] - pas[0]).total_seconds()} for pas in passes]
    all_passes.sort(key=lambda t: t["rise_time"])

    return all_passes


def check_datetime(time_to_check: datetime, datetimes: List[datetime]) -> bool:
    return (time_to_check >= min(datetimes)) and (time_to_check <= max(datetimes))


def check_datetime2(datetimes_1: List[datetime], datetimes_2: List[datetime]) -> bool:
    return check_datetime(datetimes_1[0], datetimes_2) and check_datetime(datetimes_1[1], datetimes_2) or \
        check_datetime(datetimes_2[0], datetimes_1) and check_datetime(datetimes_2[1], datetimes_1)


def remove_passes_time_colisions(all_passes: List[dict], satellites_d: dict) -> List[dict]:
    filtered_passes = []

    for i in range(len(all_passes)):
        for j in range(len(all_passes)):
            sat_p_min = min([all_passes[i], all_passes[j]], key=lambda x: satellites_d[x["name"]]["priority"])
            if check_datetime2([all_passes[i]["rise_time"], all_passes[i]["fall_time"]], [all_passes[j]["rise_time"], all_passes[j]["fall_time"]]):
                if sat_p_min not in filtered_passes:
                    filtered_passes.append(sat_p_min)
            else:
                if all_passes[i] not in filtered_passes:
                    filtered_passes.append(all_passes[i])
                if all_passes[j] not in filtered_passes:
                    filtered_passes.append(all_passes[j])
    return sorted(list(filtered_passes), key=lambda t: t["rise_time"])


def get_passes_of_sat_type(all_passes: List[dict], sat_type: str) -> List[dict]:
    ans = list(filter(lambda t: t["type"] == sat_type, all_passes))
    return ans


def get_passes_of_sat_name(all_passes: List[dict], sat_name: str) -> List[dict]:
    ans = list(filter(lambda t: t["name"] == sat_name, all_passes))
    return ans


def correct_for_json(ans: List[dict]) -> List[dict]:
    ans_s = list()
    for a in ans:
        el = a
        el["rise_time"] = str(el["rise_time"])
        el["fall_time"] = str(el["fall_time"])
        # el["duration"] = str(el["duration"])
        ans_s.append(el)
    return ans_s


def correct_from_json(ans: List[dict]) -> List[dict]:
    ans_s = list()
    for a in ans:
        el = a
        el["rise_time"] = datetime.fromisoformat(el["rise_time"])
        el["fall_time"] = datetime.fromisoformat(el["fall_time"])
        # el["duration"] = datetime.fromisoformat(el["duration"])
        ans_s.append(el)
    return ans_s


def do_predict(tle_dir: str, satellites: dict, station_location: dict, min_elevation: float, for_next_hours: int, prev_predict: list = []) -> List[dict]:
    st_time = time.time()
    ans = [] + prev_predict
    ans += predict_next_passes(tle_dir, satellites, station_location, min_elevation, for_next_hours)
    ans.sort(key=lambda t: t["rise_time"])
    ans = remove_passes_time_colisions(ans, satellites)

    print("predicted", len(ans), "passes of", len(satellites.items()), "satellites", f"in {time.time()-st_time}s.")
    return ans


@sio.on("predict", namespace="/predict_pass")
def callback(msg):
    print("callback")
    tle_dir = msg["tle_directory"]
    satellites = msg["satellites"]
    station_location = msg["station_location"]
    min_elevation = msg["min_elevation"]
    for_next_hours = msg["for_next_hours"]
    prev_predict = correct_from_json(msg["prev_predict"])
    print(msg)
    ans = correct_for_json(do_predict(tle_dir, satellites, station_location, min_elevation, for_next_hours, prev_predict))
    sio.emit("predict_ans", {"ans": ans, "tle_dir": tle_dir, "last_update_datetime": str(datetime.utcnow())},
             namespace="/predict_pass")


@sio.event
def connect():
    print("I'm connected!")


sio.connect("http://localhost:5000", namespaces=["/predict_pass"])
sio.wait()