#!/bin/sh

#PBS -l select=2:ncpus=16:mem=48gb
#PBS -l walltime=23:59:00
# High throughput has $PBS_ARRAY_INDEX output

cd $PBS_O_WORKDIR

module load intel-suite
module load mpi
module load lammps/19Mar2020

timer=`date`

echo Running $timer >> $PBS_O_WORKDIR/script.log 

start=0
end=$(($start + 49))

for PBS_ARRAY_INDEX in $(seq ${start} 1 ${end});
	do cp in.janus_rod job$PBS_ARRAY_INDEX
	sed -i "s/^variable.*rand1.*equal.*/variable          rand1    equal $(( $RANDOM ))/" job$PBS_ARRAY_INDEX
	sed -i "s/^variable.*rand2.*equal.*/variable          rand2    equal $(( $RANDOM ))/" job$PBS_ARRAY_INDEX
	sed -i "s/^variable.*job.*equal.*/variable          job    equal $(( $PBS_ARRAY_INDEX ))/" job$PBS_ARRAY_INDEX
	mpiexec lmp_mpi -in job$PBS_ARRAY_INDEX > logfile$PBS_ARRAY_INDEX
done

echo Done >> $PBS_O_WORKDIR/script.log


