export default `#!/bin/bash

# ---------------------------------------------------------------- #
#                                                                  #
#  EXAMPLE JUPYTER LAB CONFIGURATION SCRIPT.                       #
#                                                                  #
#  ADJUST BELOW TO CUSTOMIZE YOUR JUPYTER LAB ENVIRONMENT.         #
#                                                                  #
# ---------------------------------------------------------------- #

cat > requirements.txt <<-EOF
####
# This is a consistent set of packages installable in Python 3, obtained by:
# pip3 install "jupyterlab==3.0.3" "exabyte-api-client>=2020.10.19" "numpy>=1.17.3" "pandas>=1.1.4" --only-binary numpy,pandas --use-deprecated=legacy-resolver
####
anyio==2.0.2
argon2-cffi==20.1.0
async-generator==1.10
attrs==20.3.0
Babel==2.9.0
backcall==0.2.0
bleach==3.2.1
certifi==2020.12.5
cffi==1.14.4
chardet==3.0.4
decorator==4.4.2
defusedxml==0.6.0
entrypoints==0.3
exabyte-api-client==2020.10.19
idna==2.7
ipykernel==5.4.3
ipython==7.19.0
ipython-genutils==0.2.0
jedi==0.18.0
Jinja2==2.11.2
json5==0.9.5
jsonschema==3.2.0
jupyter-client==6.1.11
jupyter-core==4.7.0
jupyter-server==1.2.1
jupyterlab==3.0.3
jupyterlab-pygments==0.1.2
jupyterlab-server==2.1.2
MarkupSafe==1.1.1
mistune==0.8.4
nbclassic==0.2.6
nbclient==0.5.1
nbconvert==6.0.7
nbformat==5.1.0
nest-asyncio==1.4.3
notebook==6.2.0
numpy==1.19.5
packaging==20.8
pandas==1.2.0
pandocfilters==1.4.3
parso==0.8.1
pexpect==4.8.0
pickleshare==0.7.5
prometheus-client==0.9.0
prompt-toolkit==3.0.10
ptyprocess==0.7.0
pycparser==2.20
Pygments==2.7.4
pyparsing==2.4.7
pyrsistent==0.17.3
python-dateutil==2.8.1
pytz==2020.5
pyzmq==20.0.0
requests==2.20.1
Send2Trash==1.5.0
six==1.15.0
sniffio==1.2.0
terminado==0.9.2
testpath==0.4.4
tornado==6.1
traitlets==5.0.5
urllib3==1.24.3
wcwidth==0.2.5
webencodings==0.5.1
EOF

pip3 install --no-deps -r requirements.txt
`;
