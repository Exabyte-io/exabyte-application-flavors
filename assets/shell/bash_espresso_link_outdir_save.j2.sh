{%- raw -%}
#!/bin/bash

mkdir -p {{ JOB_SCRATCH_DIR }}/outdir/_ph0
cd {{ JOB_SCRATCH_DIR }}/outdir
cp -r {{ JOB_WORK_DIR }}/../outdir/__prefix__.* .
{%- endraw -%}
