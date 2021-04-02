#!/bin/bash

# ---------------------------------------------------------------- #
#                                                                  #
#  Example job submission script for Exabyte.io platform           #
#                                                                  #
#  Shows resource manager directives for:                          #
#                                                                  #
#    1. the name of the job                (-N)                    #
#    2. the number of nodes to be used     (-l nodes=)             #
#    3. the number of processors per node  (-l ppn=)               #
#    4. the walltime in dd:hh:mm:ss format (-l walltime=)          #
#    5. queue                              (-q) D, OR, OF, SR, SF  #
#    6. merging standard output and error  (-j oe)                 #
#    7. email about job abort, begin, end  (-m abe)                #
#    8. email address to use               (-M)                    #
#                                                                  #
#  For more information visit https://docs.exabyte.io/cli/jobs     #
# ---------------------------------------------------------------- #

#PBS -N ESPRESSO-TEST
#PBS -j oe
#PBS -l nodes=1
#PBS -l ppn=1
#PBS -l walltime=00:00:10:00
#PBS -q D
#PBS -m abe
#PBS -M info@exabyte.io

# load module
module add espresso/540-i-174-impi-044

# go to the job working directory
cd $PBS_O_WORKDIR

# create input file
cat > pw.in <<EOF
&CONTROL
    calculation= 'scf'
    title= ''
    verbosity= 'low'
    restart_mode= 'from_scratch'
    wf_collect= .true.
    tstress= .true.
    tprnfor= .true.
    outdir= './'
    wfcdir= './'
    prefix= '__prefix__'
    pseudo_dir= '/export/share/pseudo/si/gga/pbe/gbrv/1.0/us/'
/
&SYSTEM
    ibrav=0
    nat=2
    ntyp=1
    ecutwfc= 40
    ecutrho= 200
    occupations= 'smearing'
    degauss= 0.005
/
&ELECTRONS
    diagonalization= 'david'
    diago_david_ndim= 4
    diago_full_acc= .true.
    mixing_beta= 0.3
    startingwfc='atomic+random'
/
&IONS
/
&CELL
/
ATOMIC_SPECIES
Si 28.0855 si_pbe_gbrv_1.0.upf
CELL_PARAMETERS angstrom
3.867000000 0.000000000 0.000000000
1.933500000 3.348920236 0.000000000
1.933500000 1.116306745 3.157392278
ATOMIC_POSITIONS crystal
Si 0.000000000 0.000000000 0.000000000
Si 0.250000000 0.250000000 0.250000000
K_POINTS automatic
10 10 10 0 0 0
EOF

# run the calculation
mpirun -np $PBS_NP pw.x -in pw.in > pw.out
