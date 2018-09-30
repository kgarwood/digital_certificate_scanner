import datetime as dt
import mock
import pytest
import pandas as pd
from cert_scanner.transform.main_transformation import \
    get_results_by_week
from cert_scanner.transform.main_transformation import \
    get_results_by_month
from cert_scanner.util.data_frame_comparator_utility import compare_data_sets


def get_test_cert_records():
    # 2018-03-03: is on Month Mar
    # 2018-03-04: is on Month Mar
    # 2018-06-04: is on Month Jun
    test_data = \
        [{'expiry_date': dt.datetime(year=2018, month=3, day=3),
          'num_locations': 10,
          'num_releases': 3},
         {'expiry_date': dt.datetime(year=2018, month=3, day=4),
          'num_locations': 10,
          'num_releases': 3},
         {'expiry_date': dt.datetime(year=2018, month=6, day=4),
          'num_locations': 10,
          'num_releases': 3}]
    test_df = pd.DataFrame(test_data)
    return test_df


def test_aggregate_results_by_week():

    start_date = dt.datetime(year=2018, month=1, day=1)
    # 2018-03-03: is on Week 9
    # 2018-03-04: is on Week 9
    # 2018-06-04: is on Week 23
    test_data = get_test_cert_records()
    test_df = pd.DataFrame(test_data)

    expected_results_data = \
        [{'expiry_week': '09',
          'total_locations': 20,
          'total_releases': 6,
          'total_expiring_certs': 2},
         {'expiry_week': '23',
          'total_locations': 10,
          'total_releases': 3,
          'total_expiring_certs': 1}]
    expected_results_df = pd.DataFrame(expected_results_data)

    actual_results_df = get_results_by_week(start_date, test_df)
    # For convenience, filter out all the rows where there are no weekly
    # results
    actual_results_df = \
        actual_results_df[actual_results_df['total_locations'] > 0]

    compare_data_sets(expected_results_df, actual_results_df, 'expiry_week',
                      ['expiry_week', 'total_locations', 'total_releases'])


def test_aggregate_results_by_month():

    start_date = dt.datetime(year=2018, month=1, day=1)
    test_df = get_test_cert_records()

    expected_results_data = \
        [{'expiry_month': 'Mar',
          'total_locations': 20,
          'total_releases': 6,
          'total_expiring_certs': 2},
         {'expiry_month': 'Jun',
          'total_locations': 10,
          'total_releases': 3,
          'total_expiring_certs': 1}]
    expected_results_df = pd.DataFrame(expected_results_data)

    actual_results_df = get_results_by_month(start_date, test_df)
    # For convenience, filter out all the rows where there are no weekly
    # results
    actual_results_df = \
        actual_results_df[actual_results_df['total_locations'] > 0]

    compare_data_sets(expected_results_df, actual_results_df, 'expiry_month',
                      ['expiry_month', 'total_locations', 'total_releases'])
