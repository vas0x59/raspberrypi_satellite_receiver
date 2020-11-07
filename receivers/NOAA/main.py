import os
import sys
import subprocess
import json 
import time
import threading
from typing import *
import  socketio
# import datetime
from datetime import datetime
# config
# main_config = {}
station_location = {}
tle_dir_path = ""
#
noaa_config = {}
# class NOAA_Satellite:
#     def __init__(self):
#         self.freq = 0
#         self.name = 0

# class Pass:
#     def __init__(self, start_time = 0, end_time = 0, duration = 0):
#         self.start_time = start_time
#         self.end_time = end_time
#         self.duration = duration

# noaa_satellites = {}

# next_pass = None

sio = socketio.Client()

ans1 = False
ans2 = False

passes = []
# passed_passes_times = []

def creat_prev_folders(path: str):
    path_folder = "/".join(path.split("/")[:-1])
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)


def record_1(freq: float, file_out: str, duration: float, sample_rate: int = 60000, dongle_gain: int = 50, bias_tee: str = "enable_bias_tee" , wav_rate: int = 11025) -> str:
    """
    freq - in MHz, sample, 

    out:
    wav_out_path
    """
    wav_out_path = file_out
    raw_out_path = ".".join(file_out.split(".")[:-1] + ["raw"])
    print("raw", raw_out_path, "file_out", file_out)
    # creat_prev_folders(wav_out_path)
    # Run rtl_fm (record)
    a = [
        "timeout", str(duration),
        "rtl_fm",
        "-f", str(freq)+"M",
        "-s", str(sample_rate),
        "-g", str(dongle_gain),
        # "-E", "wav",
        # "-E", "deemp",
        "-A", "fast",
        "-E", "offset",
        "-F", "9",
        raw_out_path
    ]
    print("a:   ", " ".join(a))
    s = subprocess.call(args=a)
    # s.wait()
    # Run sox (convert)
    subprocess.call(args=[
        "sox",
        "-t", "raw",
        "-r", str(sample_rate),
        "-es",
        "-b", "16",
        "-c", "1",
        "-V1",
        raw_out_path,
        wav_out_path,
        "rate", str(wav_rate)
    ])
    
    # Setcorrect time stamp and remove raw
    subprocess.call(args=[
        "touch", "-r", raw_out_path, wav_out_path
    ])
    subprocess.call(args=[
        "rm", raw_out_path
    ])
    return wav_out_path


def wx_to_img(file_in: str, file_out: str, enhancement: str) -> str:
    subprocess.call(args=[
        "wxtoimg", "-o",
        "-e", enhancement,
        file_in,
        file_out
    ])
    return file_out


def process(sat_name: str, pass_duration: float, pass_time_rise: datetime, pass_time_fall: datetime, noaa_config: dict):
    # global passed_passes_times
    output_path = "/home/vasily/Projects/raspberrypi_satellite_receiver/output"
    freq = noaa_config["satellites"][sat_name]["apt_freq"]
    duration = pass_duration

    datetime_str = str(pass_time_rise)
    sat_output_folder = "{}/NOAA/{}/{}".format(output_path, sat_name, datetime_str)
    creat_prev_folders(sat_output_folder)
    wav_file = sat_output_folder+"/wav/{}_{}_{}.wav".format(sat_name, freq, datetime_str)
    creat_prev_folders(wav_file)

    record_1(freq, wav_file, duration, dongle_gain=noaa_config["radio"]["dongle_gain"])

    images_folder = sat_output_folder+"/image"
    creat_prev_folders(images_folder)

    enhancements = noaa_config["wx_to_img"]["enhancements"]
    print(enhancements)
    for e in enhancements:
        image_file = images_folder+"/{}_{}_{}.jpg".format(sat_name, e, datetime_str)
        wx_to_img(wav_file, image_file, e)
    # passed_passes_times.append(pass_time_rise)
    # if len(passed_passes_times) > 50:
    #     passed_passes_times = passed_passes_times[1:]


'''
-> pass
process(pass.sat_name, pass.duration, pass.start_time)
'''


def passes_from_json(ans: List[dict]) -> List[dict]:
    ans_s = list()
    for i in range(len(ans)):
        el = dict(ans[i])
        # el = ans[a]
        # print("bbbbbb", el["rise_time"], el["fall_time"])
        el["rise_time"] = datetime.fromisoformat(ans[i]["rise_time"])
        el["fall_time"] = datetime.fromisoformat(ans[i]["fall_time"])
        # print("aaaaaaa", el["rise_time"], el["fall_time"])
        # el["duration"] = datetime.fromisoformat(el["duration"])
        ans_s.append(el)
    return ans_s


def passes_to_json(ans: List[dict]) -> List[dict]:
    ans_s = list()
    for i in range(len(ans)):
        el = ans[i].copy()
        el["rise_time"] = str(ans[i]["rise_time"])
        el["fall_time"] = str(ans[i]["fall_time"])
        # el["duration"] = str(el["duration"])
        ans_s.append(el)
    return ans_s


@sio.on("pass_schedule", namespace="/receivers/NOAA")
def ps_callback(msg):
    global passes, ans1
    ans1 = True
    passes_msg = passes_from_json(msg["passes"])
    passes_msg = [i for i in passes_msg if i["fall_time"] > datetime.utcnow()]
    passes = passes_msg
    print("pass_schedule")


@sio.on("config", namespace="/receivers/NOAA")
def c_callback(msg):
    global noaa_config, station_location, tle_dir_path, ans2
    ans2 = False
    noaa_config = msg["config"]
    station_location = msg["station_location"]
    tle_dir_path = msg["tle_directory"]
    print("config", msg)


@sio.event
def connect():
    print("I'm connected!")
    # sio.emit("config/get", {"":""}, namespace="/receivers/NOAA")
    # sio.emit("pass_schedule/get", {"":""}, namespace="/receivers/NOAA")
    # print("Send")


sio.connect("http://localhost:5000", namespaces=["/receivers/NOAA", "/receivers"])

sio.emit("config/get", {"":""}, namespace="/receivers/NOAA")
sio.emit("pass_schedule/get", {"":""}, namespace="/receivers/NOAA")

while True:
    if len(passes) > 0:
        next_pass = passes[0]
        # print(next_pass)
        # print(datetime.utcnow() >= next_pass["fall_time"])
        if next_pass["rise_time"] <= datetime.utcnow() <= next_pass["fall_time"]:
            print("Start st2", next_pass)
            while datetime.utcnow() < next_pass["rise_time"]:
                time.sleep(0.05)
            duration_u = (next_pass["fall_time"] - max(next_pass["rise_time"], datetime.utcnow())).total_seconds()
            sio.emit("pass_begin", {"pass": passes_to_json([next_pass])[0]}, namespace="/receivers/NOAA")

            # print(next_pass["name"], next_pass["duration"], duration_u, noaa_config)
            process(next_pass["name"], min(duration_u, next_pass["duration"]), next_pass["rise_time"], next_pass["fall_time"], noaa_config)
            print("RECORD END wait for end of pass")
            while datetime.utcnow() <= next_pass["fall_time"]:
                time.sleep(0.05)
            print("Exit st2")
            sio.emit("pass_end", {"pass":passes_to_json([next_pass])[0]}, namespace="/receivers/NOAA")
            # sio.emit("pass_schedule/get", {}, namespace="/receivers/NOAA")
        passes = sorted([i for i in passes if i["fall_time"] > datetime.utcnow()], key=lambda x: x["rise_time"])
    time.sleep(0.1)
sio.wait()