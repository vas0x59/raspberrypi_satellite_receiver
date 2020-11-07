import React, { Component } from 'react'
import Button from '@material-ui/core/Button'
import TextField from '@material-ui/core/TextField';
import io from 'socket.io-client'
const socket = io()

import { createMuiTheme, ThemeProvider, makeStyles } from '@material-ui/core/styles'
import { SnackbarProvider, useSnackbar } from 'notistack'


const theme = createMuiTheme({
    palette: {
        type:"dark",
        primary: {
            main: '#8bc34a',
        },
        secondary: {
            main: '#ff9100',
        },
        background: {
          paper: "#212121"
        }
    },
});

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

function Button_update_tle() {
    const { enqueueSnackbar } = useSnackbar();
    socket.on("update_tle/ans", () => {
        enqueueSnackbar('TLE Updated', { variant: "success" });
    })
    const hClick = () => {
        socket.emit("update_tle", {});
    };
    return (
        <Button variant="contained" color="primary" onClick={()=>{hClick()}}>
            update_tle
        </Button>
    )
}

function Button_predict_pass() {
    const { enqueueSnackbar } = useSnackbar();
    socket.on("predict_pass/ans", () => {
        enqueueSnackbar('Satellites passes predicted', { variant: "success" });
    })
    const hClick = () => {
        socket.emit("predict_pass", {});
    };
    return (
        <Button variant="contained" color="primary" onClick={()=>{hClick()}}>
            predict_pass
        </Button>
    )
}

class Station_settings extends Component{
    constructor(params) {
        super(params)
        this.state = {
            station_location: {
                lat: 0,
                lon: 0,
                alt: 0
            },
            station_location_d: {
                lat: "",
                lon: "",
                alt: ""
            },
            station_name: ""

        }
        this.fields = ["station_location", "station_name"]

        for (let ii in this.fields){
            let i = this.fields[ii]
            socket.on(i+"/get/ans", (msg) => {
                console.log(i+"/get/ans", msg)
                let s = {}
                s[i] = msg[i]
                if (i === "station_location")
                    s[i+"_d"] = msg[i]
                this.setState(s)
            })
            console.log(i+"/get")
            socket.emit(i+"/get", {})
        }
        // for (const ii in ["station_location", "station_name"]) {
        //     const i =
        //
        // }
        // this.send = this.send.bind(send)
        // this.on_sl_ch = this.on_sl_ch.bind(on_sl_ch)
        // this.save_click = this.save_click.bind(save_click)
    }
    on_sl_ch = (n, e) => {
        let station_location = Object.assign({}, this.state.station_location);
        let station_location_d = Object.assign({}, this.state.station_location_d);
        station_location[n] = parseFloat(e.target.value)
        station_location_d[n] = e.target.value
        console.log("on_sl_ch", station_location, station_location_d, parseFloat(e.target.value))
        this.setState({station_location_d: station_location_d, station_location: station_location})
        // this.props.onChange(this.state)
    }
    save_click = () => {
        console.log("state", this.state);

        for (let ii in this.fields){
            let i = this.fields[ii]
            console.log(i + "/set")
            let mes = {}
            mes[i] = this.state[i]
            socket.emit(i + "/set", mes)
        }
    }
    render() {
        return (
            <div>
                <TextField variant="filled" id="station_name_input" label="Station Name" value={this.state.station_name} onChange={(e)=>{
                    this.setState({station_name:e.target.value})}
                }/>
                <TextField variant="filled" id="Latitude_input" label="Latitude" value={this.state.station_location_d.lat} onChange={(e)=>{
                    this.on_sl_ch("lat", e)}
                }/>
                <TextField variant="filled" id="Longitude_input" label="Longitude" value={this.state.station_location_d.lon} onChange={(e)=>{
                    this.on_sl_ch("lon", e)}
                }/>
                <TextField variant="filled" id="Altitude_input" label="Altitude" value={this.state.station_location_d.alt} onChange={(e)=>{
                    this.on_sl_ch("alt", e)}
                }/>
                <Button variant="contained" color="primary" onClick={this.save_click}>Save</Button>
            </div>
        )
    }
}

class App extends Component {
    constructor(params) {
        super(params)
        // socket.on('connect', function(){});
        // socket.on('event', function(data){});
        // Input_station_location.send();
        // this.save_click = this.save_click.bind(this);
    }
    render() {
        return (
            <div>
                <Station_settings/>
                <Button_update_tle/>
                <Button_predict_pass/>

            </div>
        )
    }
}

export default function CustomStyles() {
    return (
        <ThemeProvider theme={theme}>
            <SnackbarProvider maxSnack={3}>
                <App/>
            </SnackbarProvider>
        </ThemeProvider>
    )
}