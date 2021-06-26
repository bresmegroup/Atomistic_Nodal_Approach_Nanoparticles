from scipy import spatial
import pandas as pd
import numpy as np

df_fluid_border = df_filtered

fluid_array = df_fluid_border[['x', 'y', 'z']] # coordinates of fluid grid
fluid_tree = spatial.cKDTree(fluid_array)


particle_array = df_particle_border[['x', 'y', 'z']] #coordinates of NP atomic nodal positions
particle_tree = spatial.cKDTree(particle_array)


indexes = particle_tree.query_ball_tree(fluid_tree, r= 1.3) 
# r = 1.3 is a local minima in the g(r) curve for fluid-NP interactions. First solvation shell radial distance is the cutoff threshold for querying the cdktree
# indexes identifies which neighbouring fluids are within r = 1.3 

temp_list = []
temp_list_std = []
Ncount_list = []

for i in indexes: 
    u = df_fluid_border.iloc[i] # collate fluid data for neihbouring grids within r = 1.3
    
    weighted_stats = DescrStatsW(u.temp, weights=u.Ncount, ddof=0) # Ncount refers to the avearge number of fluid particles occupying a cuboid grid
    temp_list.append(weighted_stats.mean)
    temp_list_std.append(weighted_stats.std)
		Ncount_list.append(sum(u.Ncount)) # number of fluid atoms 
		
df_particle_border['Ncount'] = Ncount_list    
df_particle_border['fluid_temp'] = temp_list
df_particle_border['dT'] = df_particle_border['temp'] - df_particle_border['fluid_temp'] # temperature discontinuity
df_particle_border['G'] = df_particle_border['r_flux']/df_particle_border['dT']/df_particle_border.volume    
