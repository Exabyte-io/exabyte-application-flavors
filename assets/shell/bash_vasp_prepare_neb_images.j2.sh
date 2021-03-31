#!/bin/bash

# ------------------------------------------------------------------ #
#  This script prepares necessary directories to run VASP NEB
#  calculation. It puts initial POSCAR into directory 00, final into 0N
#  and intermediate images in 01 to 0(N-1). It is assumed that SCF
#  calculations for initial and final structures are already done in
#  previous subworkflows and their standard outputs are written into
#  "vasp_neb_initial.out" and "vasp_neb_final.out" files respectively.
#  These outputs are here copied into initial (00) and final (0N)
#  directories to calculate the reaction energy profile.
# ------------------------------------------------------------------ #

{% raw -%}
cd {{ JOB_WORK_DIR }}
{%- endraw %}

# Prepare First Directory
mkdir -p 00
cat > 00/POSCAR <<EOF
{{ input.FIRST_IMAGE }}
EOF
cp vasp_neb_initial.out 00/stdout
cp CONTCAR 00/CONTCAR

# Prepare Last Directory
mkdir -p 0{{ input.INTERMEDIATE_IMAGES.length + 1 }}
cat > 0{{ input.INTERMEDIATE_IMAGES.length + 1 }}/POSCAR <<EOF
{{ input.LAST_IMAGE }}
EOF
cp CONTCAR 0{{ input.INTERMEDIATE_IMAGES.length + 1 }}/CONTCAR
cp vasp_neb_final.out 0{{ input.INTERMEDIATE_IMAGES.length + 1 }}/stdout

{% for IMAGE in input.INTERMEDIATE_IMAGES %}
# Prepare Intermediate Directory {{ loop.index }}
mkdir -p 0{{ loop.index }}
cat > 0{{ loop.index }}/POSCAR <<EOF
{{ IMAGE }}
EOF
{% endfor -%}
