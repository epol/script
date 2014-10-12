#!/usr/bin/env python3.2 
# -*- coding: utf-8 -*-

# Copyright (C) 2013 - Enrico Polesel
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/>.

import argparse
#import sys

error_place = []

def elaborate_line(line,debug,usePM=False,replaceD=False):
    ar = line.split("\t")
    if debug:
        print (ar)
    out_line = ""
    index = 0
    for element in ar:
        if (element != ""):
            if element.startswith("D") or element.startswith("∆"):
                error_place.append(index)
                if replaceD:
                    element = element.lstrip("D")
                    element = element.lstrip("∆")
                    element = "\\Delta "+element
            
            if usePM and (index in error_place):
                out_line = out_line.rstrip(" & ")
                out_line = out_line + " \pm "
            out_line = out_line + element + " & "
            index = index +1
    out_line = out_line.strip(" & ")
    out_line = out_line + " \\\\ \n"
    if index != 0:
        return out_line
    else:
        return ""


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="A tool to convert a gnuplot compatibile table in a latex table")
    parser.add_argument("file")
    parser.add_argument("-d","--debug", help="Enable debug output",action="store_true")
    parser.add_argument("-t","--title", help="Use a # as a title trigger for the first line",action="store_true")
    parser.add_argument("-p","--pm",help="Use \pm for error (implies -t)",action="store_true")
    parser.add_argument("-o","--output",help="Write output to file",type=str)
    args = parser.parse_args()
    
    
    infile = open(args.file,"r")
    
    
    out_text = ""
    for line in infile:
        line = line.strip()
        if (line.startswith("#")):
            if ((args.title  or args.pm) and out_text == ""):
                line = line.lstrip("#")
                line = line.strip()
                out_text = out_text + elaborate_line(line,args.debug,args.pm,True)
                out_text = out_text + "\\hline \n"
                
            else:
                continue
        else :
            out_text = out_text + elaborate_line(line,args.debug,args.pm)
            
    if args.debug:
        print ("")
    if args.output == None:
        print (out_text)
    else:
        outfile = open(args.output,"w")
        outfile.write(out_text)


if __name__ == "__main__":
    main()
