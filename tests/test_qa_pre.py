import pytest
import rasterio

from l8qa.qa_pre import summary_stats


@pytest.fixture
def qaarr_pre():
    with rasterio.open("tests/LC81070352015282LGN00_BQA.TIF") as src:
        arr = src.read(1)
    return arr


expected_pre = {
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


def test_summary_pre(qaarr_pre):
    assert summary_stats(qaarr_pre) == expected_pre
