import datetime
from dateutil.relativedelta import relativedelta
import os


"""
Generates a report showing all of the certificates which expired
at latest the day before the cert scanner program was run.
"""


def generate(certificates_df, output_directory_path):

    today = datetime.datetime.now()
    file_name = \
        'dead_cert_report-{}.txt'.format(today.strftime("%d-%b-%Y"))
    output_file_path = os.path.join(output_directory_path, file_name)

    yesterday = today - relativedelta(days=1)
    dead_certificates_df = \
        certificates_df[certificates_df['expiry_date'] <= yesterday]

    dead_certificate_file_paths = set()
    for index, row in dead_certificates_df.iterrows():
        file_paths = row['locations']
        dead_certificate_file_paths = \
            dead_certificate_file_paths.union(file_paths)

    with open(output_file_path, 'a') as output_file:
        header_message = ('There are {} files which contain certificates '
                          'that are dead as of {}.\n')
        output_file.write(header_message.format(
            len(dead_certificate_file_paths),
            today.strftime("%d-%b-%Y")))

        for file_path in dead_certificate_file_paths:
            output_file.write("{}\n".format(file_path))
