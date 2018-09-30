import cert_scanner.util.file_name_utility as file_name_utility

import datetime as dt
import mock
import pytest


def test_get_dated_file_name():
    """
    Correctly generates a file name or diretory name that is appended with
    current date
    """
    sample_date = dt.datetime(year=2015, month=10, day=15)
    file_name_utility.get_current_date = \
        mock.MagicMock(return_value=sample_date)
    file_name = file_name_utility.get_dated_file_name('my_directory')
    assert "my_directory_2015-10-15" == file_name


def test_get_dated_file_name_errors():
    """
    Raises an exception if call to get dated file name is passed a null
    base file name
    """
    with pytest.raises(ValueError) as ex:
        file_name_utility.get_dated_file_name(None)
    assert "The base file name cannot be null" in str(ex)


def test_get_period_file_name_valid_period_types():
    """
    Correctly generates file names for valid period types.  These include
    daily, week, monthly.
    """
    end_date = dt.datetime(year=2015, month=10, day=31)

    # Generate daily file name
    actual_daily_file_name = \
        file_name_utility.get_period_file_name('idp_reports',
                                               'idp1',
                                               'daily',
                                               end_date,
                                               'csv')
    expected_daily_file_name = "idp_reports_idp1_daily_2015-10-31.csv"
    assert expected_daily_file_name == actual_daily_file_name

    # Generate week file name
    actual_week_file_name = \
        file_name_utility.get_period_file_name('idp_reports',
                                               'idp1',
                                               'week',
                                               end_date,
                                               'csv')
    expected_week_file_name = \
        "idp_reports_idp1_week_2015-10-25_2015-10-31.csv"
    assert expected_week_file_name == actual_week_file_name

    # Generate monthly file name
    actual_monthly_file_name = \
        file_name_utility.get_period_file_name('idp_reports',
                                               'idp1',
                                               'monthly',
                                               end_date,
                                               'csv')
    expected_monthly_file_name = \
        "idp_reports_idp1_monthly_2015-10-01_2015-10-31.csv"
    assert expected_monthly_file_name == actual_monthly_file_name


def test_get_period_file_name_no_segment():
    """
    Correctly generates a file name if no segment is specified
    """
    end_date = dt.datetime(year=2015, month=10, day=31)
    actual_week_file_name = \
        file_name_utility.get_period_file_name('idp_reports',
                                               'idp1',
                                               'week',
                                               end_date,
                                               'csv')
    expected_week_file_name = \
        "idp_reports_idp1_week_2015-10-25_2015-10-31.csv"
    assert expected_week_file_name == actual_week_file_name


def test_get_period_file_name_no_end_date():
    """
    Correctly generates file name for a call to get period file name when
    the end date has not been specified.  By default, it should assume that
    the current date is used.
    """
    sample_date = dt.datetime(year=2015, month=10, day=31)
    file_name_utility.get_current_date = \
        mock.MagicMock(return_value=sample_date)
    actual_week_file_name = \
        file_name_utility.get_period_file_name('idp_reports',
                                               'idp1',
                                               'week',
                                               None,
                                               'txt')
    expected_week_file_name = \
        "idp_reports_idp1_week_2015-10-25_2015-10-31.txt"
    assert expected_week_file_name == actual_week_file_name


def test_get_period_file_name_no_file_extension():
    """
    Correctly generates a file name for a call to get period file name when
    no file extension is specified.  By default it should use 'csv'
    """
    sample_date = dt.datetime(year=2015, month=10, day=31)
    file_name_utility.get_current_date = \
        mock.MagicMock(return_value=sample_date)
    actual_week_file_name = \
        file_name_utility.get_period_file_name('idp_reports',
                                               'idp1',
                                               'week',
                                               None)
    expected_week_file_name = \
        "idp_reports_idp1_week_2015-10-25_2015-10-31.csv"
    assert expected_week_file_name == actual_week_file_name


def test_get_period_file_name_invalid_period_type_error():
    """
    Raises an exception if the period type is None or not recognised
    """
    end_date = dt.datetime(year=2015, month=10, day=31)
    with pytest.raises(ValueError) as ex:
        file_name_utility.get_period_file_name('idp_reports',
                                               'idp1',
                                               'blah',
                                               end_date,
                                               'csv')
    expected_error_message = 'blah is not an accepted period type.'
    assert expected_error_message in str(ex)

    with pytest.raises(ValueError) as ex:
        file_name_utility.get_period_file_name('idp_reports',
                                               'idp1',
                                               None,
                                               end_date,
                                               'csv')
    assert "Period type cannot be null." in str(ex)


def test_get_period_file_name_null_base_file_error():
    """
    Correctly generates exceptions for call to get period file name if
    the base file name or the period type is None
    """
    end_date = dt.datetime(year=2015, month=10, day=31)
    with pytest.raises(ValueError) as ex:
        file_name_utility.get_period_file_name(None,
                                               'idp1',
                                               'daily',
                                               end_date,
                                               'csv')
    assert "The base file name cannot be null." in str(ex)


def test_get_time_range_file_name_valid_dates():
    """
    Call to get time range correctly generates file name when given a
    base file name, a segment, valid start and end dates and a file extension
    """
    start_date = dt.datetime(year=2015, month=10, day=28)
    end_date = dt.datetime(year=2015, month=10, day=31)

    actual_file_name = \
        file_name_utility.get_time_range_file_name('idp_reports',
                                                   'idp1',
                                                   start_date,
                                                   end_date,
                                                   'txt')
    expected_file_name = \
        "idp_reports_idp1_range_2015-10-28_2015-10-31.txt"
    assert expected_file_name == actual_file_name


def test_get_time_range_file_name_no_segment():
    """
    Call to get time range correctly generates a file name if no segment is
    specified
    """
    start_date = dt.datetime(year=2015, month=10, day=28)
    end_date = dt.datetime(year=2015, month=10, day=31)

    actual_file_name = \
        file_name_utility.get_time_range_file_name('idp_reports',
                                                   None,
                                                   start_date,
                                                   end_date,
                                                   'txt')
    assert "idp_reports_range_2015-10-28_2015-10-31.txt" == actual_file_name


def test_get_time_range_no_file_extension():
    """
    Call to get time range correctly generates a file name if no file
    extension is specified.  By default it should use csv
    """
    start_date = dt.datetime(year=2015, month=10, day=28)
    end_date = dt.datetime(year=2015, month=10, day=31)

    actual_file_name = \
        file_name_utility.get_time_range_file_name('idp_reports',
                                                   'idp1',
                                                   start_date,
                                                   end_date)
    expected_file_name = \
        'idp_reports_idp1_range_2015-10-28_2015-10-31.csv'
    assert expected_file_name == actual_file_name


def test_get_time_range_file_name_invalid_date_errors():

    start_date = dt.datetime(year=2015, month=10, day=31)
    end_date = dt.datetime(year=2015, month=10, day=15)

    with pytest.raises(ValueError) as ex:
        file_name_utility.get_time_range_file_name('idp_reports',
                                                   'idp1',
                                                   None,
                                                   end_date,
                                                   'csv')
    assert "start date cannot be null." in str(ex)

    with pytest.raises(ValueError) as ex:
        file_name_utility.get_time_range_file_name('idp_reports',
                                                   'idp1',
                                                   start_date,
                                                   None,
                                                   'csv')
    assert "end date cannot be null." in str(ex)

    with pytest.raises(ValueError) as ex:
        file_name_utility.get_time_range_file_name('idp_reports',
                                                   'idp1',
                                                   start_date,
                                                   end_date,
                                                   'csv')
    expected_error_message = \
        ("start date 2015-10-31 cannot be greater than "
         "the end date 2015-10-15")
    assert expected_error_message in str(ex)
