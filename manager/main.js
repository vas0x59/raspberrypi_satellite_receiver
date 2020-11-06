const app = require('express')()
const http = require('http').createServer(app)
const io = require('socket.io')(http)
const fs = require('fs')
const path = require('path')
const cm_m = require('./config_manager')
const EventEmitter = require('events')

const RSR_PATH = process.env.RSR_PATH
const RSR_CONFIGS_PATH = process.env.RSR_CONFIGS_PATH

let cm = new cm_m.ConfigManager(RSR_CONFIGS_PATH)

class GlobalEvents extends EventEmitter {}
let event = new GlobalEvents()

let passes = []
let last_tle_update_time = NaN
let last_pass_predict_time = NaN

app.get('/', (req, res) => {
    res.send("HELLO WORLD")
})

io.on('connection', (socket) => {
    console.log('a user connected')
})



event.on("/tle_updater/update", (_) => {
    console.log("/tle_updater/update")
    io.of("/tle_updater").emit("update", {
        "tle_directory":cm.get_main("tle_directory"),
        "tle_sources":cm.get_main("tle_sources"),
        "satellites_list":cm_m.satellites_d_to_l(cm_m.ungroup_satellites(cm.get_main("satellites")))
    })
})

event.on("/predict_pass/predict", (_) => {
    console.log("/predict_pass/predict")
    if (isNaN(last_tle_update_time)) {
        let interval_id = setInterval(() => {
            event.emit("/tle_updater/update", {})
        }, 5000)
        event.emit("/tle_updater/update", {})
        event.on("/tle_updater/update_ans", () => {
            clearInterval(interval_id)
            io.of("/predict_pass").emit("predict", {
                "tle_directory":cm.get_main("tle_directory"),
                "satellites":cm_m.ungroup_satellites(cm.get_main("satellites")),
                "station_location":cm.get_main("station_location"),
                "min_elevation":cm.get_main("min_elevation"),
                "for_next_hours":cm.get_main("predict_update_period"),
                "prev_predict":passes
            })
        })
    }
    else {
        io.of("/predict_pass").emit("predict", {
            "tle_directory":cm.get_main("tle_directory"),
            "satellites":cm_m.ungroup_satellites(cm.get_main("satellites")),
            "station_location":cm.get_main("station_location"),
            "min_elevation":cm.get_main("min_elevation"),
            "for_next_hours":cm.get_main("predict_update_period"),
            "prev_predict":passes
        })
    }
})

io.of("/tle_updater").on("connection", (socket) => {
    console.log("tle_updater connected")
    socket.on("update_ans", (mes) => {
        console.log("update_ans", mes)
        last_tle_update_time = Date.parse(mes["last_update_time"])
        event.emit("/tle_updater/update_ans", mes)
    })
    event.emit("/tle_updater/update", {})
})

io.of("/predict_pass").on("connection", (socket) => {
    console.log("predict_pass connected")
    socket.on("predict_ans", (mes) => {
        console.log("predict_ans", mes)
        passes = mes["ans"]
        last_pass_predict_time = Date.parse(mes["last_predict_time"])
        event.emit("/predict_pass/predict_ans", mes)
    })
    event.emit("/predict_pass/predict", {})
})

 
http.listen(5000, () => {
    console.log('listening on *:5000')
})


