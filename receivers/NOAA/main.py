import os
import sys
import subprocess
import json 
# from typing import *


def record(freq: float, file_out: str, duration: float, sample_rate = 60000: int, dongle_gain = 50: int, bias_tee = "enable_bias_tee": str, wav_rate: int = 11025) -> str:
    """
    freq - in MHz, sample, 

    out:
    wav_out_path
    """
    wav_out_path = file_out
    raw_out_path = ".".join(file_out.split(".")[:-1] + ["raw"])

    # Run rtl_fm (record)
    subprocess.run(args=[
        "timeout", str(duration), 
        "rtl_fm", bias_tee,   
        "-f", str(freq)+"M", 
        "-s", str(sample_rate), 
        "-g", str(dongle_gain),
        "-F", "9",
        raw_out_path
    ])
    
    # Run sox (convert)
    subprocess.run(args=[
        "sox",
        "-t", "raw",
        "-r", str(sample_rate),
        "-b", "16",
        raw_out_path,
        wav_out_path,
        "rate", str(wav_rate)
    ])
    
    # Setcorrect time stamp and remove raw
    subprocess.run(args=[
        "touch -r", raw_out_path, wav_out_path
    ])
    subprocess.run(args=[
        "rm", raw_out_path
    ])
    return wav_out_path

def wx_to_img(file_in: str, file_out: str, enhancement: str) -> str:
    subprocess.run(args=[
        "wxtoimg", "-o",
        "-e", enhancement,
        file_in,
        file_out
    ])
    return file_out
# record()

def process():
    wav_file = ""
    
    record(freq, wav_file, duration)

    enhancements = []
    for e in enhancements:
        image_file = ""
        wx_to_img(wav_file, image_file, e)

