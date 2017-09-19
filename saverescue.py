#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# saverescue.py
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
# - enable ssh netconf on the target switch:
#   [configure] set system services netconf ssh

import jnpr.junos
import argparse
import sys
import logging
import os

parser = argparse.ArgumentParser()
parser.add_argument("target", help="Switch hostname or IP")
parser.add_argument("-u","--username", help="Username", required=False)
#parser.add_argument("-p","--password", help="User password (required if not using SSH keys)", required=False)
parser.add_argument("-k","--ssh-key", help="Private SSH key location", required=False)
parser.add_argument("-ll", "--log-level", help="Logger log level",required=False)

args = parser.parse_args()

logger = logging.getLogger(sys.argv[0])
logger.propagate = False
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)-9s %(levelname)-8s %(message)s',datefmt='%H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
if args.log_level is not None:
    logger.setLevel(args.log_level)

if args.username:
    username = args.username
else:
    username = os.getlogin()

try:
    device =  jnpr.junos.Device(host=args.target,user=username,ssh_private_key_file=args.ssh_key)
    device.open()
except:
    logger.error("Unable to open device")
    sys.exit(1)
else:
    logger.info("Connected to "+device.facts['hostname'])

#print(device.cli("request system configuration rescue save"))
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
