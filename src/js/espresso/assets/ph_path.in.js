export default `&INPUTPH
    tr2_ph = 1.0d-12
    asr = .true.
    search_sym = .false.
    prefix = '__prefix__'
    outdir = {% raw %}'{{ JOB_WORK_DIR }}/outdir'{% endraw %}
/
{% for point in qpath -%}
{% for d in point.coordinates %}{{d}} {% endfor %}
{% endfor %}
`;
