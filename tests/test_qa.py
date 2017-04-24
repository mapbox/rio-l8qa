import pytest
import rasterio

from l8qa.qa import summary_stats


@pytest.fixture
def qaarr():
    with rasterio.open("tests/LC08_L1TP_005004_20170410_20170414_01_T1_BQA.TIF") as src:
        arr = src.read(1)
    return arr


expected = {
    "terrain": {
        "no": 1.0
    },
    "cloud": {
        "no": 0.999995,
        "yes": 5e-06
    },
    "snowIceConf": {
        "notDetermined": 0.513239,
        "no": 0.005215,
        "yes": 0.481546
    },
    "cloudConf": {
        "notDetermined": 0.513239,
        "maybe": 0.000119,
        "no": 0.486637,
        "yes": 5e-06
    },
    "radiometricSaturation": {
        "notDetermined": 1.0
    },
    "fill": {
        "no": 0.486761,
        "yes": 0.513239
    },
    "cloudShadowConf": {
        "notDetermined": 0.513239,
        "no": 0.486757,
        "yes": 5e-06
    },
    "cirrusConf": {
        "notDetermined": 0.513239,
        "no": 0.486161,
        "yes": 0.000601
    }
}


def test_summary(qaarr):
    assert summary_stats(qaarr) == expected
