"""
J. Chanenson
2/17/24
"""

import pandas as pd
import numpy as np
import random
from pprint import pprint

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

def checkIndiciesInRange(original_df, truncated_df, final_df, min_cold_call_interval = 4):
    """
        Check if indices of elements in final_df['Names'] not present in truncated_df['Names']
        are within a specified range.

        Parameters:
        - truncated_df (pandas.DataFrame): The first DataFrame containing a 'Names' column.
        - final_df (pandas.DataFrame): The second DataFrame containing a 'Names' column.
        - min_cold_call_interval (int): The minimum interval to consider for index range.

        Returns:
        None
        """
    # Calculate domain start and end indices
    values_not_in_truncated_df = final_df[~final_df['Names'].isin(truncated_df['Names'])]

    # Specify the range of indices you want to check
    min_index = min_cold_call_interval
    max_index = len(final_df) - min_cold_call_interval

    # Check if all indices are within the specified range
    are_indices_within_range = all(min_index <= index <= max_index for index in values_not_in_truncated_df.index)

    # Check to make sure the new df has the same number of unique names 
    original_df_count = original_df['Names'].nunique() 
    final_df_count = final_df['Names'].nunique() 

    if are_indices_within_range and (final_df_count == original_df_count):
        # print(f"All indices are accounted for and shuffled correctly. | Interval: {min_cold_call_interval}")
        pass
    
    elif are_indices_within_range and (final_df_count != original_df_count):
        print(f"Issue! Some indices are missing! All indices in the df are shuffled correctly. | Interval: {min_cold_call_interval}.")
        print(f"Orginal {original_df_count} | Final {final_df_count} | Final raw len {len(final_df)}")


        unique_names_final_df = final_df['Names'].unique()
        unique_names_original_df = original_df['Names'].unique()

        # Find the difference
        names_difference = set(unique_names_original_df).difference(unique_names_final_df)

        # Print the difference
        print("Unique elements in 'Names' column of original_df not present in final_df:")
        print(names_difference)

        # Spot the duplicate
        duplicates = final_df[final_df['Names'].duplicated()]

        print("Duplicate elements in the 'Names' column of final_df:")
        print(duplicates)
        pprint(final_df['Names'])

        pprint(original_df['Names'])

    elif not are_indices_within_range and (final_df_count == original_df_count):
        print(f"Issue! Some indices are still in the interval space. All indices are accounted for. | Interval: {min_cold_call_interval}.")
    else:
        print(f"Issue! Some indices are still in the interval space and some indices are missing! | Interval: {min_cold_call_interval}.")

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
    # Turn into df
    rows_to_insert = pd.DataFrame(list(rows_to_insert), columns=['Names'])

    # Calculate domain start and end indices
    domain_start = min_cold_call_interval
    domain_end = len(truncated_df) - min_cold_call_interval

    # Generate random indices within the specified domain
    random_indices = np.random.randint(domain_start, domain_end, len(rows_to_insert))

    # Sort the indices to insert rows in the correct order
    random_indices.sort()
    
    # Insert the rows from the other DataFrame into the original DataFrame
    for i, index in enumerate(random_indices):
        # print(f"New index {index}")
        # print(rows_to_insert.iloc[i:i + 1])
        truncated_df = pd.concat([truncated_df.iloc[:index + i], rows_to_insert.iloc[i:i + 1], truncated_df.iloc[index + i:]]).reset_index(drop=True)
    
    # pprint(truncated_df)
    
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
    for i, df in enumerate(duplicated_dfs_list):
        duplicated_dfs_list[i] = df.sample(frac=1).reset_index(drop=True)

    # Step 3: Find duplicates within m at the seams between DataFrame n-1 and n for all DataFrames
    for i in range(1, n):
        bottom_of_prev_df = duplicated_dfs_list[i-1].iloc[-m:, 0] # [row, column]
        top_of_current_df = duplicated_dfs_list[i].iloc[:m, 0]

        common_duplicates = set(bottom_of_prev_df.values).intersection(top_of_current_df.values)
        print(f"len dups {len(common_duplicates)}")
        print(common_duplicates)
        
        # If no overlaps, continue to next loop
        if not common_duplicates:
            continue
        
        # If overlaps, handle them.
        # Drop rows in the DataFrame where bottom_of_prev_df/top_of_current_df is a duplicate
        truncated_prev_df = duplicated_dfs_list[i-1][~duplicated_dfs_list[i-1].isin(common_duplicates).any(axis=1)] # this assumes all unique names
        truncated_current_df = duplicated_dfs_list[i][~duplicated_dfs_list[i].isin(common_duplicates).any(axis=1)]

        # Step 4: Move duplicates elsewhere in the DataFrame
        min_cold_call_interval = 4 #TODO find a way for user to modify this value

        duplicated_dfs_list[i-1] = random_insert_rows(truncated_prev_df, common_duplicates, min_cold_call_interval)
        duplicated_dfs_list[i] = random_insert_rows(truncated_current_df, common_duplicates, min_cold_call_interval)

        # Check your work
        checkIndiciesInRange(original_df, truncated_current_df, duplicated_dfs_list[i], min_cold_call_interval)

        checkIndiciesInRange(original_df, truncated_prev_df, duplicated_dfs_list[i-1], min_cold_call_interval)


    # Concatenate all the DataFrames into a df
    long_df = pd.concat(duplicated_dfs_list, axis=0, ignore_index=True).reset_index(drop=True)

    return long_df



if __name__ == "__main__":
    
    #Import 
    original_df = pd.read_csv('import_data.csv')  #TODO make robust to excell files and split 1st name last name fields
    
    # Generate
    n = 5   #TODO make these user input 
    m = 5
    export_df = create_long_list(original_df, n, m)

    # Check your work
    column_name = "Names" #TODO make robust
    count_rows_until_duplicate_in_column(export_df, column_name)
    
    export_df.to_csv("long.csv", index=False, encoding='utf-8')