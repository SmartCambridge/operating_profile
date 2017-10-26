#!/usr/bin/env python3

import xmltodict
import pprint
import sys
import json

with open(sys.argv[1], 'rb') as xml_file:
    content = xmltodict.parse(xml_file)
    #print(pprint.pprint(content))
    print(json.dumps(content, indent=2))