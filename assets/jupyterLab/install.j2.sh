#!/bin/bash

# ---------------------------------------------------------------- #
#                                                                  #
#  JUPYTER LAB INSTALLATION SCRIPT FOR EXABYTE.IO PLATFORM.        #
#                                                                  #
#  DO NOT MODIFY THIS FILE! ADJUST "configure.sh" SCRIPT           #
#  IF YOU NEED TO CUSTOMIZE YOUR JUPYTER LAB ENVIRONMENT.          #
#                                                                  #
# ---------------------------------------------------------------- #

export PYTHONDONTWRITEBYTECODE=1

# Create and activate a virtual environment, to isolate the installed packages.
envdir=$(pwd)
python -m virtualenv -q .env
source .env/bin/activate

# Clean up virtual environment directory on exit to avoid occupying disk space.
# The information about the packages installed is saved in the corresponding file.
function cleanup () {
    cd $envdir
    python -m pip freeze > installed_packages_list.txt
    deactivate
    rm -rf .env
    exit
}
trap cleanup INT TERM EXIT

# Install Jupyter Lab
python -m pip install -q jupyterlab=={{ application.version }}

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
