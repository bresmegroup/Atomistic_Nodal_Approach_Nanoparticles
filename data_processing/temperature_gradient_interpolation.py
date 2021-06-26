import numpy as np
import pandas as pd
from scipy import spatial
from scipy.interpolate import LinearNDInterpolator

df0 = df_traj_[['v_vx','v_vy','v_vz','temp', 'Coordination', 'Ncount']] # NP properties
df1 = fluid[['v_vx','v_vy','v_vz','temp', 'Coordination', 'Ncount']] # fluid properties

temp_net = pd.concat([df0,df1])

# array of data used for interpolation
x = temp_net['v_vx'].values
y = temp_net['v_vy'].values
z = temp_net['v_vz'].values
data = temp_net['temp'].values
data_coord = temp_net['Coordination'].values
Ncount = temp_net['Ncount'].values

interp = LinearNDInterpolator(list(zip(x, y, z)), data) # temperature inteterpolator
interp_coord = LinearNDInterpolator(list(zip(x, y, z)), data_coord) #  coordination inteterpolator
interp_Ncount = LinearNDInterpolator(list(zip(x, y, z)), Ncount) # number of particles inteterpolator

linx = linspace(min(x), max(x), 199) # create an array of 3d points to interpolate onto
liny = linspace(min(y), max(y), 199)
linz = linspace(min(z), max(z), 199)

xx,yy,zz = np.meshgrid(linx,liny,linz) # generate a meshgrid based 

Z = interp(xx, yy, zz) # temperature interpolated
coord = interp_coord(xx, yy, zz)
ncount = interp_Ncount(xx, yy, zz)

dtdy, dtdx, dtdz= np.gradient(Z, np.diff(linx)[0], np.diff(liny)[0], np.diff(linz)[0], edge_order =2) # tempearture gradient 

dim = xx.shape[0] * xx.shape[1] * xx.shape[2]
xxx = xx.reshape(dim )
yyy = yy.reshape(dim )
zzz = zz.reshape(dim )
ZZ = Z.reshape(dim )
DTDX = dtdx.reshape(dim )
DTDY = dtdy.reshape(dim )
DTDZ = dtdz.reshape(dim )
norm = np.sqrt(DTDX**2 + DTDY**2 + DTDZ**2)


### storing the data
df_swopper = pd.DataFrame([])

df_swopper['x'] = xxx
df_swopper['y'] = yyy
df_swopper['z'] = zzz
df_swopper['temp'] = ZZ #DTDX
df_swopper['norm'] = norm #DTDX
df_swopper['fx'] = DTDX / norm
df_swopper['fy'] = DTDY / norm
df_swopper['fz'] = DTDZ / norm
df_swopper['coord'] = coord.reshape(dim )
df_swopper['Ncount'] = ncount.reshape(dim )
df_swopper['DisplacementX'] = DTDX 
df_swopper['DisplacementY'] = DTDY
df_swopper['DisplacementZ'] = DTDZ

### kdtree to collect interpolated temperature gradient
df_fluid_border = df_swopper

fluid_array = df_fluid_border[['v_vx', 'v_vy', 'v_vz']] # can normalise the terms and add in the temperature
fluid_tree = spatial.cKDTree(fluid_array)

#df_particle_border = df_border defined

particle_array = df_particle_border[['x', 'y', 'z']]
particle_tree = spatial.cKDTree(particle_array)

indexes = particle_tree.query_ball_tree(fluid_tree, r= 1.0) # only collect data from nearby vicinity, for r < 1.1, on a per-atom nodal basis. 

dtdx = []
dtdy = []
dtdz = []
displacement = []
for index,i in enumerate(indexes):
    test_particle = df_particle_border.iloc[index]
    px = test_particle.x
    py = test_particle.y
    pz = test_particle.z
    u = df_fluid_border.iloc[i].reset_index()
    
    weighted_stats = DescrStatsW(u.DisplacementX, weights=u.Ncount, ddof=0)
    dtdx.append(weighted_stats.mean)

    weighted_stats = DescrStatsW(u.DisplacementY, weights=u.Ncount, ddof=0)
    dtdy.append(weighted_stats.mean)

    weighted_stats = DescrStatsW(u.DisplacementZ, weights=u.Ncount, ddof=0)
    dtdz.append(weighted_stats.mean)
        
df_particle_border['DisplacementX'] = dtdx
df_particle_border['DisplacementY'] = dtdy
df_particle_border['DisplacementZ'] = dtdz
