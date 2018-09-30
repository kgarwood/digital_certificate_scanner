import cert_scanner.pipeline_configuration as pipeline_configuration

import os

def generate(output_directory,
             all_certs_df,
             relevant_certs_df,
             start_date,
             end_date):

    file_name = \
        file_name_utility.get_time_range_file_name("summary",
                                                   None,
                                                   start_date,
                                                   end_date)
    output_file_path = os.path.join(output_directory, file_name)


    end_date_phrase = \
        end_date.strftime(pipeline_configuration.DATE_OUTPUT_FORMAT)

    with open(output_file_path, 'a') as output_file:
        output_file.write(
            "Total Certs Detected: {}".format(len(all_certs_df)))



def __write_all_certs_stats(all_certs_df, output_file):
    output_file.write("Properties of All Certificates\n")
    __write_file_extension_breakdown(all_certs_df, output_file)
    __write_cert_purpose_breakdown(df, output_file)





def __write_relevant_certs_stats(relevant_certs_df, output_file):
    output_file.write(
        "Total Certs Expiring Between {} and {}: {}".format(
        start_date.strftime(pipeline_configuration.DATE_OUTPUT_FORMAT),
        end_date.strftime(pipeline_configuration.DATE_OUTPUT_FORMAT),
        len(relevant_certs_df)))
    __write_file_extension_breakdown(relevant_certs_df, output_file)
    __write_cert_purpose_breakdown(df, output_file)


def __write_repository_list(target_directory, output_file):
    output_file.write(
        "The scan was applied at {} in the following repositories:\n".format(
            current_time))

    for root, directories, file_names in os.walk(target_directory):
        for file_name in file_names:
            if fnmatch.fnmatch(file_name, YML_FILTER):
                current_yml_path = os.path.join(root, file_name)
                current_yml_file_cert_lst = \
                    extract_cert_from_yml_file(
                        current_yml_path,
                        crt_from_file_path)
                cert_summary_dct_lst.extend(current_yml_file_cert_lst)


def __write_cert_purpose_breakdown(df, output_file):
    summary_purpose_type_df = \
        df['type'].value_counts().reset_index()
    summary_purpose_type_df = \
        summary_purpose_type_df.rename(columns={expiry_field_name: 'total_certs_per_purpose'})
    summary_purpose_type_df = \
        summary_purpose_type_df.rename(columns={'index': 'type'})
    summary_purpose_type_df = \
        summary_purpose_type_df.reset_index(drop=True)

    output_file.write("Expiring Certs by Purpose\n")
    for index, row in summary_purpose_type_df.iterrows():
        output_file.write("{}: {}".format(row['type'], row['total_certs_per_purpose']))


def __write_file_extension_breakdown(df, output_file):
    summary_file_extension_df = \
        df['file_extension_type'].value_counts().reset_index()
    summary_file_extension_df = \
        summary_file_extension_df.rename(columns={expiry_field_name: 'total_certs_of_file_type'})
    summary_file_extension_df = \
        summary_file_extension_df.rename(columns={'index': 'file_extension_type'})
    summary_file_extension_df = \
        summary_file_extension_df.reset_index(drop=True)

    output_file.write("Expiring Certs by File Extension\n")
    for index, row in summary_file_extension_df.iterrows():
        output_file.write("{}: {}".format(row['file_extension_type'], row['total_certs_of_file_type']))
