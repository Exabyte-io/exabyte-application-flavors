#!/bin/bash

# ---------------------------------------------------------------- #
#                                                                  #
#  EXAMPLE JUPYTER LAB CONFIGURATION SCRIPT.                       #
#                                                                  #
#  ADJUST BELOW TO CUSTOMIZE YOUR JUPYTER LAB ENVIRONMENT.         #
#                                                                  #
# ---------------------------------------------------------------- #

cat > requirements.txt <<-EOF
####
# The default JupyterLab environment is a consistent set of packages obtained from running
# pip3 install "jupyterlab==3.0.3" "exabyte-api-client>=2020.10.19" "numpy>=1.17.3" "pandas>=1.1.4" --only-binary numpy,pandas --use-deprecated=legacy-resolver
# Additional packages to be installed can be installed by adding them to this requirements.txt file
# These packages will be installed to the user's local site-packages
####

EOF

pip3 install --user --no-deps -r requirements.txt

