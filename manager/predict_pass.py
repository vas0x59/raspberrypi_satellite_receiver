import json
import socketio
import predict
# from pyorbital.orbital import Orbital
import numpy
import pandas
from datetime import datetime

sio = socketio.Client()

@sio.on("predict", namespace="predict_pass")
def callback(sid, msg):
    print("update")
    tle_dir = msg["tle_dir"]
    satellites = msg["satellites"] # {"type":"NOAA", "name":"NOAA 15"}
    max_time = msg["max_time"]     # hours
    station_location = msg["station_location"] # { "lat" : 0, "lon" : 0, "alt" : 0 }
    min_elevation = msg["min_elevation"]
    all_transitions = []
    for sat in satellites:
        sat_type = sat["type"]
        sat_name = sat["name"]
        # orbital = Orbital(sat, tle_file="{}/{}/{}.tle".format(tle_dir, sat_type, sat_name))
        time_now = datetime.now()
        # passes = orbital.get_next_passes(time_now, max_time, station_location["lon"], station_location["lat"], station_location["alt"], horizon=min_elevation)

        all_transitions += [{"type":sat_type, "name":sat_name, "rise_time":pas[0], "fall_time":pas[1], "duration":pas[2]} for pas in passes]
    
    
    
@sio.event
def connect():
    print("I'm connected!")

sio.connect("http://localhost:5000", namespaces=["predict_pass"])
sio.wait()


