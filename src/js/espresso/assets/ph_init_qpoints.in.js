export default `&INPUTPH
    tr2_ph = 1.0d-18,
    recover = .false.
    start_irr = 0
    last_irr = 0
    ldisp = .true.
    fildyn = 'dyn0'
    prefix = '__prefix__'
    outdir = {% raw %}'{{ JOB_WORK_DIR }}/outdir'{% endraw %}
    {% for d in qgrid.dimensions -%}
    nq{{loop.index}} = {{d}} 
    {% endfor %}
/
`;
