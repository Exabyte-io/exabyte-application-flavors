export default `&CONTROL
    calculation = 'bands'
    title = ''
    verbosity = 'low'
    restart_mode = '{{input.RESTART_MODE}}'
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
/
&ELECTRONS
    diagonalization = 'david'
    diago_david_ndim = 4
    diago_full_acc = .true.
    mixing_beta = 0.3
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
K_POINTS crystal_b
{{kpath.length}}
{% for point in kpath -%}
{% for d in point.coordinates %}{{d}} {% endfor -%}{{point.steps}}
{% endfor %}
`;
