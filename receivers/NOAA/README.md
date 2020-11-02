# NOAA receiver 

## Pipeline

```
[SDR] --> [rtl_fm] --raw--> [sox] --wav--> [wxtoimg] --images--> [python process] ----> OUT
```


## Output files

```
<path to output>/NOAA/<satellite name>/<date>/image/<images>
<path to output>/NOAA/<satellite name>/<date>/wav/<wavs>
<path to output>/NOAA/<satellite name>/<date>/temp/<>
```
