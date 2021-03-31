export default `&gw_input

  ! see http://www.sternheimergw.org for more information.
  
  ! config of the scf run
  prefix         = '__prefix__'
  outdir         = {% raw %}'{{ JOB_WORK_DIR }}/outdir'{% endraw %}

  ! the grid used for the linear response
  kpt_grid       = {{ kgrid.dimensions|join(', ') }}
  qpt_grid       = {{ qgrid.dimensions|join(', ') }}

  ! truncation (used for both correlation and exchange)
  truncation     = '2d'

  ! number of bands for which the GW correction is calculated
  num_band       = 8

  ! configuration of the Coulomb solver
  thres_coul     = 1.0d-2

  ! configuration of W in the convolution
  model_coul     = 'godby-needs'
  max_freq_coul  = 120
  num_freq_coul  = 35

  ! configuration of the Green solver
  thres_green    = 1.0d-3
  max_iter_green = 300

  ! configuration for the correlation self energy
  ecut_corr      = 5.0
  max_freq_corr  = 100.0
  num_freq_corr  = 11

  ! configuration for the exchange self energy
  ecut_exch      = 20.0

  ! configuration for the output
  eta            = 0.1
  min_freq_wind  = -30.0
  max_freq_wind  =  30.0
  num_freq_wind  = 601
/

&gw_output
/

FREQUENCIES
2
  0.0    0.0
  0.0   10.0
/

K_points
{{ explicitKPath2PIBA.length }}
{% for point in explicitKPath2PIBA -%}
{% for coordinate in point.coordinates %}{{ coordinate }}{% endfor %}
{% endfor %}
/
`;
