export default `&INPUTPP
    outdir = {% raw %}'{{ JOB_WORK_DIR }}/outdir'{% endraw %}
    prefix = '__prefix__'
    filplot = 'pp.dat'
    plot_num = 0
/
&PLOT
    iflag = 3
    output_format = 5
    fileout ='density.xsf'
/
`;
