import requests
import json
# import socketio

# sio = socketio.Client()

def download_tle(tle_sources: list[str], tle_dir: str):
    concatenated_content = ""
    for tle_source in tle_sources:
        r = requests.get(tle_source, allow_redirects=True)
        tle_source_name = tle_source.split("/")[-1].split(".")[0] + ".tle"
        tle_source_file_name = tle_dir + "/original/" + tle_source_name
        concatenate_content += r.content
        open(tle_source_file_name, "w").write(r.content)
    
    open(tle_dir + "/all.tle", "w").write(concatenated_content)
    


def split_tle_for_satellites(satellites: list[dict], tle_dir: str):
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
        sat_name = satellite["name"]
        sat_type = satellite["type"]
        out_file = "{}/{}/{}.tle".format(tle_dir, sat_type, sat_name)
        if sat_name.strip() in all_sat_tle:
            sat_tle = all_sat_tle[sat_tle]
            open(out_file, "w").write(sat_tle)

def tle_update(tle_dir: str, tle_sources: list[str], satellites: list[dict]):
    tle_dir_json = json.loads(open(tle_dir+"/last_update.json", "r").read())
    tle_dir_json["last_update_datetime"] = get_datetime()
    download_tle(tle_sources, tle_dir)
    split_tle_for_satellites(satellites, tle_dir)
    open(tle_dir+"/last_update.json", "w").write(json.dumps(tle_dir_json))

# @sio.on("update", namespace="tle_download")
# def callback(sid, msg):
#     print("update")
#     tle_dir = msg["tle_dir"]
#     tle_sources = msg["tle_sources"]
#     satellites = msg["satellites"] # {"type":"NOAA", "name":"NOAA 15"}
#     tle_update(tle_dir, tle_sources, satellites)

# def connect():
#     print("I'm connected!")

# sio.connect("http://localhost:5000", namespaces=["tle_download"])
# sio.wait()