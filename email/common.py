#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2014 - Enrico Polesel
# 
# This is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# any later version.
# 
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

import urllib
import urllib.request

import datetime

def send_mail(send_from, send_to, subject, text, files=None, reply_to=None, cc_to=None, bcc_to=None, server="localhost",SSL=False,date=None,references=None,inreplyto=None):
    if files is None:
        files = []
    if reply_to is not None:
        assert isinstance(reply_to, list)
    if cc_to is None:
        cc_to = []
    else:
        assert isinstance(cc_to, list)
    if bcc_to is None:
        bcc_to = []
    else:
        assert isinstance(bcc_to, list)
    assert isinstance(send_to, list)
    assert isinstance(files, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Cc'] =	COMMASPACE.join(cc_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    if reply_to is not None:
        msg['Reply-To'] = COMMASPACE.join(reply_to)
    if date is not None:
        msg['Date'] = date.strftime("%a, %d %b %Y %H:%M:%S %z")
    if references is not None:
        msg['References'] = references
    if inreplyto is not None:
        msg['In-Reply-To'] = inreplyto

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        try:
            part.set_payload( open(f,"rb").read() )
        except:
            pass
        else:
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)
    if SSL:
        smtp = smtplib.SMTP_SSL(server)
    else:
        smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to+cc_to+bcc_to, msg.as_string())
    smtp.close()


def get_baconipsum():
    url = "http://baconipsum.com/api/?type=all-meat"
    page = urllib.request.urlopen(url)
    btext = page.read()
    page.close()
    text = btext.decode()
    text = text.rstrip('"]')
    text = text.lstrip('["')
    return text


def get_randomdate(first,last):
    delta = last-first
    return first + datetime.timedelta(seconds=random.randrange(delta.seconds))


