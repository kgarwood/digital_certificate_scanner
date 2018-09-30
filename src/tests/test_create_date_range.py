import cert_scanner.util.certificate_scanner_utility as \
    certificate_scanner_utility

import datetime as dt
import mock
import pytest


def test_current_day_is_current_monday():
    current_monday_date = dt.datetime(year=2018, month=9, day=3)

    certificate_scanner_utility.get_today = \
        mock.MagicMock(return_value=current_monday_date)
    start_date, end_date = certificate_scanner_utility.calculate_date_range()

    expected_start_date = dt.datetime(year=2018, month=9, day=3)
    expected_end_date = dt.datetime(year=2019, month=9, day=3)

    assert start_date == expected_start_date
    assert end_date == expected_end_date


def test_current_day_after_current_monday():
    current_tuesday_date = dt.datetime(year=2018, month=9, day=4)

    certificate_scanner_utility.get_today = \
        mock.MagicMock(return_value=current_tuesday_date)
    start_date, end_date = certificate_scanner_utility.calculate_date_range()

    expected_start_date = dt.datetime(year=2018, month=9, day=10)
    expected_end_date = dt.datetime(year=2019, month=9, day=10)

    assert start_date == expected_start_date
    assert end_date == expected_end_date
