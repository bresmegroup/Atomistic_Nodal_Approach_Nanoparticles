# Atomistic Nodal Approach for Obtaining Conductance
Python Code for Processing LAMMPS Data generated for two data types: LAMMPS trajectory file and LAMMPS dump files. Subsequently, the code involves post-processing of the data to give interfacial heat flux, temperature discontinuity and ultimately interfacial conductance using the atomistic nodal approach.

![3_janus_rods](https://user-images.githubusercontent.com/40763563/123518175-493d5100-d6d7-11eb-834b-f228ee0ac928.jpg)
LAMMPS Package used to generate Data:
- LAMMPS 19MAR20

Python Pacakages Needed:
- Scipy 1.6.0
- Dask 2.3.0
- Numpy 1.6.1
- SKlearn 0.24.1
- Pandas 1.1.3

## Part 1: Processing the Data
Two data types are generated from the sample LAMMPS script given, which are processed using the DASK and Pandas in the raw_data_treatment folder. The first is the cuboid grid-based DUMPS data format, which is used to process the fluid's thermodynamics and positional information. This is done through https://github.com/PanoptoSalad/Atomistic_Nodal_Approach_Conductance/blob/main/raw_data_treatment/dump_file_averaging.py. The second is the per-atom averaging conducted for the relatively stationary atoms of the NP, which are treated as nodesm whose physical properties are averaged on a per atom basis for the simulation. To process the data from the simulation, https://github.com/PanoptoSalad/Atomistic_Nodal_Approach_Conductance/blob/main/raw_data_treatment/traj_averaging.py can be used

## Part 2: Interpreting the Data
To find the thermal conductance of a NP, 2 quantities are needed: Interfacial heat flux and temperature disconituity, shown in the data_processing folder

1) Interfacial Heat Flux
- Volume: Volume can be calculated at a per-atom level using the Voronoi volume calculated by LAMMPS
- Direction of Heat Flux. Heat flux is projected along the temperature gradient.
- This Temperature gradient can be calculated using the https://github.com/PanoptoSalad/Atomistic_Nodal_Approach_Conductance/blob/main/data_processing/temperature_gradient_interpolation.py, using interpolation method in Scipy LinearNDInterpolator library

2) Temperature Discontinutiy
- The Temperature discontinuity can be obtained from constructing a C-KD tree for rapid querying of fluid grid information within a radius of interest (normally 1st peak in g(r)). This is done using https://github.com/PanoptoSalad/Atomistic_Nodal_Approach_Conductance/blob/main/data_processing/cdktree_dT_discontinuity.py

