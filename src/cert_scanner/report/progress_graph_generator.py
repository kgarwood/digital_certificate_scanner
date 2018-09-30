import cert_scanner.util.file_name_utility as file_name_utility
import cert_scanner.util.certificate_scanner_utility as \
    certificate_scanner_utility

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os


def generate(original_df,
             expiry_type,
             expiry_period_field_name,
             expiry_period_phrase,
             start_date,
             end_date,
             output_directory):

    title_date_phrase = \
        "from {} to {}\n({} {} to Week {})".format(
                start_date.strftime("%d %b %Y"),
                end_date.strftime("%d %b %Y"),
                expiry_period_phrase,
                start_date.strftime("%W %Y"),
                expiry_period_phrase,
                end_date.strftime("%W %Y"))

    __generate_num_certs_graph(original_df,
                               output_directory,
                               expiry_type,
                               expiry_period_field_name,
                               expiry_period_phrase,
                               start_date,
                               end_date)

    __generate_num_releases_graph(original_df,
                                  output_directory,
                                  expiry_type,
                                  expiry_period_field_name,
                                  expiry_period_phrase,
                                  start_date,
                                  end_date)

    __generate_num_locations_graph(original_df,
                                   output_directory,
                                   expiry_type,
                                   expiry_period_field_name,
                                   expiry_period_phrase,
                                   start_date,
                                   end_date)


def __generate_num_locations_graph(original_df,
                                   output_directory,
                                   expiry_type,
                                   expiry_period_field_name,
                                   expiry_period_phrase,
                                   start_date,
                                   end_date):

    title_date_phrase = \
        __generate_title_phrase(start_date, end_date, expiry_period_phrase)
    num_locations_title = \
        "Number of Files Containing Expiring Certs\n{}".format(
            title_date_phrase)

    period_to_period_phrase = \
        __generate_period_to_period_phrase(expiry_type,
                                           start_date,
                                           end_date,
                                           expiry_period_phrase)
    num_locations_title = \
        "Expiring Cert Files {}".format(period_to_period_phrase)
    date_to_date_phrase = \
        certificate_scanner_utility.generate_date_range_phrase(start_date,
                                                               end_date)


    ax = original_df.plot.bar(x=expiry_period_field_name,
                              y='total_locations', width=1.0, rot=0)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(labelsize=8)
    legend = ax.legend()
    legend.remove()

    plt.suptitle(num_locations_title, fontsize=14)
    plt.title(date_to_date_phrase, fontsize=10)

    plt.setp(ax.get_xticklabels()[::2], visible=False)
    plt.setp(ax.get_xticklabels()[::2], visible=False)
    plt.setp(ax.get_xticklabels(), rotation=0, horizontalalignment='center')
    plt.xlabel('Expiry {}'.format(expiry_period_phrase))
    plt.ylabel('Total Files')

    base_file_name = "total_{}_locations".format(expiry_type)
    file_name = \
        file_name_utility.get_time_range_file_name(base_file_name,
                                                   None,
                                                   start_date,
                                                   end_date,
                                                   "png")
    output_file_path = os.path.join(output_directory, file_name)
    plt.savefig(output_file_path)


def __generate_num_certs_graph(original_df,
                               output_directory,
                               expiry_type,
                               expiry_period_field_name,
                               expiry_period_phrase,
                               start_date,
                               end_date):

    period_to_period_phrase = \
        __generate_period_to_period_phrase(expiry_type,
                                           start_date,
                                           end_date,
                                           expiry_period_phrase)
    num_certs_title = \
        "Expiring Cert Records {}".format(period_to_period_phrase)
    date_to_date_phrase = \
        certificate_scanner_utility.generate_date_range_phrase(start_date,
                                                               end_date)


    ax = original_df.plot.bar(x=expiry_period_field_name,
                              y='total_expiring_certs', width=1.0, rot=0)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    legend = ax.legend()
    legend.remove()

    ax.tick_params(labelsize=8)

    plt.suptitle(num_certs_title, fontsize=14)
    plt.title(date_to_date_phrase, fontsize=10)

    plt.setp(ax.get_xticklabels()[::2], visible=False)
    plt.setp(ax.get_xticklabels(), rotation=0, horizontalalignment='center')
    plt.xlabel('Expiry {}'.format(expiry_period_phrase))
    plt.ylabel('Total Certificates')

    base_file_name = "total_{}_certs".format(expiry_type)
    file_name = \
        file_name_utility.get_time_range_file_name(base_file_name,
                                                   None,
                                                   start_date,
                                                   end_date,
                                                   "png")
    output_file_path = os.path.join(output_directory, file_name)
    plt.savefig(output_file_path)


def __generate_num_releases_graph(original_df,
                                  output_directory,
                                  expiry_type,
                                  expiry_period_field_name,
                                  expiry_period_phrase,
                                  start_date,
                                  end_date):

    period_to_period_phrase = \
        __generate_period_to_period_phrase(expiry_type,
                                           start_date,
                                           end_date,
                                           expiry_period_phrase)
    num_releases_title = \
        "Expiring Cert Releases {}".format(period_to_period_phrase)
    date_to_date_phrase = \
        certificate_scanner_utility.generate_date_range_phrase(start_date,
                                                               end_date)
    ax = \
        original_df.plot.bar(x=expiry_period_field_name,
                             y='total_releases',
                             width=1.0,
                             rot=0)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(labelsize=8)
    legend = ax.legend()
    legend.remove()

    plt.suptitle(num_releases_title, fontsize=14)
    plt.title(date_to_date_phrase, fontsize=10)

    plt.setp(ax.get_xticklabels()[::2], visible=False)
    plt.setp(ax.get_xticklabels(),
             rotation=0,
             horizontalalignment='center')
    plt.xlabel('Expiry {}'.format(expiry_period_phrase))
    plt.ylabel('Total Releases')

    base_file_name = "total_{}_releases".format(expiry_type)
    file_name = \
        file_name_utility.get_time_range_file_name(base_file_name,
                                                   None,
                                                   start_date,
                                                   end_date,
                                                   "png")
    output_file_path = os.path.join(output_directory, file_name)
    plt.savefig(output_file_path)


def __generate_title_phrase(start_date,
                            end_date,
                            expiry_period_phrase):
    title_date_phrase = \
        "from {} to {}\n({} {} to Week {})".format(
                start_date.strftime("%d %b %Y"),
                end_date.strftime("%d %b %Y"),
                expiry_period_phrase,
                start_date.strftime("%W %Y"),
                expiry_period_phrase,
                end_date.strftime("%W %Y"))
    return title_date_phrase


def __generate_period_to_period_phrase(expiry_type,
                                       start_date,
                                       end_date,
                                       expiry_period_phrase):
    if expiry_type == 'monthly':
        return "({} to {})".format(
                start_date.strftime("%b %Y"),
                end_date.strftime("%b %Y"))
    else:
        return "(Week {} to Week {})".format(
                start_date.strftime("%W %Y"),
                end_date.strftime("%W %Y"))




def __generate_date_range_phrase(period_phrase, start_date, end_date):
    return "from {} to {}\n({} {} to {} {})".format(
                start_date.strftime("%d %b %Y"),
                end_date.strftime("%d %b %Y"),
                period_phrase,
                start_date.strftime("%W %Y"),
                period_phrase,
                end_date.strftime("%W %Y"))
