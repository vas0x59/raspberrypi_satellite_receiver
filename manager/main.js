const app = require('express')();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const fs = require('fs');
const path = require('path');
const cm_m = require('./config_manager');

const RSR_PATH = process.env.RSR_PATH
const RSR_CONFIGS_PATH = process.env.RSR_CONFIGS_PATH

// let main_config_json = JSON.parse(fs.readFileSync(RSR_CONFIGS_PATH + "/main_config.json").toString());
// console.log(main_config_json);
// let satellites_sep_by_type = main_config_json.satellites;

// console.log(satellites_sep_by_type);
// let satellites_list = [];
// for (let key in satellites_sep_by_type) {
//     if (satellites_sep_by_type.hasOwnProperty(key)) {
//         let el = satellites_sep_by_type[key];
//         el.name = key;
//         satellites_list.push(el);
//     }
// }
// console.log("satellites_list", satellites_list);
let cm = new cm_m.ConfigManager(RSR_CONFIGS_PATH);

let passes = [];

app.get('/', (req, res) => {
    res.send("HELLO WORLD");
});

io.on('connection', (socket) => {
    console.log('a user connected');
});
io.of("/tle_updater").on("connection", (socket) => {
    console.log("tle_updater");
    let mes = {
        "tle_directory":cm.get_main("tle_directory"),
        "tle_sources":cm.get_main("tle_sources"),
        "satellites_list":cm_m.satellites_d_to_l(cm_m.ungroup_satellites(cm.get_main("satellites")))
    };
    console.log("tle update message", mes);
    socket.on("update_ans", (mes) => {
        console.log("update_ans", mes);
    });
    socket.emit("update", mes);
});

io.of("/predict_pass").on("connection", (socket) => {
    console.log("predict_pass");
    /*
    tle_dir = msg["tle_directory"]
    satellites = msg["satellites"]
    station_location = msg["station_location"]
    min_elevation = msg["min_elevation"]
    for_next_hours = msg["for_next_hours"]
    prev_predict = msg["prev_predict"]
     */
    let mes = {
        "tle_directory":cm.get_main("tle_directory"),
        "satellites":cm_m.ungroup_satellites(cm.get_main("satellites")),
        "station_location":cm.get_main("station_location"),
        "min_elevation":cm.get_main("min_elevation"),
        "for_next_hours":cm.get_main("predict_update_period"),
        "prev_predict":passes
    };
    console.log("predict_pass message", mes);
    socket.on("predict_ans", (mes) => {
        console.log("predict_pass ans", mes);
        passes = mes["ans"];
    });
    socket.emit("predict", mes);
});

// setInterval(() => {
//     console.log("tle_updater");
//     let mes = {
//         "tle_directory":cm.get_main("tle_directory"),
//         "tle_sources":cm.get_main("tle_sources"),
//         "satellites_list":cm_m.satellites_d_to_l(cm_m.ungroup_satellites(cm.get_main("satellites")))
//     };
//     console.log("tle update message", mes);
//     io.of("/tle_updater").emit("update", mes);
// }, cm.get_main("tle_update_period")*60*60*1000)


 
http.listen(5000, () => {
    console.log('listening on *:5000');
});


