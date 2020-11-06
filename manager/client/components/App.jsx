import React, { Component } from 'react'
import Button from '@material-ui/core/Button'
import io from 'socket.io-client'
const socket = io()

import { createMuiTheme, ThemeProvider, makeStyles } from '@material-ui/core/styles'
import { SnackbarProvider, useSnackbar } from 'notistack'


const theme = createMuiTheme({
    palette: {
        type:"dark",
        primary: {
            main: '#ff9800',
        },
        secondary: {
            main: '#66bb6a',
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
    socket.on("update_tle_ans", () => {
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
    socket.on("predict_pass_ans", () => {
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

class App extends Component {
    constructor(params) {
        super(params)
        // socket.on('connect', function(){});
        // socket.on('event', function(data){});
    }
    render() {
        return (
            <div>
                <Button_update_tle/>
                <Button_predict_pass/>

            </div>
        )
    }
}
function IntegrationNotistack() {
  return (
    <SnackbarProvider maxSnack={3}>
      <App />
    </SnackbarProvider>
  );
}

export default function CustomStyles() {
    return (
        <ThemeProvider theme={theme}>
            <IntegrationNotistack/>
        </ThemeProvider>
    )
}