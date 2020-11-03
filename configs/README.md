# Configuration files description 

## Main config file
```json
{
    "output_directory": "<path to output>",
    "tle_directory": "./tle",
    "tle_sources": [
        "https://celestrak.com/NORAD/elements/weather.txt",
        "https://celestrak.com/NORAD/elements/amateur.txt"
    ],
    "tle_update_period" : 86400,
    "station_name" : "Test1",
    "station_location": {
        "lat" : 0,
        "lon" : 0,
        "alt" : 0
    },
    "satellites": {
        "NOAA":{
            "NOAA 15" : {
                "freq": 137.62,
                "priority": 1
            }
        }
    }
}
```
## Satellites configs
```
<path to configs>/satellites/<satellite type>/<configs>
```


## NOAA Config
```json 
{
    "radio" {
        "dongle_gain" : 50,
        "bias_tee" : "enable_bias_tee"
    }
}
```