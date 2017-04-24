## Background

The QA Band for the Landsat 8 product packs multiple spatial variables into a single 16bit GeoTiff band. There are two formats we need to handle:

### Collection 1 productions

This module support the LC08 collection 1 QA band format described here: https://landsat.usgs.gov/collectionqualityband

<img width="886" src="img/collection1-bit.jpg">


### L8 level 1 products

**WARNING** this legacy format is deprecated and only available through the `qa_L8.py` module. These won't currently work with the command line interface.

See section 5.4 of the [L8 Users Handbook](http://landsat.usgs.gov/documents/Landsat8DataUsersHandbook.pdf):

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



