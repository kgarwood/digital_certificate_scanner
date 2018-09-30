import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

"""
Contains various functions that are typically to do with date
calculations or formatting date results.  It also contains a routine
that helps combine all the file paths where an x509 certificate may
appear.
"""


def calculate_date_range():
    today_date = get_today()
    start_date = find_next_monday(today_date)
    end_date = start_date + relativedelta(years=1)
    return(start_date, end_date)

def generate_date_range_phrase(start_date, end_date):
    return "{} to {}".format(start_date.strftime("%d %b %Y"),
                             end_date.strftime("%d %b %Y"))

def get_today():
    return datetime.datetime.now()


def find_next_monday(date):
    today_weekday = date.weekday()
    next_monday_start_date = None
    if today_weekday == 0:
        # current day is current Monday
        next_monday_start_date = date
    else:
        # current day occurs after current Monday
        next_monday_start_date = \
            date + datetime.timedelta(7 - today_weekday)
    return next_monday_start_date


def create_week_name_data_frame(start_date):
    next_monday_date = find_next_monday(start_date)
    week_lst = []
    for i in range(0, 52):
        current_date = next_monday_date + relativedelta(weeks=i)
        week_number = str(current_date.isocalendar()[1]).zfill(2)
        week_lst.append(week_number)
    weeks_df = pd.DataFrame(week_lst)
    weeks_df.columns = ['expiry_week']
    return weeks_df


def create_month_name_data_frame(start_date):
    month_lst = []
    for i in range(12):
        current_date = start_date + relativedelta(months=i)
        month_lst.append(current_date.strftime('%b'))
    months_df = pd.DataFrame(month_lst)
    months_df.columns = ['expiry_month']
    return months_df


def create_cert_from_identifier_dct(cert_summary_dct_lst):
    """
    Uses a list of certificate_summary_records that are produced by the
    cert_summary_factory and creates a collection of unique certs.  When the
    same cert is found in multiple files, this routine will combine all of
    the locations in different records so that the resulting collection of
    unique certs will include all of the locations they appear.
    """
    cert_from_identifier_dct = dict()
    for cert_summary_dct in cert_summary_dct_lst:
        identifier = cert_summary_dct['serial_number']
        if identifier in cert_from_identifier_dct:
            locations_set = cert_summary_dct['locations']
            cert_from_identifier_dct[identifier]['locations'] = \
                cert_from_identifier_dct[identifier]['locations'].union(
                locations_set)
        else:
            cert_from_identifier_dct[identifier] = cert_summary_dct

    return cert_from_identifier_dct


def write_csv(df, file_path):
    df.to_csv(
        file_path,
        sep=',',
        index=False,
        index_label=True,
        encoding='utf-8')
