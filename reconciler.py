import os
import time
from datetime import datetime

import numpy as np
import pandas as pd
from skrub import fuzzy_join


def remove_columns(df_1, df_2):
    keep_col1 = []
    keep_col2 = []
    keep_1 = keep_col1 + ['id_col']
    keep_2 = keep_col2 + ['id_col']
    df_1 = df_1[keep_1]
    df_2 = df_2[keep_2]


def create_id_col(df, columns):
    """Create a new column which is the join of the col_keys_1/2."""
    # df = df.fillna(value="NULL", columns=columns)
    df['id_col'] = np.array([""] * df.shape[0])
    for column in columns:
        df['id_col'] = df['id_col'] + "_" + df[column]
    return df


def complete_indicator_column(df: pd.DataFrame):
    def f(col1, col2):
        if col1 == col2:
            return 'both'
        elif not col1:
            return 'file2_only'
        elif not col2:
            return 'file1_only'
        else:
            return 'something went wrong'

    pd.options.mode.chained_assignment = None  # default='warn'
    df['origin_dataframe'] = df[['id_col_file1', 'id_col_file2']].apply(lambda x: f(*x), axis=1)
    pd.options.mode.chained_assignment = 'warn'  # default='warn'
    df = df.drop(['id_col_file1', 'id_col_file2'], axis=1)

    return df


def main():
    # TODO: Duplicated.
    col_keys_1 = ["Country"]
    col_keys_2 = ["Country Name"]

    # CUSTOM: Timer
    time_1 = time.time()

    df_1 = pd.read_csv("data/df_1.csv", index_col=0)
    df_2 = pd.read_csv("data/df_2.csv", index_col=0)

    df_1 = create_id_col(df_1, col_keys_1)
    df_2 = create_id_col(df_2, col_keys_2)
    remove_columns(df_1, df_2)

    [df_1.rename(columns={col_name: col_name + "_file1"}, inplace=True) for col_name in df_1.columns]
    [df_2.rename(columns={col_name: col_name + "_file2"}, inplace=True) for col_name in df_2.columns]

    df_merge_1 = fuzzy_join(
        df_1,
        df_2,
        left_on="id_col_file1",
        right_on="id_col_file2",
        max_dist=0.9,
        add_match_info=True,
    )
    df_merge_1 = df_merge_1.rename(columns={"id_col": "id_col_file1"})
    df_merge_2 = fuzzy_join(
        df_2,
        df_1,
        left_on="id_col_file2",
        right_on="id_col_file1",
        max_dist=0.9,
        add_match_info=True,
    )
    df_merge_2 = df_merge_2.rename(columns={"id_col": "id_col_file2"})

    df_concat = pd.concat([df_merge_1, df_merge_2])
    df_dedupe = df_concat.drop_duplicates()
    df = complete_indicator_column(df_dedupe)
    value_counts = df['origin_dataframe'].value_counts()

    if not os.path.exists("output"):
        os.makedirs("output")
    time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(f"output/{time_now}.csv")

    # CUSTOM: Timer
    time_2 = time.time()

    # CUSTOM: Timer
    print(f"Execution time: {time_2 - time_1} seconds")


if __name__ == "__main__":
    main()
