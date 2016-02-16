# landsat8-qa
Landsat 8 QA band CLI tool and python lib

## Background

The QA Band for the Landsat 8 Level 1 product packs ten spatial variables into a single 16bit GeoTiff band. See section 5.4 of the [L8 Users Handbook](http://landsat.usgs.gov/documents/Landsat8DataUsersHandbook.pdf):

<img width="586" alt="screen shot 2015-11-09 at 9 07 20 am" src="https://cloud.githubusercontent.com/assets/1151287/11034401/b46bdf94-86c1-11e5-9df2-f39627f5373b.png">

The single-bit variables are simple binary variables
```
0 = no
1 = yes
```

The two-bit versions allow for a bit more subtlety:
```
 00 = "Not Determined" = For Cloud or Cirrus, the algorithm did not run. For the other confidence classifications this is a "No"; the Algorithm has no confidence that this condition exists.
 01 = "No" = Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
 10 = "Maybe" = Algorithm has medium confidence that this condition exists (34- 66 percent confidence)
 11 = "Yes" = Algorithm has high confidence that this condition exists (67-100 percent confidence).
```

## Installation

No release yet, install from master

```
pip install git+https://github.com/mapbox/landsat8-qa.git@master#egg=landsat8-qa
```

## Command Line Interface

Get summary stats, representing proportion of the scene
```
$ rio l8qa LC81100752015319LGN00_BQA.TIF
{
  "clouds": {
    "maybe": 0.00238,
    "notDetermined": 0.295914,
    "yes": 0.174949,
    "no": 0.526757
  },
  "snow_ice": {
    "notDetermined": 1.0,
    "yes": 0.0
  },
  "cloud_shadow": {
    "notDetermined": 1.0
  },
  "terrain": {
    "no": 1.0
  },
  "water": {
    "maybe": 8.2e-05,
    "notDetermined": 0.999918
  },
  "dropped_frame": {
    "no": 1.0
  },
  "cirrus": {
    "notDetermined": 0.295914,
    "yes": 0.245638,
    "no": 0.458448
  },
  "fill": {
    "yes": 0.295914,
    "no": 0.704086
  }
}
```

Optionally, you can also output tifs for each QA topic to a directory
```
$ rio l8qa -o /tmp/qa LC81100752015319LGN00_BQA.TIF
...
QA variables written as uint8 tifs to /tmp/l8qa

$ ls /tmp/l8qa
LC81100752015319LGN00_cirrus.TIF
LC81100752015319LGN00_cloud_shadow.TIF
LC81100752015319LGN00_clouds.TIF
LC81100752015319LGN00_dropped_frame.TIF
LC81100752015319LGN00_fill.TIF
LC81100752015319LGN00_snow_ice.TIF
LC81100752015319LGN00_terrain.TIF
LC81100752015319LGN00_water.TIF
```
