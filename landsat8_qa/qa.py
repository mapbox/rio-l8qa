import os
import numpy as np
import rasterio


def _capture_bits(arr, b1, b2):
    width_int = int((b1 - b2 + 1) * "1", 2)
    return ((arr >> b2) & width_int).astype('uint8')

# 0 = not determined
# 1 = no
# 2 = maybe
# 3 = yes

def cloud_qa(arr):
    return _capture_bits(arr, 15, 14)


def cirrus_qa(arr):
    return _capture_bits(arr, 13, 12)


def snow_ice_qa(arr):
    return _capture_bits(arr, 11, 10)


def cloud_shadow_qa(arr):
    return _capture_bits(arr, 7, 6)


def water_qa(arr):
    return _capture_bits(arr, 5, 4)


# 1 bit qa bands: 0 = no, 1=yes

def terrain_qa(arr):
    return _capture_bits(arr, 2, 2)


def dropped_frame_qa(arr):
    return _capture_bits(arr, 1, 1)


def fill_qa(arr):
    return _capture_bits(arr, 0, 0)


qa_vars = {
    'clouds': cloud_qa,
    'cirrus': cirrus_qa,
    'cloud_shadow': cloud_shadow_qa,
    'water': water_qa,
    'snow_ice': snow_ice_qa,
    'terrain': terrain_qa,
    'dropped_frame': dropped_frame_qa,
    'fill': fill_qa
}


binary_vars = ('terrain', 'dropped_frame', 'fill')

def lookup(name, val):
    if name in binary_vars:
        if val == 0:
            return "No"
        else:
            return "Yes"
    else:
        if val == 0:
            return "Not Determined"
        elif val == 1:
            return "No"
        elif val == 2:
            return "Maybe"
        elif val == 3:
            return "Yes"


def summary_stats(arr, basename=None, outdir=None, profile=None):
    """Returns summary stats for QA variables
    Input is a 16bit 2D array from a Landasat 8 band

    Optional side effect: specify an outdir to write QA variables as uint8 tifs
    """
    stats = {}
    size = arr.size
    for name, func in qa_vars.items():
        data = func(arr)
        u, counts = np.unique(data, return_counts=True)
        u = [lookup(name, x) for x in u]
        counts = [round(x / float(size), 6) for x in counts]
        stats[name] = dict(zip(u, counts))

        # Optionally write the band to outdir as a uint8 tif
        if outdir and basename and profile:
            profile.update(dtype='uint8')
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            outpath = os.path.join(outdir, basename.replace('BQA', name))
            with rasterio.open(outpath, 'w', **profile) as dest:
                dest.write_band(1, data)

    return stats
