#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from pprint import pprint
from collections import defaultdict

TEXTCHARS = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})

class ErrorWorker(Exception):
    pass


def include(keys, paths):
# Function for compute common lines

    keys = [key for key in keys if all(path in key for path in paths)]
    
    return keys

def exclude(keys, _exclude):
# Function for compute exceptions

    return [key for key in keys if all(path not in key for path in _exclude)]
    
def unique(keys, files):
    
    return [key for key in keys if len(key) == 1 and (not files or key[0] in files)]


def check_binary(row):

    return bool(row.translate(None, TEXTCHARS))


def dict_creation(paths):
    
    dict_orig = defaultdict(set)

    for filename in paths:
        with open(filename, 'rb') as checkfile:
            for row in checkfile.readlines():
                if check_binary(row):
                    print "File %s seems like a binary, exit." % \
                            os.path.basename(filename)
                    sys.exit(1)
                
                dict_orig[row.rstrip()].add(filename)

    dict_new = defaultdict(list)
    
    for k, v in dict_orig.iteritems():
        dict_new[tuple(v)].append(k)

    return dict_new
        

def main():


    parser = argparse.ArgumentParser()
    
    parser.add_argument("path", nargs='+',
                        help="paths to two or more files "
                             "for comparison")

    parser.add_argument("-e", "--exclude", nargs='+', 
                        help="show common lines in all files, except "
                             "lines in excluded files")

    parser.add_argument("-u", "--unique", nargs='*',
                        help="show unique lines for given files, "
                             "for all if empty")
    
    args = parser.parse_args()

    paths = args.path[:]
    paths.extend(args.exclude or [])

    if len(paths) == 1:
        print "Please specify two or more files."
        return 1

    dict_full = dict_creation(paths)
    keys = dict_full.keys()

    if args.unique is not None:
        keys = unique(keys, args.unique)    

        for key in keys:
            print 'Unique lines in %s:\n---' % key
            print '\n'.join(dict_full[key])
            print ''
        
        return 0

    keys = include(keys, args.path)

    if args.exclude:
        keys = exclude(keys, args.exclude)

    print '\n'.join('\n'.join(dict_full[key]) for key in keys)
        
if __name__ == "__main__":
    main()
