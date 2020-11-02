HELLO

## Architecture
```
[Receivers manager] <--http--> [NOAA receiver] ----> [NOAA output dir], --http--> [Receivers manager]
                                      |
                                    [SDR]

[NOAA output dir] ---->, [Receivers manager] --http--> [Web UI]


[Receivers manager] :
    src: ./manager
    functionality:
        Calculate/Get schedule
        Calling the satellite receiver at the start of the passage
        Config managment

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
<path to output>/<satellite type>/<satellite name>/<date>/<satellite data>
```

## Configuration

## Manual Installation 

