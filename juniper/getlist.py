#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# getlist.py
# This file is part of epol/script
#
# Copyright (C) 2017 - Enrico Polesel
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import sys
import json
import requests
import re


parser = argparse.ArgumentParser()
parser.add_argument("-i","--icingahost", help="Hostname of the icinga host", required=True)
parser.add_argument("-u","--icingausername", help="Username for the icinga API", required=True)
parser.add_argument("-p","--icingapassword", help="Password for the icinga API", required=True)

args = parser.parse_args()

icinga_session = requests.Session()
icinga_session.verify = False
icinga_session.auth = (args.icingausername,args.icingapassword)

icinga_url = 'https://'+args.icingahost+':5665/v1/'


r = requests.post(icinga_url+'objects/hosts',
           headers={'X-HTTP-Method-Override':'GET'},
                  verify=False,auth=(args.icingausername,args.icingapassword),
                  data=json.dumps({'attrs': ['name','address','display_name'],
                                   'filter': 'host.vars.os=="Junos"'}))

r.raise_for_status()

outinventory = "[junos]\n"

for host in r.json()['results']:
    print("{name}: {address}".format(**host['attrs']))
    outinventory += "{address}\n".format(**host['attrs'])

with open('junos-inventory.ini','w') as f:
    f.write(outinventory)
