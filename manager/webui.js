const express = require('express')
const app = express()
const http = require('http')
const server = http.createServer(app)
const io = require('socket.io')(server)
const path = require("path")
let g = require("./g.js")
var serveIndex = require('serve-index')

app.use('/', express.static(path.join(__dirname, 'public')))

app.use('/output', express.static(g.cm.get_main("output_directory")), serveIndex(g.cm.get_main("output_directory"), {'icons': true}))

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/index.html'))
})


io.on('connection', (socket) => {
    console.log("new client")
    socket.on("update_tle", (_) => {
        // console.log("GGGGG")
        g.event.emit("/tle_updater/update", {})
    })
    socket.on("predict_pass", (_) => {
        g.event.emit("/predict_pass/predict", {})
    });
    let fields = ["station_location", "station_name"]
    for (let ii in fields){
        let i = fields[ii]
        socket.on(i+"/get", (_) => {

            // g.event.emit("/predict_pass/predict", {})
            // g.cm.set_main(i, mes[i])
            let res = {}
            res[i] = g.cm.get_main(i)
            console.log("GET", i+"/get", "RES", i+"/get/ans", res)
            socket.emit(i+"/get/ans", res)
        })
        socket.on(i+"/set", (mes) => {
            console.log("SET", i+"/set", mes)

            // console.log("GETTTT")
            // g.event.emit("/predict_pass/predict", {})
            if (JSON.stringify(g.cm.get_main(i)) !== JSON.stringify(mes[i])) {
                console.log("emit", "/main_config/"+i+"/new", g.cm.get_main(i), mes[i])
                g.event.emit("/main_config/"+i+"/new", {})
            }
            g.cm.set_main(i, mes[i])

            let res = {}
            res[i] = g.cm.get_main(i)
            socket.emit(i+"/get/ans", res)
        })
    }
})
g.event.on("/tle_updater/update/new", () => {
    io.emit("update_tle/ans")
})
g.event.on("/predict_pass/predict/new", () => {
    io.emit("predict_pass/ans")
})
g.event.on("pass_begin", (m) => {
    io.emit("pass_begin", m)
})
g.event.on("pass_end", (m) => {
    io.emit("pass_end", m)
})

server.listen(8080,  () => {
  console.log('Express listening on *:8080')
})

