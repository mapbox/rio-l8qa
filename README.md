# landsat8-qa
Landsat 8 QA band CLI tool and python lib

# TODO

Everything.

Proposed CLI:
```
# get summary stats
rio l8qa LC82310622015254LGN00_BQA.tif

# get summary stats and output tifs for each QA topic to the qastuff directory
rio l8qa LC82310622015254LGN00_BQA.tif -o qastuff
```

Proposed Python API:
* Funcs for `clouds(numpy_array) -> ndarray`, etc.
* `summary_stats(path_to_qa) -> dictionary`


