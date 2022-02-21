#!/bin/bash

# ------------------------------------------------------------ #
#                                                              #
#   JUPYTER LAB INSTALLATION SCRIPT FOR EXABYTE.IO PLATFORM.   #
#                                                              #
#    DO NOT MODIFY THIS FILE! ADJUST "configure.sh" SCRIPT     #
#    IF YOU NEED TO CUSTOMIZE YOUR JUPYTER LAB ENVIRONMENT.    #
#                                                              #
# ------------------------------------------------------------ #

export PYTHONDONTWRITEBYTECODE=1

# Load the fixed python environment for jupyterlab
# This is a consistent set of packages installable in Python 3, obtained by:
# > pip3 install "jupyterlab==3.0.3" "exabyte-api-client>=2020.10.19" numpy>=1.17.3 \
# >  pandas>=1.1.4 matplotlib seaborn ase pymatgen rdkit-pypi "matminer==0.7.0" scikit-learn xgboost
jupyterlabdir="/export/compute/software/python-applications/jupyterlab/py-3.8.6/3.0.3/"

# activate the virtual environment.
cd "$jupyterlabdir"
source "bin/activate"

# Create a self-signed certificate to make communication with Jupyter Lab secure
SUBJECT="/C=US/ST=CA/L=San Francisco/O=Exabyte Inc./CN=Jupyter Lab"
openssl req -new -newkey rsa:4096 -days 30 -nodes -x509 -subj "$SUBJECT" -keyout key.pem -out cert.pem

# execute the configuration script provided by user
source ./configure.sh

# Run Jupyter Lab on dropbox to read/write files
cd /dropbox/{% raw %}{{ JOB_OWNER_SLUG }}{% endraw %}
if [ $? -ne 0 ]; then
    exit 1
fi

# Start the Jupyter notebook
jupyter notebook --config {% raw %}{{ JOB_WORK_DIR }}/config.py{% endraw %}
