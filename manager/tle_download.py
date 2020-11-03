import requests

def download_tle(tle_sources: list[str], tle_dir: str):
    concatenated_content = ""
    for tle_source in tle_sources:
        r = requests.get(tle_source, allow_redirects=True)
        tle_source_name = tle_source.split("/")[-1].split(".")[0] + ".tle"
        tle_source_file_name = tle_dir + "/original/" + tle_source_name
        concatenate_content += r.content
        open(tle_source_file_name, "w").write(r.content)
    
    open(tle_dir + "/all.tle", "w").write(concatenated_content)
    


def split_tle_for_satellites(satellites: list[], tle_dir: str):
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
        sat_name = ""
        sat_type = ""
        out_file = "{}/{}/{}.tle".format(tle_dir, sat_type, sat_names)
        if sat_name.strip() in all_sat_tle:
            sat_tle = all_sat_tle[sat_tle]
            open(out_file, "w").write(sat_tle)

def tle_update(tle_dir: str, tle_sources: list[str], satellites: list[]):
    download_tle(tle_sources, tle_dir)
    split_tle_for_satellites(satellites, tle_dir)
