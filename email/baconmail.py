#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2012 - Enrico Polesel
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
# along with this software. If not, see
# <http://www.gnu.org/licenses/>.

import datetime

import common

def main():
    for i in range(4):
        common.send_mail("enrico.polesel@sns.it",
                         ["enrico.polesel@sns.it"],
                         subject="Test bacon "+str(i),
                         text=common.get_baconipsum(),
                         server="mail.sns.it",
                         date=common.get_randomdate(datetime.datetime.now() + datetime.timedelta(hours=-2),
                                                    datetime.datetime.now() + datetime.timedelta(minutes=10))
                  )



if __name__=="__main__":
    main()
