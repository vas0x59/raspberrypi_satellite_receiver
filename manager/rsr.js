// const app = require('express')()
const http = require('http')
http_server = http.createServer(() => {})
const io = require('socket.io')(http_server)
const fs = require('fs')
const path = require('path')
const utils = require('./utils.js')
// const EventEmitter = require('events')
let g = require('./g.js')
// event = g.event

io.on('connection', (socket) => {
    console.log('a user connected')
})

function send_predict_pass_predict () {
    io.of("/predict_pass").emit("predict", {
        "tle_directory":g.cm.get_main("tle_directory"),
        "satellites":utils.ungroup_satellites(g.cm.get_main("satellites")),
        "station_location":g.cm.get_main("station_location"),
        "min_elevation":g.cm.get_main("min_elevation"),
        "for_next_hours":g.cm.get_main("predict_update_period"),
        "prev_predict":g.passes
    })
}

g.event.on("/tle_updater/update", (_) => {
    console.log("/tle_updater/update")
    io.of("/tle_updater").emit("update", {
        "tle_directory":g.cm.get_main("tle_directory"),
        "tle_sources":g.cm.get_main("tle_sources"),
        "satellites_list":utils.satellites_d_to_l(utils.ungroup_satellites(g.cm.get_main("satellites")))
    })
})

g.event.on("/predict_pass/predict", (_) => {
    console.log("/predict_pass/predict")
    console.log((new Date()).getTime(), g.last_tle_update_time )
    if ((isNaN(g.last_tle_update_time) ||
        (new Date().getTime() - g.last_tle_update_time > g.cm.get_main("tle_update_period")*60*60*1000)) &&
        g.modules_connected.tle_updater) {
        // let interval_id = setInterval(() => {
        //     g.event.emit("/tle_updater/update", {})
        // }, 5000)
        g.event.emit("/tle_updater/update", {})
        let a = () => {
            send_predict_pass_predict();
            g.event.removeListener("/tle_updater/update/new", a)
        }
        g.event.on("/tle_updater/update/new", a)
    }
    else {
        console.log("123123")
        send_predict_pass_predict();
    }
})

io.of("/tle_updater").on("connection", (socket) => {
    console.log("tle_updater connected")
    g.modules_connected.tle_updater = true

    socket.on("update_ans", (mes) => {
        console.log("update_ans", mes)
        g.last_tle_update_time = Date.parse(mes["last_update_datetime"])
        g.event.emit("/tle_updater/update/new", mes)
    })
    // g.event.emit("/tle_updater/update", {})
})

io.of("/predict_pass").on("connection", (socket) => {
    console.log("predict_pass connected")
    g.modules_connected.predict_pass = true

    socket.on("predict_ans", (mes) => {
        console.log("predict_ans", mes)
        g.passes = mes["ans"]
        g.last_pass_predict_time = Date.parse(mes["last_predict_datetime"])
        // console.log('g.last_pass_predict_time', g.last_pass_predict_time)
        g.event.emit("/predict_pass/predict/new", mes)
        // socket.removeListener('predict_ans', a);
    })
    g.event.on("/main_config/station_location/new", () => {
        g.event.emit("/predict_pass/predict", {})
    })

    // g.event.emit("/predict_pass/predict", {})
})

io.of("/receivers/NOAA").on("connection", (socket) => {
    console.log("/receivers/NOAA connected")
    g.modules_connected.NOAA = true
    let send_conf = () => {
        socket.emit("config", {"config": g.cm.get_receiver_config("NOAA"), "station_location":g.cm.get_main("station_location"), "tle_directory":g.cm.get_main("tle_directory")})
    }
    socket.on("config/get", (_) => {
        console.log("/receivers/NOAA config/get")
        send_conf()
    })
    socket.on("pass_schedule/get", (_) => {
        console.log("/receivers/NOAA pass_schedule/get")
        socket.emit("pass_schedule", {"passes": utils.get_passes_by_type_satellites(g.passes, "NOAA")})
    })
    socket.on("pass_begin", (m) => {
        g.event.emit("pass_begin", {"name":m.pass.name, "type":m.pass.type})
    })
    socket.on("pass_end", (m) => {
        g.event.emit("pass_end", {"name":m.pass.name, "type":m.pass.type})
    })
    g.event.on("/predict_pass/predict/new", (_) => {
        socket.emit("pass_schedule", {"passes": utils.get_passes_by_type_satellites(g.passes, "NOAA")})
    })
    g.event.on("/main_config/station_location/new", (_) => {
        send_conf()
    })
})

function predict_pass_interval_f() {
    console.log("predict_pass_interval_f")
    g.event.emit("/predict_pass/predict", {})
}
function tle_update_interval_f() {
    // if ((new Date().getTime() - g.last_tle_update_time > g.cm.get_main("tle_update_period")*60*60*1000)){
    g.event.emit("/tle_updater/update", {})
    // }
}

function predict_pass_and_tle_update_retry() {
    if (!g.modules_connected.predict_pass || !g.modules_connected.tle_updater) {
        setTimeout(predict_pass_and_tle_update_retry, 80);
        return;
    }
    predict_pass_interval_f()
    let predict_pass_interval = setInterval(predict_pass_interval_f, (g.cm.get_main("predict_update_period")*60*60 - 1)*1000) // (g.cm.get_main("predict_update_period")*60*60 - 1)*1000
    let tle_update_interval = setInterval(predict_pass_interval_f, (g.cm.get_main("tle_update_period")*60*60 - 1)*1000)
}
predict_pass_and_tle_update_retry()

http_server.listen(5000, () => {
    console.log('Socket IO listening on *:5000')
    g.event.emit("io_server_started", {})
})


