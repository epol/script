#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# saverescueall.py
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

# REQUIREMENTS:
# - install Junos PyEZ:
#   $ pip install junos-eznc
# - enable ssh netconf on the target switches:
#   [configure] set system services netconf ssh

import jnpr.junos
import argparse
import sys
import logging
import os
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument("-u","--username", help="Username", required=False)
#parser.add_argument("-p","--password", help="User password (required if not using SSH keys)", required=False)
parser.add_argument("-k","--ssh-key", help="Private SSH key location", required=False)
parser.add_argument("-ll", "--log-level", help="Logger log level",required=False)
parser.add_argument("-ih","--icingahost", help="Hostname of the icinga host", required=True)
parser.add_argument("-iu","--icingausername", help="Username for the icinga API", required=True)
parser.add_argument("-ip","--icingapassword", help="Password for the icinga API", required=True)

args = parser.parse_args()

logger = logging.getLogger(sys.argv[0])
logger.propagate = False
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)-9s %(levelname)-8s %(message)s',datefmt='%H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
if args.log_level is not None:
    logger.setLevel(args.log_level)


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

if args.username:
    username = args.username
else:
    username = os.getlogin()

for host in r.json()['results']:
    try:
        device = jnpr.junos.Device(host=host['attrs']['address'],user=username,ssh_private_key_file=args.ssh_key)
        device.open()
    except:
        logger.error("Unable to open device {address}".format(**host['attrs']))
        continue
    else:
        logger.info("Connected to "+device.facts['hostname'])
        
    logger.debug("Sending RPC to target")
    response = device.rpc.request_save_rescue_configuration()                

    logger.debug("Reading response")
    for re in response.findall('routing-engine'):
        name = re.find('name').text
        if re.find('output') is not None:
            output = re.find('output').text.strip()
        elif re.find('success') is not None:
            output = 'success'
        else:
            output = 'unknown'
        logstring = "Routing engine {name} result is {output}".format(name=name,output=output)
        if output == 'success':
            logger.info(logstring)
        else:
            logger.critical(logstring)

    logger.debug("Closing target")
    device.close()
