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
# This is a consistent set of packages installable in Python 3, obtained by:
# pip3 install "jupyterlab==3.0.3" "exabyte-api-client>=2020.10.19" "numpy>=1.17.3" "pandas>=1.1.4"
####
anyio==3.5.0
appnope==0.1.2
argon2-cffi==21.3.0
argon2-cffi-bindings==21.2.0
asttokens==2.0.5
attrs==21.4.0
Babel==2.9.1
backcall==0.2.0
black==22.1.0
bleach==4.1.0
certifi==2021.10.8
cffi==1.15.0
charset-normalizer==2.0.12
click==8.0.4
debugpy==1.5.1
decorator==5.1.1
defusedxml==0.7.1
entrypoints==0.4
exabyte-api-client==2022.1.13.post0
executing==0.8.2
idna==3.3
importlib-resources==5.4.0
ipykernel==6.9.1
ipython==8.0.1
ipython-genutils==0.2.0
jedi==0.18.1
Jinja2==3.0.3
json5==0.9.6
jsonschema==4.4.0
jupyter-client==7.1.2
jupyter-core==4.9.2
jupyter-server==1.13.5
jupyterlab==3.0.3
jupyterlab-pygments==0.1.2
jupyterlab-server==2.10.3
MarkupSafe==2.1.0
matplotlib-inline==0.1.3
mistune==0.8.4
mypy-extensions==0.4.3
nbclassic==0.3.5
nbclient==0.5.11
nbconvert==6.4.2
nbformat==5.1.3
nest-asyncio==1.5.4
notebook==6.4.8
numpy==1.22.2
packaging==21.3
pandas==1.4.1
pandocfilters==1.5.0
parso==0.8.3
pathspec==0.9.0
pexpect==4.8.0
pickleshare==0.7.5
platformdirs==2.5.1
prometheus-client==0.13.1
prompt-toolkit==3.0.28
ptyprocess==0.7.0
pure-eval==0.2.2
pycparser==2.21
Pygments==2.11.2
pyparsing==3.0.7
pyrsistent==0.18.1
python-dateutil==2.8.2
pytz==2021.3
pyzmq==22.3.0
requests==2.26.0
Send2Trash==1.8.0
six==1.16.0
sniffio==1.2.0
stack-data==0.2.0
terminado==0.13.1
testpath==0.5.0
tomli==2.0.1
tornado==6.1
traitlets==5.1.1
typing_extensions==4.1.1
urllib3==1.26.8
wcwidth==0.2.5
webencodings==0.5.1
websocket-client==1.2.3
zipp==3.7.0
EOF

pip3 install --no-deps -r requirements.txt
