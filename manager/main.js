let g = require('./g.js')
const { spawn, exec } = require('child_process');


require("./rsr.js")
require("./webui.js")
console.log("start tle_updater.py predict_pass.py")
// const tle_updater_spawn = exec("python3 " + g.RSR_PATH+"/manager/tle_updater.py");
// const predict_pass_spawn = exec("python3 " + g.RSR_PATH+"/manager/predict_pass.py");
g.event.on("io_server_started", () =>{
    // const tle_updater_spawn = spawn("python3", [g.RSR_PATH+"/manager/tle_updater.py"]);
    // const predict_pass_spawn = spawn("python3", [g.RSR_PATH+"/manager/predict_pass.py"]);
    const tle_updater_spawn = exec("python3 " + g.RSR_PATH+"/manager/tle_updater.py");
    const predict_pass_spawn = exec("python3 " + g.RSR_PATH+"/manager/predict_pass.py");

})
// let cleanExit = function() {  };
process.on('SIGINT', ()=>{process.exit()}); // catch ctrl-c
process.on('SIGTERM', ()=>{process.exit()}); // catch kill
