export default `&CONTROL
    calculation = 'relax'
    title = ''
    verbosity = 'low'
    restart_mode = '{{ input.RESTART_MODE }}'
    wf_collect = .true.
    tstress = .true.
    tprnfor = .true.
    outdir = {% raw %}'{{ JOB_WORK_DIR }}/outdir'{% endraw %}
    wfcdir = {% raw %}'{{ JOB_WORK_DIR }}/outdir'{% endraw %}
    prefix = '__prefix__'
    pseudo_dir = {% raw %}'{{ JOB_WORK_DIR }}/pseudo'{% endraw %}
/
&SYSTEM
    ibrav = {{ input.IBRAV }}
    nat = {{ input.NAT }}
    ntyp = {{ input.NTYP }}
    ecutwfc = {{ cutoffs.wavefunction }}
    ecutrho = {{ cutoffs.density }}
    occupations = 'smearing'
    degauss = 0.005
    assume_isolated = 'esm'
    esm_bc = '{{ boundaryConditions.type }}'
    fcp_mu = {{ boundaryConditions.targetFermiEnergy }}
    esm_w = {{ boundaryConditions.offset }}
    esm_efield = {{ boundaryConditions.electricField }}
/
&ELECTRONS
    diagonalization = 'david'
    diago_david_ndim = 4
    diago_full_acc = .true.
    mixing_beta = 0.3
    startingwfc = 'atomic+random'
/
&IONS
/
&CELL
/
ATOMIC_SPECIES
{{ input.ATOMIC_SPECIES }}
ATOMIC_POSITIONS crystal
{{ input.ATOMIC_POSITIONS }}
CELL_PARAMETERS angstrom
{{ input.CELL_PARAMETERS }}
K_POINTS automatic
{% for d in kgrid.dimensions %}{{d}} {% endfor %}{% for s in kgrid.shifts %}{{s}} {% endfor %}
`;
