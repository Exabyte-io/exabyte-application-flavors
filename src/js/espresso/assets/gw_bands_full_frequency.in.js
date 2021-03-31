export default `&gw_input

  ! see http://www.sternheimergw.org for more information.
  
  ! config of the scf run
  prefix         = '__prefix__'
  outdir         = {% raw %}'{{ JOB_WORK_DIR }}/outdir'{% endraw %}

  ! the grid used for the linear response
  kpt_grid       = {{ kgrid.dimensions|join(', ') }}
  qpt_grid       = {{ qgrid.dimensions|join(', ') }}

  ! number of bands for which the GW correction is calculated
  num_band       = 8

  ! configuration of W in the convolution
  max_freq_coul  = 200
  num_freq_coul  = 51

  ! configuration for the correlation self energy
  ecut_corr      = 6.0

  ! configuration for the exchange self energy
  ecut_exch      = 15.0
/

&gw_output
/

FREQUENCIES
35
  0.0    0.0
  0.0    0.3
  0.0    0.9
  0.0    1.8
  0.0    3.0
  0.0    4.5
  0.0    6.3
  0.0    8.4
  0.0   10.8
  0.0   13.5
  0.0   16.5
  0.0   19.8
  0.0   23.4
  0.0   27.3
  0.0   31.5
  0.0   36.0
  0.0   40.8
  0.0   45.9
  0.0   51.3
  0.0   57.0
  0.0   63.0
  0.0   69.3
  0.0   75.9
  0.0   82.8
  0.0   90.0
  0.0   97.5
  0.0  105.3
  0.0  113.4
  0.0  121.8
  0.0  130.5
  0.0  139.5
  0.0  148.8
  0.0  158.4
  0.0  168.3
  0.0  178.5
/

K_points
{{ explicitKPath2PIBA.length }}
{% for point in explicitKPath2PIBA -%}
{% for coordinate in point.coordinates %}{{ coordinate }}{% endfor %}
{% endfor %}
/
`;
