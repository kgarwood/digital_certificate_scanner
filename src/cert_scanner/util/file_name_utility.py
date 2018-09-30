import cert_scanner.system.pipeline_configuration as pipeline_configuration
import datetime as dt
import dateutil.relativedelta as rd

PERIOD_TYPES = ['daily', 'week', 'monthly']
"""
A collection of functions that are used to create consistent names that
are used to produce various parts of a pipeline run.
"""


def get_dated_file_name(base_file_name, file_extension=None):
    __validate_base_file_name(base_file_name)

    current_date = get_current_date()
    file_name = \
        base_file_name + '_' + \
        current_date.strftime(pipeline_configuration.DATE_OUTPUT_FORMAT)
    if file_extension is not None:
        file_name = file_name + '.' + file_extension
    return file_name.lower()


def get_period_file_name(base_file_name, segment, period_type,
                         date, file_extension='csv'):

    __validate_base_file_name(base_file_name)
    __validate_period_type(period_type)

    end_date = date
    if end_date is None:
        end_date = get_current_date()

    date_phrase = get_period_date_range_phrase(period_type, end_date)
    return __generate_file_name(base_file_name, segment, period_type,
                                date_phrase, file_extension)


def get_time_range_file_name(base_file_name, segment, start_date,
                             end_date, file_extension='csv'):

    __validate_base_file_name(base_file_name)
    __validate_date_range(start_date, end_date)
    date_phrase = get_date_range_phrase(start_date, end_date)

    return __generate_file_name(base_file_name, segment, 'range',
                                date_phrase, file_extension)


def get_current_date():
    return dt.datetime.now().date()


def __validate_base_file_name(base_file_name):
    if base_file_name is None:
        raise ValueError('The base file name cannot be null.')


def __validate_period_type(period_type):
    if period_type is None:
        raise ValueError('Period type cannot be null.')
    if period_type not in PERIOD_TYPES:
        error_message = \
            '{} is not an accepted period type.'.format(period_type)
        raise ValueError(error_message)


def __validate_date_range(start_date, end_date):
    if start_date is None:
        raise ValueError('start date cannot be null.')
    if end_date is None:
        raise ValueError('end date cannot be null.')
    if start_date > end_date:
        error_template = \
            'start date {} cannot be greater than the end date {}'
        start_date_phrase = \
            start_date.strftime(pipeline_configuration.DATE_OUTPUT_FORMAT)
        end_date_phrase = \
            end_date.strftime(pipeline_configuration.DATE_OUTPUT_FORMAT)
        error_message = \
            error_template.format(start_date_phrase, end_date_phrase)
        raise ValueError(error_message)


def __generate_file_name(base_file_name, segment, period_type,
                         date_phrase, file_extension):
    file_name = base_file_name
    if segment is not None:
        file_name = file_name + '_' + segment
    if period_type is not None:
        file_name = file_name + '_' + period_type
    file_name = file_name + '_' + date_phrase
    if file_extension is not None:
        file_name = file_name + "." + file_extension
    return file_name.lower()


def get_period_date_range_phrase(period_type, end_date=None):
    start_date = None
    if period_type == 'daily':
        start_date = end_date
    elif period_type == 'week':
        start_date = end_date - rd.relativedelta(weeks=1) + \
                     rd.relativedelta(days=1)
    else:
        # Assume monthly
        start_date = end_date - rd.relativedelta(months=1) + \
                     rd.relativedelta(days=1)

    date_range_phrase = get_date_range_phrase(start_date, end_date)
    return date_range_phrase


def get_date_range_phrase(start_date, end_date):
    phrase = None
    start_date_phrase = \
        start_date.strftime(pipeline_configuration.DATE_OUTPUT_FORMAT)
    if start_date == end_date:
        return start_date_phrase

    end_date_phrase = \
        end_date.strftime(pipeline_configuration.DATE_OUTPUT_FORMAT)
    phrase = \
        start_date_phrase + '_' + end_date_phrase
    return phrase
