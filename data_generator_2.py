import random

import pandas as pd


def CUSTOM_augment(df, noise_cols, noise_strs):
    for noise_col in noise_cols:
        for i in df.index:
            # Randomly add noise to the end
            noise_str_idx = random.randint(0, len(noise_strs) - 1)
            noise_str = noise_strs[noise_str_idx]
            df.loc[i, noise_col] = f"{df.loc[i, noise_col]}. {noise_str}."

            # Generate a random number between min_count and max_count
            num_asterisks = random.randint(0, 3)
            # Create a string with the generated number of asterisks
            asterisks_string = '*' * num_asterisks
            # Augment existing string with asterisks at the end
            df.loc[i, noise_col] = df.loc[i, noise_col] + asterisks_string

    print(f"DataFrame augmented: len(df) = {len(df)}")
    return df


# Function to split text into sentences
def CUSTOM_augment_by_split_text(df):
    new_rows = []
    for index, row in df.iterrows():
        sentences = row['text'].split('. ')
        for sentence in sentences:
            if sentence:  # Avoid adding empty sentences
                new_rows.append({'text': row['categories'], 'author': row['author']})
                new_rows.append({'text': sentence.strip(), 'author': row['author']})
    new_df = pd.DataFrame(new_rows)
    print(f"DataFrame augmented: len(df) = {len(new_df)}")
    return new_df


def CUSTOM_create_datasets():
    # https://github.com/MartinStyk/quotes-recommender/blob/master/data/quotes_filtered_2.csv
    df = pd.read_csv("quotes.csv")
    df = CUSTOM_augment_by_split_text(df)
    # assert len(df) == 9344

    df_1 = df.copy().iloc[000:9000, :]
    df_2 = df.copy().iloc[200:9200, :]
    df_1["text"] = df_1["text"].apply(lambda x: " ".join(x.split()[:5])).to_list()
    df_2["text"] = df_2["text"].apply(lambda x: " ".join(x.split()[:5])).to_list()
    noise_strs = df.iloc[:100, :]["text"].apply(lambda x: " ".join(x.split()[:2])).to_list()
    
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