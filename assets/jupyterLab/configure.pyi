# ---------------------------------------------------------------- #
#                                                                  #
#  JUPYTER CONFIG FILE.                                            #
#                                                                  #
# ---------------------------------------------------------------- #

{% raw %}
JOB_WORK_DIR = '{{ JOB_WORK_DIR }}'
c.NotebookApp.open_browser = False
c.NotebookApp.ip = '{{ JUPYTER_LAB_IP }}'
c.NotebookApp.keyfile = '{{ JOB_WORK_DIR }}/key.pem'
c.NotebookApp.certfile = '{{ JOB_WORK_DIR }}/cert.pem'
c.NotebookApp.base_url = '/jupyter/{{ JOB_ID }}/{{ UNIT_ID }}'
c.FileCheckpoints.checkpoint_dir = '{{ JOB_WORK_DIR }}/checkpoints'
{% endraw %}
