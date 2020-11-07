import os
import subprocess
import sys
import json

RSR_PATH = os.getenv('RSR_PATH')
RSR_CONFIGS_PATH = os.getenv('RSR_CONFIGS_PATH')

print("path:", RSR_PATH)
f_c = open(RSR_CONFIGS_PATH+"/main_config.json", "r")
main_config = json.loads(f_c.read())
f_c.close()
print("main_config", main_config)

manager_p = subprocess.Popen(args=["node", "{}/manager/main.js".format(RSR_PATH)])
tle_updater_p = subprocess.Popen(args=["python3", "{}/manager/tle_updater.py".format(RSR_PATH)])
predict_pass_p = subprocess.Popen(args=["python3", "{}/manager/predict_pass.py".format(RSR_PATH)])

receivers_p = []

for rn in main_config["receivers"]:
    rn_p = subprocess.Popen(args=["python3", "{}/receivers/{}/main.py".format(RSR_PATH, rn)])
    receivers_p.append(rn_p)


manager_p.wait()
tle_updater_p.wait()
predict_pass_p.wait()
[rp.wait() for rp in receivers_p]
