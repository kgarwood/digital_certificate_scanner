import cert_scanner.util.certificate_scanner_utility as \
    certificate_scanner_utility

import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
"""
Contains all the code that either derives new fields, filters records
or aggregates them.
"""


def enhance_and_filter_certificates(configuration_manager,
                                    all_certs_df,
                                    start_date,
                                    end_date):
    """
    Derive more information about each certificate and filter them
    based on whether they're expiring within the date range (a year)
    Then aggregate the certificate record summaries by month and week.
    These data sets will inform work estimate graphs.
    """
    results_df = \
        derive_additional_cert_metadata(
            configuration_manager,
            all_certs_df)
    results_df = \
        filter_certs_by_time_frame(results_df,
                                   end_date)

    date_range_phrase = \
        certificate_scanner_utility.generate_date_range_phrase(start_date,
                                                               end_date)

    print(('Of all {} x509 certificates, '
           '{} will expire between '
           '{}\n\n').format(len(all_certs_df),
                            len(results_df),
                            date_range_phrase))

    return results_df


def derive_additional_cert_metadata(configuration_manager, certs_df):
    df = certs_df.copy()
    df = derive_releases_for_affected_files(configuration_manager, df)
    df = derive_location_and_release_counts(df)
    df = derive_environment(configuration_manager, df)
    df = derive_status(configuration_manager, df)
    df = derive_certificate_type(configuration_manager, df)
    return df


def derive_releases_for_affected_files(configuration_manager, original_df):
    df = original_df.copy()
    df['num_locations'] = None
    df['num_releases'] = None
    for index, row in df.iterrows():
        loc = row['locations']

        df.at[index, 'num_locations'] = len(row['locations'])
        df.at[index, 'required_releases'] = \
            get_required_releases(configuration_manager, row['locations'])
        df.at[index, 'num_releases'] = len(row['required_releases'])

    return df

def derive_certificate_type(configuration_manager, original_df):
    df = original_df.copy()
    df['type'] = None
    for index, row in df.iterrows():
        loc = row['locations']
        df.at[index, 'type'] = \
            configuration_manager.determine_certificate_type(row['certificate_authority'])
    return df

def derive_environment(configuration_manager, original_df):
    df = original_df.copy()
    df['environment]'] = None

    for index, row in df.iterrows():
        locations = row['locations']
        df.at[index, 'environment'] = \
            configuration_manager.determine_environment(
                row['certificate_authority'],
                locations)
    return df


def derive_status(configuration_manager, original_df):
    df = original_df.copy()
    today = datetime.datetime.now()
    one_week_from_now = today + relativedelta(weeks=1)
    one_month_from_now = today + relativedelta(months=1)

    for index, row in df.iterrows():
        df.at[index, 'status'] = \
            __determine_status_message(configuration_manager,
                                       today,
                                       one_week_from_now,
                                       one_month_from_now,
                                       row['expiry_date'],
                                       row['locations'])
    return df

def __determine_status_message(configuration_manager,
                               today,
                               one_week_from_now,
                               one_month_from_now,
                               expiry_date,
                               locations):

    if expiry_date < today:
        return 'EXPIRED'
    elif __is_referenced(configuration_manager, locations) is False:
        return 'UNREFERENCED'
    elif expiry_date <= one_week_from_now:
        return 'URGENTLY EXPIRING'
    elif expiry_date <= one_month_from_now:
        return 'EXPIRING'
    else:
        return 'HEALTHY'

def __is_referenced(configuration_manager, locations):
    appears_in_main_cert_directory = False
    appears_in_at_least_one_other_repo = False

    for file_path in locations:
        if configuration_manager.is_in_main_certificate_directory(file_path):
            appears_in_main_cert_directory = True
        else:
            appears_in_at_least_one_other_repo = True

    return(appears_in_main_cert_directory and appears_in_at_least_one_other_repo)


def __derive_environment(certificate_authority, locations_lst):
    for file_path in locations_lst:
        canonical_file_path = file_path.upper()

        if 'TEST' in canonical_file_path:
            return 'non-prod'
        if 'INTEGRATION' in canonical_file_path:
            return 'non-prod'
        if 'PROD' in canonical_file_path:
            return 'prod'
        if 'IDAP_ROOT_CA' in canonical_file_path:
            return 'prod'

    if 'TEST' in certificate_authority:
        return 'non-prod'
    if 'NON-PROD' in certificate_authority:
        return 'non-prod'
    if 'PROD' in certificate_authority:
        return 'prod'

    return 'unknown'

def get_required_releases(configuration_manager, locations):
    results = set()
    for file_path in locations:
        release_command = \
            configuration_manager.get_release_for_file(file_path)
        if release_command is not None:
            results.add(release_command)
    return results

def derive_location_and_release_counts(original_df):
    df = original_df.copy()
    df['num_locations'] = None
    df['num_releases'] = None
    for index, row in df.iterrows():
        loc = row['locations']
        df.at[index, 'num_locations'] = len(row['locations'])
        df.at[index, 'num_releases'] = len(row['required_releases'])

    return df

def filter_certs_by_time_frame(original_df,
                               end_date):
    df = original_df.copy()
    df = df[df['expiry_date'] <= end_date]
    return df


def get_results_by_week(start_date, original_df):
    df = original_df.copy()
    weeks_df = \
        certificate_scanner_utility.create_week_name_data_frame(start_date)
    df['expiry_week'] = df['expiry_date'].dt.strftime('%W')
    return aggregate_results('expiry_week', df, weeks_df)


def get_results_by_month(start_date, original_df):
    df = original_df.copy()
    months_df = \
        certificate_scanner_utility.create_month_name_data_frame(start_date)
    df['expiry_month'] = df['expiry_date'].dt.strftime('%b')
    return aggregate_results('expiry_month', df, months_df)


def aggregate_results(expiry_field_name, original_df, time_period_names_df):
    df = original_df.copy()
    summary_num_locations_df = df[[expiry_field_name, 'num_locations']]
    summary_num_locations_df = \
        summary_num_locations_df.groupby(expiry_field_name,
                                         as_index=False).sum()
    summary_num_locations_df = \
        summary_num_locations_df.rename(
            columns={'num_locations': 'total_locations'})

    summary_num_releases_df = df[[expiry_field_name, 'num_releases']]
    summary_num_releases_df = \
        summary_num_releases_df.groupby(expiry_field_name,
                                        as_index=False).sum()
    summary_num_releases_df = \
        summary_num_releases_df.rename(
            columns={'num_releases': 'total_releases'})

    summary_num_certs_df = \
        df[expiry_field_name].value_counts().reset_index()
    summary_num_certs_df = \
        summary_num_certs_df.rename(
            columns={expiry_field_name: 'total_expiring_certs'})
    summary_num_certs_df = \
        summary_num_certs_df.rename(columns={'index': expiry_field_name})
    summary_num_certs_df = \
        summary_num_certs_df.reset_index(drop=True)

    results_df = \
        pd.merge(time_period_names_df, summary_num_certs_df,
                 how='left', on=[expiry_field_name])

    results_df = \
        pd.merge(results_df, summary_num_releases_df,
                 how='left', on=[expiry_field_name])
    results_df = \
        pd.merge(results_df, summary_num_locations_df,
                 how='left', on=[expiry_field_name])

    results_df.fillna(0, inplace=True)
    results_df['total_expiring_certs'] = \
        results_df['total_expiring_certs'].astype(int)
    results_df['total_releases'] = results_df['total_releases'].astype(int)
    results_df['total_locations'] = results_df['total_locations'].astype(int)

    return results_df
