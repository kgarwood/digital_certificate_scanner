import cert_scanner.util.file_name_utility as file_name_utility
import cert_scanner.system.pipeline_configuration as pipeline_configuration
import cert_scanner.util.certificate_scanner_utility as \
    certificate_scanner_utility
import cert_scanner.report.progress_graph_generator as \
    progress_graph_generator

import os


"""
This module has routines that generate graphs and spreadsheets for reports
that show monthly and weekly breakdowns of these expiring certificate
attributes:
(1)  certificates: the number of expiring certs
(2)  releases: the number of releases needed to process all the files
     that contain a certificate
(3)  locations: the number of file locations that contain an expiring
     certificate.

Note that the number of locations and releases represent an upper bound
because they may overlap.  For example, a file may contain two
expiring certificates but in the results, the same file will be counted
twice even though it might be changed onced to fix both expiring certs.

Similarly, the changes needed to the same file may be counted in
separate releases even though making all the changes to it once may only
warrant one rather than two releases.
"""


def generate_weekly_reports(output_directory,
                            weekly_expiration_metrics_df,
                            start_date,
                            end_date):

    # Write out the spreadsheet
    spreadsheet_file_name = \
        file_name_utility.get_time_range_file_name('weekly_results',
                                                   None,
                                                   start_date,
                                                   end_date)
    spreadsheet_file_path = \
        os.path.join(output_directory, spreadsheet_file_name)
    certificate_scanner_utility.write_csv(weekly_expiration_metrics_df,
                                          spreadsheet_file_path)

    # Write out the graph
    graph_file_name = \
        file_name_utility.get_time_range_file_name('weekly_results',
                                                   None,
                                                   start_date,
                                                   end_date,
                                                   'png')
    graph_file_path = os.path.join(output_directory, graph_file_name)

    progress_graph_generator.generate(weekly_expiration_metrics_df,
                                      output_directory,
                                      'weekly',
                                      'expiry_week',
                                      'Week',
                                      start_date,
                                      end_date,
                                      3)


def generate_monthly_reports(output_directory,
                             monthly_expiration_metrics_df,
                             start_date,
                             end_date):

    file_name = \
        file_name_utility.get_time_range_file_name('monthly_results',
                                                   None,
                                                   start_date,
                                                   end_date)
    output_file_path = os.path.join(output_directory, file_name)

    certificate_scanner_utility.write_csv(monthly_expiration_metrics_df,
                                          output_file_path)

    # Write out the graph
    graph_file_name = \
        file_name_utility.get_time_range_file_name('monthly_results',
                                                   None,
                                                   start_date,
                                                   end_date,
                                                   'png')
    graph_file_path = os.path.join(output_directory, graph_file_name)

    progress_graph_generator.generate(monthly_expiration_metrics_df,
                                      output_directory,
                                      'monthly',
                                      'expiry_month',
                                      'Month',
                                      start_date,
                                      end_date,
                                      2)
