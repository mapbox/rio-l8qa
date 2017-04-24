# rio-l8qa

Landsat 8 QA band CLI tool and python module

## Install

```
$ pip install rio-l8qa
```

*The command line interface currently works only with new Landsat collections format. See `docs/collections.md` for details.*


## Command Line Usage

Summary statistics for each of the QA metrics

```
$ rio l8qa LC08_L1TP_005004_20170410_20170414_01_T1_BQA.TIF \
    --stats
{
  "cloudConf": {
    "maybe": 0.000119,
    "yes": 5e-06,
    "no": 0.486637,
    "notDetermined": 0.513239
  },
  ...
}
```

To generate output tifs for each QA metric to a directory
```
$ rio l8qa LC08_L1TP_005004_20170410_20170414_01_T1_BQA.TIF \
    --outdir /tmp
$ ls /tmp
/tmp/LC08_L1TP_005004_20170410_20170414_01_T1_cirrusConf.TIF
/tmp/LC08_L1TP_005004_20170410_20170414_01_T1_cloud.TIF
/tmp/LC08_L1TP_005004_20170410_20170414_01_T1_cloudConf.TIF
/tmp/LC08_L1TP_005004_20170410_20170414_01_T1_cloudShadowConf.TIF
/tmp/LC08_L1TP_005004_20170410_20170414_01_T1_fill.TIF
/tmp/LC08_L1TP_005004_20170410_20170414_01_T1_radiometricSaturation.TIF
/tmp/LC08_L1TP_005004_20170410_20170414_01_T1_snowIceConf.TIF
/tmp/LC08_L1TP_005004_20170410_20170414_01_T1_terrain.TIF
```

If you need a uint8 0-255 cloud mask, suitable for use as an alpha band in an RGBA geotif, there is a shortcut
```
$ rio l8qa LC08_L1TP_005004_20170410_20170414_01_T1_BQA.TIF \
    --cloudmask /tmp/justclouds.tif
```

## Python Usage

```
from l8qa.qa import cloud_confidence
import rasterio

qatif = "LC08_L1TP_005004_20170410_20170414_01_T1_BQA.TIF"

with rasterio.open(qatif) as src:
    yesclouds = cloud_confidence(src.read(1), ) == 3  # high confidence
```


