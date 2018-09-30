
import cert_scanner.util.certificate_scanner_utility as \
    certificate_scanner_utility
import cert_scanner.util.data_frame_comparator_utility as \
    data_frame_comparator_utility
import datetime as dt
import mock
import pytest
import pandas as pd


def test_week_names():

    # September 3 is on week 36.  The next week will therefore
    # be on week 37
    any_september_date = dt.datetime(year=2018, month=9, day=7)

    expected_weeks_data = \
        ['37', '38', '39', '40', '41',
         '42', '43', '44', '45', '46',
         '47', '48', '49', '50', '51',
         '52', '01', '02', '03', '04',
         '05', '06', '07', '08', '09',
         '10', '11', '12', '13', '14',
         '15', '16', '17', '18', '19',
         '20', '21', '22', '23', '24',
         '25', '26', '27', '28', '29',
         '30', '31', '32', '33', '34',
         '35', '36']

    expected_weeks_df = pd.DataFrame(expected_weeks_data)
    expected_weeks_df.columns = ['expiry_week']
    actual_weeks_df = \
        certificate_scanner_utility.create_week_name_data_frame(
            any_september_date)
    pd.testing.assert_frame_equal(expected_weeks_df, actual_weeks_df)
