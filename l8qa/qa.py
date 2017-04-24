"""
QA files for Landsat 8 OLI/TIRS Collection 1 Quality Band

https://landsat.usgs.gov/sites/default/files/images/C1-L4-5-7-8_QA_attributeTables.JPG

***********
* WARNING *
***********
This will not work with the previous L8 pre-Collection qa bands. See qa_L8.py instead.
"""
import os
import numpy as np
import rasterio
from rasterio.transform import guard_transform


def _capture_bits(arr, b1, b2):
    width_int = int((b1 - b2 + 1) * "1", 2)
    return ((arr >> b2) & width_int).astype('uint8')


def fill_qa(arr):
    """
    0 = No, this condition does not exist
    1 = Yes, this condition exists
    """
    return _capture_bits(arr, 0, 0)


def terrain_qa(arr):
    """
    0 = No, this condition does not exist
    1 = Yes, this condition exists
    """
    return _capture_bits(arr, 1, 1)


def radiometric_qa(arr):
    """
    For radiometric saturation bits (2-3), read from left to right
    represent how many bands contain saturation:

    00 - No bands contain saturation
    01 - 1-2 bands contain saturation
    10 - 3-4 bands contain saturation
    11 - 5 or more bands contain saturation
    """
    return _capture_bits(arr, 3, 2)


def cloud(arr):
    """
    0 = No, this condition does not exist
    1 = Yes, this condition exists
    """
    return _capture_bits(arr, 4, 4)


def cloud_confidence(arr):
    """
    00 = "Not Determined" = Algorithm did not determine the status of this condition
    01 = "No" = Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
    10 = "Maybe" = Algorithm has medium confidence that this condition exists (34-66 percent confidence)
    11 = "Yes" = Algorithm has high confidence that this condition exists (67-100 percent confidence
    """
    return _capture_bits(arr, 6, 5)


def cloud_shadow_confidence(arr):
    """
    00 = "Not Determined" = Algorithm did not determine the status of this condition
    01 = "No" = Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
    10 = "Maybe" = Algorithm has medium confidence that this condition exists (34-66 percent confidence)
    11 = "Yes" = Algorithm has high confidence that this condition exists (67-100 percent confidence
    """
    return _capture_bits(arr, 8, 7)


def snow_ice_confidence(arr):
    """
    00 = "Not Determined" = Algorithm did not determine the status of this condition
    01 = "No" = Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
    10 = "Maybe" = Algorithm has medium confidence that this condition exists (34-66 percent confidence)
    11 = "Yes" = Algorithm has high confidence that this condition exists (67-100 percent confidence
    """
    return _capture_bits(arr, 10, 9)


def cirrus_confidence(arr):
    """
    00 = "Not Determined" = Algorithm did not determine the status of this condition
    01 = "No" = Algorithm has low to no confidence that this condition exists (0-33 percent confidence)
    10 = "Maybe" = Algorithm has medium confidence that this condition exists (34-66 percent confidence)
    11 = "Yes" = Algorithm has high confidence that this condition exists (67-100 percent confidence
    """
    return _capture_bits(arr, 12, 11)


qa_vars = {
    'fill': fill_qa,
    'terrain': terrain_qa,
    'radiometricSaturation': radiometric_qa,
    'cloud': cloud,
    'cloudConf': cloud_confidence,
    'cirrusConf': cirrus_confidence,
    'cloudShadowConf': cloud_shadow_confidence,
    'snowIceConf': snow_ice_confidence,
}


binary_vars = ('terrain', 'cloud', 'fill')


def lookup(name, val):
    if name in binary_vars:
        if val == 0:
            return "no"
        return "yes"
    else:
        if val == 0:
            return "notDetermined"
        elif val == 1:
            return "no"
        elif val == 2:
            return "maybe"
        elif val == 3:
            return "yes"


def write_cloud_mask(arr, profile, cloudmask, threshold=2):
    """
    writes the cloud+alpha mask as single-band uint8 tiff
    suitable for stacking as an alpha band
    threshold defaults to 2; only 2 and above are considered clouds
    """
    func = qa_vars['cloud']
    data = func(arr)
    profile.update(dtype='uint8')
    profile.update(transform=guard_transform(profile['transform']))
    with rasterio.open(cloudmask, 'w', **profile) as dest:
        # clouds = (data >= threshold)
        # nodata = (data == 0)
        # yesdata = ((clouds + nodata) == 0)
        data = (data * 255).astype('uint8')
        dest.write(data, 1)


def summary_stats(arr, basename=None, outdir=None, profile=None, cloudmask=None):
    """Returns summary stats for QA variables
    Input is a 16bit 2D array from a Landasat 8 band

    Optional side effects:
        write QA variables as uint8 tifs to outdir
        write binary clouds as uint8 0/255 to cloudmask
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
