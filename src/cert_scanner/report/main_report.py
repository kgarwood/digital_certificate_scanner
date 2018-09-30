import cert_scanner.report.temporal_reports as temporal_reports
import cert_scanner.report.certificate_expiry_spreadsheet as \
    certificate_expiry_spreadsheet
import cert_scanner.report.dead_certificate_report as dead_certificate_report
import cert_scanner.report.detailed_certificate_report as \
    detailed_certificate_report
import cert_scanner.report.summary_certificate_report as \
    summary_certificate_report

import os
import shutil



def generate_reports(configuration_manager,
                     all_certs_df,
                     relevant_certs_df,
                     weekly_expiration_metrics_df,
                     monthly_expiration_metrics_df,
                     start_date,
                     end_date):

    output_directory = configuration_manager.reports_output_directory

    if os.path.exists(output_directory) and os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory)

    dead_certificate_report.generate(relevant_certs_df,
                                     output_directory)
    temporal_reports.generate_weekly_reports(output_directory,
                                             weekly_expiration_metrics_df,
                                             start_date,
                                             end_date)
    temporal_reports.generate_monthly_reports(output_directory,
                                              monthly_expiration_metrics_df,
                                              start_date,
                                              end_date)

    certificate_expiry_spreadsheet.generate_cert_expiration_reports(
        output_directory,
        relevant_certs_df,
        start_date,
        end_date)

    summary_certificate_report.generate(output_directory,
                                        all_certs_df,
                                        relevant_certs_df,
                                        start_date,
                                        end_date)

    detailed_certificate_report.generate(configuration_manager,
                                         output_directory,
                                         relevant_certs_df,
                                         start_date,
                                         end_date)

    print("Reports have been generated in {}\n\n".format(output_directory))
