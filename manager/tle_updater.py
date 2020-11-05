import requests
import json
from datetime import datetime
import time
# import sched
# import http
import socketio
from typing import *
import os
import sys

sio = socketio.Client()

def creat_prev_folders(path: str):
    path_folder = "/".join(path.split("/")[:-1])
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)

def download_tle(tle_sources: List[str], tle_dir: str):
    concatenated_content = ""
    for tle_source in tle_sources:
        r = requests.get(tle_source, allow_redirects=True)
        tle_source_name = tle_source.split("/")[-1].split(".")[0] + ".tle"
        tle_source_file_name = tle_dir + "/original/" + tle_source_name
        str_content = r.content.decode()
        concatenated_content += str_content
        creat_prev_folders(tle_source_file_name)
        open(tle_source_file_name, "w").write(str_content)
    # creat_prev_folders(tle_source_file_name)
    open(tle_dir + "/all.tle", "w").write(concatenated_content)
    


def split_tle_for_satellites(satellites: List[dict], tle_dir: str):
    """
    <tle_dir>/<satellite type>/<satellite name>.tle
    """
    concatenated_content = open(tle_dir + "/all.tle", "r").readlines()
    all_sat_tle = {}
    current_sat = ""
    for i in range(len(concatenated_content)):
        line = concatenated_content[i]
        if i % 3 == 0:
            current_sat = line.strip()
            all_sat_tle[current_sat] = line
        elif current_sat in all_sat_tle.keys():
            all_sat_tle[current_sat] += line


    for satellite in satellites:
        sat_name = satellite["name"].strip()
        sat_type = satellite["type"]
        out_file = "{}/{}/{}.tle".format(tle_dir, sat_type, sat_name)
        creat_prev_folders(out_file)
        if sat_name in all_sat_tle.keys():
            sat_tle = all_sat_tle[sat_name]
            open(out_file, "w").write(sat_tle)

def tle_update(tle_dir: str, tle_sources: List[str], satellites: List[dict]):
    if not os.path.exists(tle_dir):
        os.makedirs(tle_dir)
    if not os.path.exists(tle_dir + "/last_update.json"):
        open(tle_dir + "/last_update.json", "w+").write(json.dumps({"last_update_datetime":-1}))
    tle_dir_json = json.loads(open(tle_dir+"/last_update.json", "r").read())
    tle_dir_json["last_update_datetime"] = str(datetime.now())
    download_tle(tle_sources, tle_dir)
    split_tle_for_satellites(satellites, tle_dir)
    open(tle_dir+"/last_update.json", "w").write(json.dumps(tle_dir_json))

# def main():
#     # get config
#     r = requests.get("http://localhsot:4579/tle_updater/config")
#     config = r.json()
#     tle_dir = config["tle_directory"]
#     satellites_list = config["satellites_list"]
#     tle_sources = config["tle_sources"]

#     last_update


# if __name__ == "__main__":
#     main()

# while 

@sio.on("update", namespace="/tle_updater")
def callback(msg):
    # print("update", data)
    # data = json.loads(data)
    tle_dir = msg["tle_directory"]
    tle_sources = msg["tle_sources"]
    satellites = msg["satellites_list"]   # {"type":"NOAA", "name":"NOAA 15"}
    print(msg)
    tle_update(tle_dir, tle_sources, satellites)
    sio.emit("update_ans", {"tle_dir": tle_dir, "last_update_datetime": str(datetime.now())}, namespace="/tle_updater")

def connect():
    print("I'm connected!")

sio.connect("http://localhost:5000", namespaces=["/tle_updater"])
sio.wait()