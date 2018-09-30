
import cert_scanner.util.certificate_scanner_utility as \
    certificate_scanner_utility

import datetime as dt
import mock
import pytest
import pandas as pd


def test_month_names():
    any_september_date = dt.datetime(year=2018, month=9, day=3)

    expected_months_data = \
        [{'expiry_month': 'Sep'},
         {'expiry_month': 'Oct'},
         {'expiry_month': 'Nov'},
         {'expiry_month': 'Dec'},
         {'expiry_month': 'Jan'},
         {'expiry_month': 'Feb'},
         {'expiry_month': 'Mar'},
         {'expiry_month': 'Apr'},
         {'expiry_month': 'May'},
         {'expiry_month': 'Jun'},
         {'expiry_month': 'Jul'},
         {'expiry_month': 'Aug'}]
    expected_months_df = pd.DataFrame(expected_months_data)
    actual_months_df = \
        certificate_scanner_utility.create_month_name_data_frame(
            any_september_date)
    pd.testing.assert_frame_equal(expected_months_df, actual_months_df)
