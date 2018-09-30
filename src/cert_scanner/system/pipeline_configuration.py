"""
Maintains settings which are treated as constants by the rest of
the pipeline.  Most of the settings refer to:
    - which date format should be used for file names and the time
      stamp format used in logging.
    - the names of directories that appear when the pipelines are run
    - standardised parameter values for CSV file processing
"""
DATE_OUTPUT_FORMAT = '%Y-%m-%d'
TIME_STAMP_FORMAT = '%b %d, %Y %H.%M.%S'
CSV_DELIMITER = '\t'
CSV_ENCODING = 'utf-8'
PIPELINE_RUNS_DIRECTORY = './pipeline_runs'
PIPELINE_ARCHIVES_DIRECTORY = './pipeline_archives'
CODE_DIRECTORY = 'src'
RESULTS_DIRECTORY = 'results'
SNAPSHOTS_DIRECTORY = 'snapshots'
LOGS_DIRECTORY = 'logs'
ARCHIVE_DIRECTORY = 'archive'
