const express = require('express')
const app = express()
const http = require('http')
const server = http.createServer(app)
const io = require('socket.io')(server)
const path = require("path")
let g = require("./g.js")

app.use('/', express.static(path.join(__dirname, 'public')))

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/index.html'))
})


io.on('connection', (socket) => {
    console.log("new client")
    socket.on("update_tle", (_) => {
        console.log("GGGGG")
        g.event.emit("/tle_updater/update", {})
    })
    socket.on("predict_pass", (_) => {
        g.event.emit("/predict_pass/predict", {})
    })
})
g.event.on("/tle_updater/update_ans", () => {
    io.emit("update_tle_ans")
})
g.event.on("/predict_pass/predict_ans", () => {
    io.emit("predict_pass_ans")
})


server.listen(8080,  () => {
  console.log('Express listening on *:8080')
})

