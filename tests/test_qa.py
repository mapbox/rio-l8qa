import pytest
import rasterio


@pytest.fixture
def qaarr():
    with rasterio.open("tests/LC81070352015282LGN00_BQA.TIF") as src:
        arr = src.read(1)
    return arr

expected = {
    "droppedFrame": {
        "no": 1.0
    },
    "clouds": {
        "maybe": 0.003105,
        "yes": 0.013599,
        "notDetermined": 0.335058,
        "no": 0.648238
    },
    "terrain": {
        "no": 1.0
    },
    "water": {
        "maybe": 0.414231,
        "notDetermined": 0.585769
    },
    "cloudShadow": {
        "notDetermined": 1.0
    },
    "snowIce": {
        "yes": 0.000358,
        "notDetermined": 0.999642
    },
    "cirrus": {
        "yes": 1.6e-05,
        "notDetermined": 0.335058,
        "no": 0.664927
    },
    "fill": {
        "yes": 0.335058,
        "no": 0.664942
    }
}


def test_summary(qaarr):
    from landsat8_qa.qa import summary_stats
    assert summary_stats(qaarr) == expected
