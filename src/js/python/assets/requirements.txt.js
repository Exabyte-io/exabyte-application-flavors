export default `
# ----------------------------------------------------------------- #
#                                                                   #
#  Example Python package requirements for the Exabyte.io platform  #
#                                                                   #
#  Will be used as follows:                                         #
#                                                                   #
#    1. A runtime directory for this calculation is created         #
#    2. This list is used to populate a Python virtual environment  #
#    3. The virtual environment is activated                        #
#    4. The Python process running the script included within this  #
#       job is started                                              #
#                                                                   #
#  For more information visit:                                      #
#   - https://pip.pypa.io/en/stable/reference/pip_install           #
#   - https://virtualenv.pypa.io/en/stable/                         #
#                                                                   #
#  The package set below is a stable working set of pymatgen and    # 
#  all of its dependencies.  Please adjust the list to include      #
#  your preferred packages.                                         #
#                                                                   # 
# ----------------------------------------------------------------- #

# Python 2 packages
backports.functools-lru-cache==1.6.1;python_version<"3"
certifi==2020.12.5;python_version<"3"
chardet==4.0.0;python_version<"3"
cycler==0.10.0;python_version<"3"
decorator==4.4.2;python_version<"3"
enum34==1.1.10;python_version<"3"
idna==2.10;python_version<"3"
kiwisolver==1.1.0;python_version<"3"
matplotlib==2.2.5;python_version<"3"
monty==2.0.7;python_version<"3"
mpmath==1.2.1;python_version<"3"
networkx==2.2;python_version<"3"
numpy==1.16.6;python_version<"3"
palettable==3.3.0;python_version<"3"
pandas==0.24.2;python_version<"3"
PyDispatcher==2.0.5;python_version<"3"
pymatgen==2018.12.12;python_version<"3"
pyparsing==2.4.7;python_version<"3"
python-dateutil==2.8.1;python_version<"3"
pytz==2021.1;python_version<"3"
requests==2.25.1;python_version<"3"
ruamel.ordereddict==0.4.15;python_version<"3"
ruamel.yaml==0.16.12;python_version<"3"
ruamel.yaml.clib==0.2.2;python_version<"3"
scipy==1.2.3;python_version<"3"
six==1.15.0;python_version<"3"
spglib==1.16.1;python_version<"3"
subprocess32==3.5.4;python_version<"3"
sympy==1.5.1;python_version<"3"
tabulate==0.8.7;python_version<"3"
urllib3==1.26.3;python_version<"3"

# Python 3 packages
certifi==2020.12.5;python_version>="3"
chardet==4.0.0;python_version>="3"
cycler==0.10.0;python_version>="3"
decorator==4.4.2;python_version>="3"
future==0.18.2;python_version>="3"
idna==2.10;python_version>="3"
kiwisolver==1.3.1;python_version>="3"
matplotlib==3.3.4;python_version>="3"
monty==4.0.2;python_version>="3"
mpmath==1.2.1;python_version>="3"
networkx==2.5;python_version>="3"
numpy==1.19.5;python_version>="3"
palettable==3.3.0;python_version>="3"
pandas==1.1.5;python_version>="3"
Pillow==8.1.0;python_version>="3"
plotly==4.14.3;python_version>="3"
pymatgen==2021.2.8.1;python_version>="3"
pyparsing==2.4.7;python_version>="3"
python-dateutil==2.8.1;python_version>="3"
pytz==2021.1;python_version>="3"
requests==2.25.1;python_version>="3"
retrying==1.3.3;python_version>="3"
ruamel.yaml==0.16.12;python_version>="3"
ruamel.yaml.clib==0.2.2;python_version>="3"
scipy==1.5.4;python_version>="3"
six==1.15.0;python_version>="3"
spglib==1.16.1;python_version>="3"
sympy==1.7.1;python_version>="3"
tabulate==0.8.7;python_version>="3"
uncertainties==3.1.5;python_version>="3"
urllib3==1.26.3;python_version>="3"
`;
