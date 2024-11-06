import random

import pandas as pd
from skrub.datasets import fetch_world_bank_indicator

CUSTOM_AUGMENT_TIMES = 10


def CUSTOM_augment(df, noise_cols, times=CUSTOM_AUGMENT_TIMES):
    # Duplicate each row 'times' number of times
    df = pd.concat([df] * times, ignore_index=True)

    # for noise_col in noise_cols:
    #     for i in df.index:
    #         # Generate a random number between min_count and max_count
    #         num_asterisks = random.randint(1, 10)
    #         # Create a string with the generated number of asterisks
    #         asterisks_string = '*' * num_asterisks
    #         df.loc[i, noise_col] = df.loc[i, noise_col] + asterisks_string

    print(f"DataFrame augmented: len(df) = {len(df)}")
    return df


def CUSTOM_create_datasets():
    df_1 = pd.read_csv(
        (
            "https://raw.githubusercontent.com/skrub-data/datasets/"
            "master/data/Happiness_report_2022.csv"
        ),
        thousands=",",
    )
    df_1.drop(df_1.tail(1).index, inplace=True)
    df_1 = df_1.head(100)

    df_2 = fetch_world_bank_indicator(indicator_id="NY.GDP.PCAP.CD").X
    df_2 = df_2.head(100)
    
    # TODO: Duplicated.
    col_keys_1 = ["Country"]
    col_keys_2 = ["Country Name"]
    
    df_1 = CUSTOM_augment(df_1, col_keys_1)
    df_2 = CUSTOM_augment(df_2, col_keys_2)
    
    df_1.to_csv("data/df_1.csv")
    df_2.to_csv("data/df_2.csv")
    
    return df_1, df_2


if __name__ == "__main__":
    CUSTOM_create_datasets()
