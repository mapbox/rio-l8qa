import rasterio

def _capture_bits(arr, b1, b2):
    width_int = int((b1 - b2 + 1) * "1", 2)
    return ((arr >> b2) & width_int).astype('uint8')

#
# 2 bit QA bands
# 0 = not determined
# 1 = no
# 2 = maybe
# 3 = yes
#

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

#
# 1 bit qa bands: 0 = no, 1=yes
#

def terrain_qa(arr):
    return _capture_bits(arr, 2, 2)


def dropped_frame_qa(arr):
    return _capture_bits(arr, 1, 1)


def fill_qa(arr):
    return _capture_bits(arr, 0, 0)


qa_rasters = {
    'clouds': cloud_qa,
    'cirrus': cirrus_qa,
    'cloud_shadow': cloud_shadow_qa,
    'water': water_qa,
    'snow_ice': snow_ice_qa,
    'terrain': terrain_qa,
    'dropped_frame': dropped_frame_qa,
    'fill': fill_qa
}


def unpack_qa_bands(tif):
    with rasterio.open(tif) as src:
        arr = src.read(1)
        profile = src.profile
        profile.update(dtype='uint8')

        for name, func in qa_rasters.items():
            outpath = qapath.replace('BQA', name)
            data = func(arr)
            with rasterio.open(outpath, 'w', **profile) as dest:
                dest.write_band(1, data)


if __name__ == "__main__":
    qapath = "LC80010522014288LGN00_BQA.TIF"
    unpack_qa_bands(qapath)
