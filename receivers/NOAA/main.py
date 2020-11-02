import os
import sys
import subprocess
import json 
# from typing import *


def record(freq: float, work_dir: str, out_name: str, duration: float, sample = 60000: int, dongleGain = 50: int, bias_tee = "enable_bias_tee": str, wav_rate: int = 11025):
    """
    freq - in MHz, sample, 
    """
    wav_out_path = work_dir + "/" + out_name+".wav"
    raw_out_path = work_dir + "/" + out_name+".raw"

    # Run rtl_fm
    subprocess.run(args=[
        "timeout", str(duration), 
        "rtl_fm", bias_tee, 
        "-f", str(freq)+"M", 
        "-s", str(sample), 
        "-g", str(dongleGain),  
        "-F", "9"

        ])
    
    # Run sox
    subprocess.run(args=[
        "sox",
        "-t", "raw",
        "-r", str(sample),
        "-b", "16",
        raw_out_path,
        wav_out_path,
        "rate", str(wav_rate)
        ])
    
    # Remove raw file
    # os.remove()
# record()

