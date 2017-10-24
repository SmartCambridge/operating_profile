#!/usr/bin/env python3

import xmltodict
import pprint
import sys

with open(sys.argv[1], 'rb') as xml_file:
    content = xmltodict.parse(xml_file)
    print(pprint.pprint(content))