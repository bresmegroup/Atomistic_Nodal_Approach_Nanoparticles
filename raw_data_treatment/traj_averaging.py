import os, os.path
import pandas as pd
import dask.array as da
import dask.dataframe as dd
import sys

### To use this file, make sure the above libraries are installed and use 
### python traj_averaging.py no_atom general_case_file
### for instance:
### python traj_averaging.py 811

import sys
args = sys.argv[1:] 
no_atom = args[0] # USER input required here, to state the number of atoms involved
file_name = args[1] # USER input required here, to state what the general name of the files are for averaging

directory = os.path.dirname(file_name) # get directory from file name
fn = os.path.basename(file_name)

file_no = len(fnmatch.filter(os.listdir(directory)
                         , '{}*'.format(fn))) #added a bracket

df = dd.read_csv(r'{}*'.format(file_name), sep = ' ', skiprows = 17 + no_atom, sample=1000000) # 17 trajectory labels that dont contribute to the data, and lammps output for t = 0 set to 0 removed
print('dataframe loaded')
columns_l = df.columns
#df = df.dropna(axis=1)
df.columns = list(columns_l[2:-1]) + ['t1','t2','t3']
df = df[columns_l[2:-1]]
print('Columns added')

df_means = df.groupby(df.id).mean().compute()
df_means.to_csv('traj_means_{}_{}.csv'.format(0, file_no)) # output the .csv file of averaged trajectory file

print('Filed Saved')
