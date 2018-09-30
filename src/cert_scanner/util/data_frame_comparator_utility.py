import pandas as pd
"""
A convenience function used to help ensure that when two data sets are
compared that their rows and columns are in the same order
"""


def compare_data_sets(expected_results_df, actual_results_df, sort_column,
                      ordered_columns):

    expected_results_df = expected_results_df[ordered_columns]
    expected_results_df = expected_results_df.sort_values(by=sort_column,
                                                          ascending=True)
    expected_results_df = expected_results_df.reset_index(drop=True)

    actual_results_df = actual_results_df[ordered_columns]
    actual_results_df = actual_results_df.sort_values(by=sort_column,
                                                      ascending=True)
    actual_results_df = actual_results_df.reset_index(drop=True)

    pd.testing.assert_frame_equal(expected_results_df, actual_results_df)
