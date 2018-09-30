import cert_scanner.util.file_name_utility as file_name_utility
import cert_scanner.util.certificate_scanner_utility as \
    certificate_scanner_utility

import os


def generate_cert_expiration_reports(output_directory,
                                     original_df,
                                     start_date,
                                     end_date):

    file_name = \
        file_name_utility.get_time_range_file_name("cert_expirations",
                                                   None,
                                                   start_date,
                                                   end_date)
    file_path = os.path.join(output_directory, file_name)

    df = original_df.copy()
    df = df[['days_left',
             'expiry_date',
             'environment',
             'type',
             'serial_number',
             'certificate_authority',
             'organisation_name',
             'status',
             'num_locations',
             'num_releases']]

    sort_columns = ['days_left', 'num_locations']
    sort_directions = [True, False]
    df = df.sort_values(by=sort_columns, ascending=sort_directions)

    certificate_scanner_utility.write_csv(df, file_path)
