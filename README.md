HELLO

## Architecture
```
                                   [tle updater]
                                         |
[Receivers manager] <--socketio--> [NOAA receiver] ----> [NOAA output dir], --socketio--> [Receivers manager]
                                         |
                                       [SDR]

[NOAA output dir] ---->, [Receivers manager] --http--> [Web UI]

[Receivers manager] -> [NOAA receiver]:
    tle, noaa config, main config, pass time

[NOAA receiver] -> [Receivers manager]:
    pass result

[Receivers manager] :
    src: ./manager
    functionality:
        Calculate/Get schedule
        Calling the satellite receiver at the start of the passage
        Config managment
        Output data managment
    request:
        get_next_pass(sat_name) -> next_pass
        get_receiver_config(sat_type) -> receiver_config
        get_all_satellites -> List[(sat_type, sat_name)]
        get_satellites -> List[(sat_type, sat_name)]
        get_dirs -> tle_dir, output_dir

[pass] : 
    sat_type
    sat_name
    time_start
    time_end
    duration

[NOAA receiver] :
    src: ./receivers/NOAA
    functionality:
        Decode data from [SDR] (SDR -> Images)

```

## Satellites
 - [ ] **NOAA**
 - [ ] **Meteor**

## Output dir
```
<path to output>/<satellite type>/<satellite name>/<datetime>/<satellite data>
```

## Configuration

## Manual Installation 

