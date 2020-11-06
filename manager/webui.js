const express = require('express')
const app = express()
const server = require('http').createServer(app)
const io = require('socket.io')(server)
const path = require("path")
let g = require("./g.js")

io.on('connection', (socket) => {
    socket.on("update_tle", () => {
        g.event.emit("/tle_updater/update", {})
    })
    socket.on("predict_pass", () => {
        g.event.emit("/predict_pass/predict", {})
    })
})


app.use('/', express.static(path.join(__dirname, 'public')))
app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname, 'public/index.html'))
})
server.listen(8080, function () {
  console.log('Express listening on *:8080')
})




