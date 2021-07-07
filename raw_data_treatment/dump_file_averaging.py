import os, os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import sys
import dask.array as da
import dask.dataframe as dd
import fnmatch 

### To use this file, make sure the above libraries are installed and use 
### python dump_file_averaging.py base_case_file general_case_file directory 
### directory can be edited below if necessary
### for instance:
### python dump_file_averaging.py profile_grid_cool_fluid.dat0 profile_grid_cool_fluid.dat # directory

import sys
args = sys.argv[1:] 
base_case = args[0] # USER input required here, to state the base case of file name of file to iterate over
file_name = args[1] # USER input required here, to state what the general name of the files are for averaging
directory = args[2] # USER input required here, to state the directory being used

df0 = pd.read_csv(base_case # USER INPUT base_case used here
                  ,skiprows=[0,1,3], delim_whitespace=True) # base case, for columns parsing, base case is .dat0, out of 1000 files

columns_l = df0.columns[1:] # obtain columns, ignoring the '#' symbol in the datafile, raise error if format incorrect
del df0 # free up memory

file_no = len(fnmatch.filter(os.listdir(directory)
                         , '{}*'.format(file_name))

print('No. of files:  ' + str(file_no))

print('Base case loaded')

df = dd.read_csv(directory + file_name + r'*'# USER INPUT HERE improved
                ,skiprows=[0,1,3], delim_whitespace=True) # use dask to process all files of interest 'profile_grid_cool_fluid.dat'

print('All dataframes loaded')

df = df.iloc[:, :-1]
df.columns = columns_l # correct the columns
print('Columns corrected')

df_mean = df.groupby(df.Chunk).mean().compute()
print('Mean Calculated')
df_mean.to_csv('df_mean_parallel_grid_{}.csv'.format(file_no), sep = ' ')

# following code for calculating standard deviation can be computationally expensive
# the most demanding part of code, most likely to cause mem error
df_std = df.groupby(df.Chunk).std().compute().add_suffix('_std') # compute std, add suffix _std
							
df_std.to_csv('df_std_parallel_grid_{}.csv'.format(file_name), sep = ' ')

print('Standard deviation Calculated')

df_both = pd.concat([df_mean, df_std], axis = 1)
df_both.to_csv('df_both_parallel_grid_{}.csv'.format(file_name), sep = ' ') # output file
print('Job saved and finished')
os.chdir(r'../')
