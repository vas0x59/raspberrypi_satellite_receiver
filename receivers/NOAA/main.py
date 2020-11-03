import os
import sys
import subprocess
import json 
import time
# from typing import *

# config
# main_config = {}
station_location = {}
tle_dir_path = ""

noaa_config = {}
# class NOAA_Satellite:
#     def __init__(self):
#         self.freq = 0
#         self.name = 0

noaa_satellites = {}

def record(freq: float, file_out: str, duration: float, sample_rate = 60000: int, dongle_gain = 50: int, bias_tee = "enable_bias_tee": str, wav_rate: int = 11025) -> str:
    """
    freq - in MHz, sample, 

    out:
    wav_out_path
    """
    wav_out_path = file_out
    raw_out_path = ".".join(file_out.split(".")[:-1] + ["raw"])

    # Run rtl_fm (record)
    subprocess.call(args=[
        "timeout", str(duration), 
        "rtl_fm", bias_tee,   
        "-f", str(freq)+"M", 
        "-s", str(sample_rate), 
        "-g", str(dongle_gain),
        "-F", "9",
        raw_out_path
    ])
    
    # Run sox (convert)
    subprocess.call(args=[
        "sox",
        "-t", "raw",
        "-r", str(sample_rate),
        "-b", "16",
        raw_out_path,
        wav_out_path,
        "rate", str(wav_rate)
    ])
    
    # Setcorrect time stamp and remove raw
    subprocess.call(args=[
        "touch -r", raw_out_path, wav_out_path
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
# record()

def process():
    output_path = ""
    sat_name = ""
    freq = 0
    duration = 0

    datetime_str = get_datetime()
    sat_output_folder = "{}/NOAA/{}/{}".format(output_path, sat_name, datetime_str)
    wav_file = sat_output_folder+"/wav/{}_{}_{}.wav".format(sat_name, freq, datetime_str)
    
    record(freq, wav_file, duration)

    enhancements = []
    for e in enhancements:
        image_file = sat_output_folder+"/image/{}_{}_{}.jpg".format(sat_name, e, datetime_str)
        wx_to_img(wav_file, image_file, e)
    
