"""
J. Chanenson
2/17/24
"""

import pandas as pd
import numpy as np
import random

def count_rows_until_duplicate_in_column(df, column_name):
    """
    Count the number of rows until a duplicate value is encountered in a specified column of a DataFrame.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame.
    - column_name (str): The name of the column to analyze.

    Returns:
    - dict: A dictionary containing the shortest interval for each unique value in the specified column.
    """

    # Initialize an empty dictionary to store the last index where each value was seen
    last_index = {}

    # Initialize an empty dictionary to store the counts
    counts = {}

    # Iterate over the rows in the specified column
    for index, value in enumerate(df[column_name]):
        # Check if the value has been seen before
        if value in last_index:
            # Calculate the interval since the last occurrence
            interval = index - last_index[value]

            # Update the count if the interval is shorter
            if value not in counts or interval < counts[value]:
                counts[value] = interval

        # Update the last index where the value was seen
        last_index[value] = index

    # Find the key with the minimum value (lowest interval)
    min_interval_key = min(counts, key=counts.get)
    lowest_interval = counts[min_interval_key]

    # Print the lowest interval and corresponding value before returning the counts
    print(f"Lowest Interval in Column '{column_name}': {lowest_interval} for Value '{min_interval_key}'")

    return counts


def random_insert_rows(truncated_df, rows_to_insert, min_cold_call_interval = 4):
    """
    Randomly inserts rows from another DataFrame into a specified domain within the original DataFrame.

    Parameters:
    - truncated_df (pd.DataFrame): The original DataFrame where rows will be inserted.
    - rows_to_insert (pd.DataFrame): The DataFrame containing names to be inserted.
    - min_cold_call_interval (int): The minimum interval from both the top and bottom of the original DataFrame,
      within which rows will be randomly inserted.

    Returns:
    pd.DataFrame: A new DataFrame with rows inserted at random positions within the specified domain.
    """
    # Calculate domain start and end indices
    domain_start = min_cold_call_interval
    domain_end = len(truncated_df) - min_cold_call_interval

    # Generate random indices within the specified domain
    random_indices = np.random.randint(domain_start, domain_end, len(rows_to_insert))

    # Sort the indices to insert rows in the correct order
    random_indices.sort()

    # Insert the rows from the other DataFrame into the original DataFrame
    for i, index in enumerate(random_indices):
        truncated_df = pd.concat([truncated_df.iloc[:index + i], rows_to_insert.iloc[i:i + 1], truncated_df.iloc[index + i:]]).reset_index(drop=True)

    return truncated_df



def create_long_list(original_df, n, m):
    """
    Create a long list by duplicating and shuffling the original DataFrame, resolving duplicates at seams,
    and moving duplicates elsewhere in the list.

    Parameters:
    - original_df (pandas.DataFrame): The original DataFrame to be duplicated and shuffled.
    - n (int): Number of times to duplicate the original DataFrame.
    - m (int): Number of elements to consider at the seams for resolving duplicates.

    Returns:
    long_df (pandas.DataFrame): The resulting long df after the duplication, shuffling, and resolving duplicates process.
    """

    # Step 1: Duplicate rows in the original DataFrame n times
    duplicated_dfs_list = [original_df.copy() for _ in range(n)]

    # Step 2: Shuffle each of the n DataFrames independently
    for df in duplicated_dfs_list:
        df.apply(random.shuffle, axis=1)

    # Step 3: Find duplicates within m at the seams between DataFrame n-1 and n for all DataFrames
    for i in range(1, n):
        bottom_of_prev_df = duplicated_dfs_list[i-1].iloc[:, -m:]
        top_of_current_df = duplicated_dfs_list[i].iloc[:, :m]

        common_duplicates = set(bottom_of_prev_df.values.flatten()).intersection(top_of_current_df.values.flatten())

        for duplicate in common_duplicates:
            # Drop rows in the DataFrame where bottom_of_prev_df/top_of_current_df is a duplicate
            duplicated_dfs_list[i-1] = duplicated_dfs_list[i-1][~duplicated_dfs_list[i-1].iloc[:, -m:].isin([duplicate]).any(axis=1)]
            duplicated_dfs_list[i] = duplicated_dfs_list[i][~duplicated_dfs_list[i].iloc[:, :m].isin([duplicate]).any(axis=1)]

        # Step 4: Move duplicates elsewhere in the DataFrame
        duplicated_dfs_list[i] = random_insert_rows(duplicated_dfs_list[i-1], duplicated_dfs_list[i], common_duplicates, min_cold_call_interval=4)

    # Concatenate all the DataFrames into a df
    long_df = pd.concat(duplicated_dfs_list, axis=0, ignore_index=True).reset_index(drop=True)

    return long_df

if __name__ == "__main__":
    
    #Import 
    original_df = pd.read_csv('import_data.csv')  #TODO make robust to excell files and split 1st name last name fields
    
    # Generate
    n = 4   #TODO make these user input 
    m = 3
    export_df = create_long_list(original_df, n, m)

    # Check your work
    column_name = "Names" #TODO make robust
    count_rows_until_duplicate_in_column(export_df, column_name)
    
    export_df.to_csv("long", index=False, encoding='utf-8')