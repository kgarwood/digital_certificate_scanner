import cert_scanner.util.file_name_utility as file_name_utility

import os

"""
This module generates a text file that contains the subject and body of
e-mail messages which describe each expiring certificate.  The report is
designed to be num_releases
"""


def generate(configuration_manager,
             output_directory,
             original_df,
             start_date,
             end_date):

    df = original_df.copy()
    sort_columns = ['days_left', 'num_locations']
    sort_directions = [True, False]
    df = df.sort_values(by=sort_columns, ascending=sort_directions)

    # In future, this list of email message records could be used to do
    # automated e-mails that are sent to zendesk.
    email_message_record_lst = []
    for index, row in df.iterrows():
        email_message_record_lst.append(
            create_email_message_record(configuration_manager, row))

    # For now, write the e-mail messages to file
    write_email_message_records_to_file(output_directory,
                                        start_date,
                                        end_date,
                                        email_message_record_lst)


def create_email_message_record(configuration_manager, row):
    email_message_dct = dict()

    # Create the Subject field
    if row['days_left'] >= 0:
        email_message_dct['subject'] = \
            "Cert {} expires in {} days on {}".format(
                row['certificate_authority'],
                row['days_left'],
                row['expiry_date'])
    else:
        email_message_dct['subject'] = \
            "Cert {} expired {} days ago on {}".format(
                row['certificate_authority'],
                row['days_left'],
                row['expiry_date'])

    environment_field = "Environment:{}\n".format(row['environment'])
    certificate_type_field = "Certificate Type:{}\n".format(row['type'])
    status_type_field = "Status: {}\n".format(row['status'])
    organisation_field = "Organisation:{}\n".format(row['organisation_name'])
    serial_number_field = "Serial Number:{}\n".format(row['serial_number'])
    certificate_authority_field = \
        "Certificate Authority:{}\n".format(row['certificate_authority'])
    locations_section = "Locations ({})\n".format(row['num_locations']) + \
                        "---------------\n"
    for file_path in row['locations']:
        locations_section = locations_section + file_path + "\n\n"

    releases_header = 'Releases ({})\n'.format(row['num_releases']) + \
                      '---------------\n'
    releases_header = releases_header + \
        configuration_manager.release_instructions

    all_releases = ""
    for release_command in row['required_releases']:
        all_releases = all_releases + release_command + "\n\n"

    releases_section = "{}\n{}".format(releases_header, all_releases)

    email_message_dct['body'] = \
        "{}{}{}{}{}{}{}".format(environment_field,
                              certificate_type_field,
                              status_type_field,
                              organisation_field,
                              serial_number_field,
                              locations_section,
                              releases_section)

    return email_message_dct

    return overall_email_message_text


def write_email_message_records_to_file(output_directory,
                                        start_date,
                                        end_date,
                                        email_message_record_lst):
    file_name = \
        file_name_utility.get_time_range_file_name("detailed_expired_certs",
                                                   None,
                                                   start_date,
                                                   end_date,
                                                   'txt')
    file_path = os.path.join(output_directory, file_name)

    email_message_template = \
        ("-------------------------------------------------------\n"
         "Subject:{}\nMessage Body:\n{}"
         "-------------------------------------------------------\n")

    with open(file_path, 'a') as output_file:
        for email_message_record in email_message_record_lst:
            email_message = \
                email_message_template.format(email_message_record['subject'],
                                              email_message_record['body'])
            output_file.write(email_message)
