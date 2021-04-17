# ---------------------------------------------------------- #
#                                                            #
#  This script extracts q-points and irreducible             #
#  representations from Quantum ESPRESSO xml data.           #
#                                                            #
#  Expects control_ph.xml and patterns.?.xml files to exist  #
#                                                            #
# ---------------------------------------------------------- #
from __future__ import print_function
import json
from xml.dom import minidom

{# JOB_WORK_DIR will be initialized at runtime => avoid substituion below #}
{%- raw -%}
CONTROL_PH_FILENAME = "{{JOB_WORK_DIR}}/outdir/_ph0/__prefix__.phsave/control_ph.xml"
PATTERNS_FILENAME = "{{JOB_WORK_DIR}}/outdir/_ph0/__prefix__.phsave/patterns.{}.xml"
{%- endraw -%}

# get integer content of an xml tag in a document
def get_int_by_tag_name(doc, tag_name):
    element = doc.getElementsByTagName(tag_name)
    return int(element[0].firstChild.nodeValue)

values = []

# get number of q-points and cycle through them
xmldoc = minidom.parse(CONTROL_PH_FILENAME)
number_of_qpoints = get_int_by_tag_name(xmldoc, "NUMBER_OF_Q_POINTS")

for i in range(number_of_qpoints):
    # get number of irreducible representations per qpoint
    xmldoc = minidom.parse(PATTERNS_FILENAME.format(i+1))
    number_of_irr_per_qpoint = get_int_by_tag_name(xmldoc, "NUMBER_IRR_REP")
    # add each distinct combination of qpoint and irr as a separate entry
    for j in range(number_of_irr_per_qpoint):
      values.append({
          "qpoint": i + 1,
          "irr": j + 1
      })

# store final values in standard output (STDOUT)
print(json.dumps(values, indent=4))
