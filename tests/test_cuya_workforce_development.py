from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import BOARD, PASSED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cuya_workforce_development import (
    CuyaWorkforceDevelopmentSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "cuya_workforce_development.html"),
    url="http://bc.cuyahogacounty.us/en-US/Workforce-Development.aspx",
)
test_detail_response = file_response(
    join(dirname(__file__), "files", "cuya_workforce_development_detail.html"),
    url="http://bc.cuyahogacounty.us/en-US/081619-WD-Board-Meeting.aspx",
)
spider = CuyaWorkforceDevelopmentSpider()

freezer = freeze_time("2019-09-17")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]
parsed_item = [item for item in spider._parse_detail(test_detail_response)][0]

freezer.stop()


def test_count():
    assert len(parsed_items) == 3


def test_title():
    assert parsed_item["title"] == "Board Meetings “Retreat”"


def test_description():
    assert parsed_item["description"] == ""


def test_start():
    assert parsed_item["start"] == datetime(2019, 8, 16, 8, 0)


def test_end():
    assert parsed_item["end"] == datetime(2019, 8, 16, 13, 0)


def test_time_notes():
    assert parsed_item["time_notes"] == ""


def test_id():
    assert (
        parsed_item["id"]
        == "cuya_workforce_development/201908160800/x/board_meetings_retreat_"
    )


def test_status():
    assert parsed_item["status"] == PASSED


def test_location():
    assert parsed_item["location"] == {
        "name": "",
        "address": "6161 Oak Tree Boulevard, Independence, OH 44131",
    }


def test_source():
    assert (
        parsed_item["source"]
        == "http://bc.cuyahogacounty.us/en-US/081619-WD-Board-Meeting.aspx"
    )


def test_links():
    assert parsed_item["links"] == [
        {
            "href": "http://bc.cuyahogacounty.us/ViewFile.aspx?file=yC5L9gSioQoiqlSvaiowPg%3d%3d",  # noqa
            "title": "Minutes",
        },
        {
            "href": "http://bc.cuyahogacounty.us/ViewFile.aspx?file=yC5L9gSioQps7O0IXojwYQ%3d%3d",  # noqa
            "title": "Agenda",
        },
    ]


def test_classification():
    assert parsed_item["classification"] == BOARD


def test_all_day():
    assert parsed_item["all_day"] is False
