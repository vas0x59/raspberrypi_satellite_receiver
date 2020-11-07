import json
import os
import sys
# import argparse

path_to_conf_t = sys.argv[1]
path_to_conf = sys.argv[2]

m_c = json.loads(open(path_to_conf_t, "r").read())


m_c["tle_directory"] = "/home/pi/raspberrypi_satellite_receiver/tle"
m_c["output_directory"] = "/home/pi/raspberrypi_satellite_receiver/output"
m_c["configured"] = False

open(path_to_conf, "w").write(json.dumps(m_c, indent=True))
