const cm_m = require('./utils')
const EventEmitter = require('events')

const RSR_PATH = process.env.RSR_PATH
const RSR_CONFIGS_PATH = process.env.RSR_CONFIGS_PATH

let cm = new cm_m.ConfigManager(RSR_CONFIGS_PATH)

class GlobalEvents extends EventEmitter {}

let event = new GlobalEvents()

let passes = []
let last_tle_update_time = NaN
// let tle_updater_connected = false
//
let last_pass_predict_time = NaN
// let pass_predict_connected = false
let modules_connected = {
    "tle_updater": false,
    "predict_pass": false
}

module.exports.passes = passes
module.exports.last_tle_update_time = last_tle_update_time
module.exports.last_pass_predict_time = last_pass_predict_time
module.exports.event = event
module.exports.cm = cm
module.exports.RSR_PATH = RSR_PATH
module.exports.RSR_CONFIGS_PATH = RSR_CONFIGS_PATH
module.exports.modules_connected = modules_connected