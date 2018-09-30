import cert_scanner.util.file_name_utility as file_name_utility
import cert_scanner.system.pipeline_configuration as \
    pipeline_configuration
import os


def generate(output_directory,
             all_certs_df,
             relevant_certs_df,
             start_date,
             end_date):

    file_name = \
        file_name_utility.get_time_range_file_name("summary_report",
                                                   None,
                                                   start_date,
                                                   end_date,
                                                   'txt')
    file_path = os.path.join(output_directory, file_name)

    with open(file_path, 'a') as output_file:
        write_report_title(output_file)
        write_reporting_time_frame(output_file, start_date, end_date)


def write_report_title(output_file):
    today = file_name_utility.get_current_date()
    report_title = \
        "Summary Report for Cert Scan Run at {}\n\n".format(
            today.strftime(pipeline_configuration.TIME_STAMP_FORMAT))
    output_file.write(report_title)

def write_reporting_time_frame(output_file, start_date, end_date):
    time_frame_message = \
        "Certs Expiring between {} and {}\n\n".format(
            start_date.strftime(pipeline_configuration.TIME_STAMP_FORMAT),
            end_date.strftime(pipeline_configuration.TIME_STAMP_FORMAT))
    output_file.write(time_frame_message)
