#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import ntpath
import argparse

from collections import defaultdict

def diff_compute():
# Function for compute different lines
    print "Diff computing"

def comm_compute():
# Function for compute common lines
    print "Comm computing"

def check_binary(row):
# Function for check type of file:
# it check a string for existence of special 
# characters which will not to be in plain text files.
# Stackoverflow deepdive, in two words.
    
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary = lambda bytes: bool(bytes.translate(None, textchars))

    return is_binary(row)

def dict_creation(path):
    
    dict_orig = defaultdict(set)

    for filename in path:
        with open(filename, 'rb') as checkfile:
            for row in checkfile.readlines():
                if check_binary(row):
                    print "File %s seems like a binary, exit." % filename
                    sys.exit(1)
               
                dict_orig[row].add(filename)

    dict_new = defaultdict(list)
    
    for k, v in dict_orig.iteritems():
        dict_new[tuple(v)].append(k)
    
    return dict_new
        
def main():

    # Defining available arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--comm", help="Common lines in all files", action="store_true")
    parser.add_argument("-d", "--diff", help="Different lines in all files", action="store_true")
    parser.add_argument("path", nargs='+', help="Path to files for comparison")
    args = parser.parse_args()

    if args.comm:
        comm_compute()

    if args.diff:
        diff_compute()

    if len(args.path) == 1:
        print "Please specify two or more files."
        sys.exit(1)

    result = dict_creation(args.path)

    from pprint import pprint
    pprint(result)
        

    # if args.path:
    #     count = len(args.path)
    #     if count > 2:
    #         print "Too much arguments!"
    #     else:
    #         print count
    # for file in args.path[0:]:
    #   print file

if __name__ == "__main__":
    main()
