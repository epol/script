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

import smtpd
import email
import datetime
import random
import asyncore
import _thread
import time

import common


sentdate = datetime.datetime.now()
identifier = random.randint(0,2**31)


def init(sender,rcpt,server):
    global identifier
    identifier = random.randint(0,2**31)
    SMTPserver = MySMTPServer(('0.0.0.0',25), 'localhost')
    _thread.start_new_thread(delayed_send,(sender,rcpt,datetime.timedelta(seconds=1),server))
    #delayed_send()
    asyncore.loop()
    

class MySMTPServer(smtpd.SMTPServer):
    def process_message(self,peer, mailfrom, rcpttos, data):
        mail = email.message_from_string(data)
        if mail['Subject'] == "Test "+identifier:
            arrivedate = datetime.datetime.now()
            delta = arrivedate - sentdate
            print("Loop closed in "+str(delta))
            self.close()
        #else:
            #self.close_all()


def delayed_send(sender,rcpt,delay,server):
    global sentdate 
    
    time.sleep(int(delay.total_seconds()))
    sentdate = datetime.datetime.now()
    common.send_mail(sender, [rcpt], "Test "+str(identifier), common.get_baconipsum(), server=server)
    sentdate = datetime.datetime.now()

def main():
    init("enrico.polesel@sns.it","enrico.polesel@sns.it","mail.ngi.it")


if __name__ == "__main__":
    main()


