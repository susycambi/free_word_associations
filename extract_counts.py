#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:33:22 2023

@author: susannecambi
"""

import pandas as pd


# Load the data from the file with the structure
df = pd.read_csv('/Users/susannecambi/Documents/neuroscience_master/Noce_internship/dev/FWA/words-n-stuff.csv')


df.drop(df.columns[[13]], axis=1, inplace=True) # dropping associations columns
df=df.mask(df == '[]') # this changes the empty strings (seen as '[]') to NaN, which are then ignored, could also be done in other ways
 
# Get unique cue strings from the first column
cue_strings = df['word'].unique()
 
# Initialize lists, where we will keep the results & output it to a new frame
cue_results = []
subject_results = []
 
# Iterate over each cue, filter the dataset by the unique cue, and count non-empty cells….
for cue_string in cue_strings:
    # Filter the dataframe so it only has rows with the cue string
    filtered_df = df[df['word'] == cue_string]
    # Iterate over & count non-empty cells
    counts = []
    collections = []
    for col in df.columns[1:]:  # Assuming the subject columns start from the second column, so from S7 to S67
        count = filtered_df[col].count()  # Count non-empty cells in the subject column
        collection = filtered_df[col].dropna().tolist()  # Collect non-empty cell values in the subject column
        counts.append(count)
        collections.append(collection)
 
    # append the counts & collections back to those empty lists from before
    cue_results.extend([cue_string] * len(df.columns[1:]))
    subject_results.append({'Subject': df.columns[1:], 'Count': counts, 'Collection': collections})



# Create a new dataframe to store the results

results_df = pd.DataFrame({'Cue': cue_results, 'Subject': [subject for result in subject_results for subject in result['Subject']], 'Count': [count for result in subject_results for count in result['Count']], 'Collection': [collection for result in subject_results for collection in result['Collection']]})
 
#results_df = pd.DataFrame({'Cue': cue_results, 'Subject': df.columns[1:], 'Count': [count for result in subject_results for count in result['Count']], 'Collection': [collection for result in subject_results for collection in result['Collection']]})
 
# Output the results to a new CSV file
results_df.to_csv('results.csv', index=False)

# NEW STUFF TO PIVOT

# # Pivot the dataframe, account for duplicates
# pivoted_df = pd.pivot_table(results_df, index='Cue', columns='Subject',
#                             values=['Count', 'Collection'],
#                             aggfunc={'Count': 'sum', 'Collection': lambda x: ', '.join(map(str, x))})
 
# # Flatten col names
# pivoted_df.columns = [f'{col[0]}_{col[1]}' for col in pivoted_df.columns]
 
# # Reset index and save to .csv
# pivoted_df = pivoted_df.reset_index()
 
# # Remove characters [] & '' from the cue/collections cols
# pivoted_df['Cue'] = pivoted_df['Cue'].str.replace(r"[\[\]'\"]", '', regex=True)
# collection_cols = [col for col in pivoted_df.columns if col.startswith('Collection_')]
# pivoted_df[collection_cols] = pivoted_df[collection_cols].apply(lambda x: x.str.replace(r"[\[\]'\"]", '', regex=True))

# # Convert string values to list
# for collection_col in collection_cols:
#     pivoted_df[collection_col] = pivoted_df[collection_col].apply(lambda x: [val.strip() for val in x.split(",")] if isinstance(x, str) else [])
 
# # Print the updated DataFrame
# print(pivoted_df)
 
# # Save to .csv file
# pivoted_df.to_csv('pivoted_results.csv', index=False)


# Pivot the dataframe, account for duplicates
pivoted_df = pd.pivot_table(results_df, index='Cue', columns='Subject',
                            values=['Count', 'Collection'],
                            aggfunc={'Count': 'sum', 'Collection': lambda x: ''.join(map(str, x))})
 
# Flatten  column names
pivoted_df.columns = [f'{col[0]}_{col[1]}' for col in pivoted_df.columns]
 
# Reset  index ] save to .csv
pivoted_df = pivoted_df.reset_index()
 
# Remove characters [] & '' from "Collection*" columns
pivoted_df['Cue'] = pivoted_df['Cue'].str.replace(r"[\[\]']", '', regex=True)
collection_cols = [col for col in pivoted_df.columns if col.startswith('Collection_')]
pivoted_df[collection_cols] = pivoted_df[collection_cols].apply(lambda x: x.str.replace(r"[\[\]']", '', regex=True))

# Print the updated DataFrame
print(pivoted_df)
 
pivoted_df.to_csv('pivoted_results.csv', index=False)
