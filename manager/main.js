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

setInterval(() => {
    console.log("tle_updater");
    let mes = {
        "tle_directory":cm.get_main("tle_directory"),
        "tle_sources":cm.get_main("tle_sources"),
        "satellites_list":cm_m.satellites_d_to_l(cm_m.ungroup_satellites(cm.get_main("satellites")))
    };
    console.log("tle update message", mes);
    io.of("/tle_updater").emit("update", mes);
}, cm.get_main("tle_update_period")*60*60*1000)


 
http.listen(5000, () => {
    console.log('listening on *:5000');
});


