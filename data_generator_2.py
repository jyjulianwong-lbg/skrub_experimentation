import random

import pandas as pd


def CUSTOM_augment(df, noise_cols, noise_strs):
    for noise_col in noise_cols:
        for i in df.index:
            # Randomly add noise to the end
            if random.randint(0, 1) == 1:
                noise_str_idx = random.randint(0, len(noise_strs) - 1)
                noise_str = noise_strs[noise_str_idx]
                df.loc[i, noise_col] = f"{df.loc[i, noise_col]}. {noise_str}."

            # Generate a random number between min_count and max_count
            num_asterisks = random.randint(0, 1)
            # Create a string with the generated number of asterisks
            asterisks_string = '*' * num_asterisks
            # Augment existing string with asterisks at the end
            df.loc[i, noise_col] = df.loc[i, noise_col] + asterisks_string

    print(f"DataFrame augmented: len(df) = {len(df)}")
    return df


def CUSTOM_create_datasets():
    # https://github.com/MartinStyk/quotes-recommender/blob/master/data/quotes_filtered_2.csv
    df = pd.read_csv("quotes.csv")
    df_1 = df.iloc[1000:2000, :]
    df_2 = df.iloc[1200:2200, :]
    noise_strs = df.iloc[:100, :]["text"].apply(lambda x: " ".join(x.split()[:5])).to_list()
    
    # TODO: Duplicated.
    col_keys_1 = ["text"]
    col_keys_2 = ["text"]
    
    df_1 = CUSTOM_augment(df_1, col_keys_1, noise_strs)
    df_2 = CUSTOM_augment(df_2, col_keys_2, noise_strs)
    
    df_1.to_csv("data/df_1.csv", index=False)
    df_2.to_csv("data/df_2.csv", index=False)
    
    return df_1, df_2


if __name__ == "__main__":
    CUSTOM_create_datasets()