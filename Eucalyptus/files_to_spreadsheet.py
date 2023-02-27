import pandas as pd
import os


# Reading file names
path = '/Users/elijah/Library/CloudStorage/OneDrive-UNSW/Eucalyptus Raw Images/EUCS'
file_names = []

for root, dirs, files in os.walk(path):
    for file in files:
        file_names.append(file)

# Putting file names into DataFrame
raw_dataset = pd.Series(file_names)
raw_dataset = raw_dataset.str.replace('.jpg', '')

# Initial split for family and species name
raw_dataset = raw_dataset.str.split(' ', n=1, expand=True)
raw_dataset[[1, 2]] = raw_dataset[1].str.split('_', n=1, expand=True)
raw_dataset[[2, 3]] = raw_dataset[2].str.split('_', n=1, expand=True)
raw_dataset[[3, 4, 5]] = raw_dataset[3].str.split('_', n=2, expand=True)

# Filtering out invalid locations
valid_locations = raw_dataset.loc[~raw_dataset[2].isin(['kb', '1', ''])]
invalid_locations = raw_dataset.loc[raw_dataset[2].isin(['kb', '1', ''])]

# Splitting location and section type info
invalid_locations[[4, 5]] = invalid_locations[4].str.split(' ', n=1, expand=True)
invalid_locations = invalid_locations.drop([3], axis=1)
invalid_locations.columns = ['Family', 'Species', 'Location', 'Type', 'Duplicate']

valid_locations[[5, 6]] = valid_locations[5].str.split(' ', n=1, expand=True)
valid_locations = valid_locations.drop([3, 4], axis=1)
valid_locations.columns = ['Family', 'Species', 'Location', 'Type', 'Duplicate']

# Combining both DataFrames
euc_database_full = pd.concat([valid_locations, invalid_locations])
euc_database_full.columns = ['Family', 'Species', 'Location', 'Type', 'Duplicate']
euc_database_summary = euc_database_full[['Family', 'Species', 'Location']]

