export default `&BANDS
    prefix = '__prefix__'
    outdir = {% raw %}'{{ JOB_WORK_DIR }}/outdir'{% endraw %}
    filband = {% raw %}'{{ JOB_WORK_DIR }}/bands.dat'{% endraw %}
    no_overlap = .true.
/
`;
