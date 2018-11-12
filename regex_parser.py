#!/usr/bin/env python

import sys


STATE_START = 0
STATE_PARTS = 1
STATE_FLAGS = 2

ACTION_SUB = 0
ACTION_DEL = 1
ACTION_MAT = 2

FLAG_GLOBAL = 0
FLAG_CASEIN = 1


class RegexParseError(Exception):
    pass


class RegEx(object):
    """docstring for RegEx"""
    def __init__(self, arg):
        super(RegEx, self).__init__()
        self.arg = arg
        

class RegExSub(RegEx):


class RegExDel(RegEx):


class RegExMat(RegEx):


def parse_regex(complex_regex):
    action = None
    parts = []
    flags = set()
    pos = 0
    state = STATE_START
    regex_start = 0
    while pos < len(complex_regex):
        ch = complex_regex[pos]
        if ch == '\\':  # single '\' character
            pos += 2
            continue

        if state == STATE_START:
            if ch == 's':
                action = ACTION_SUB
                delim = complex_regex[1]
            elif ch == 'd':
                action = ACTION_DEL
                delim = complex_regex[1]
            else:
                action = ACTION_MAT
                delim = complex_regex[0]
                pos -= 1  # going down cause action defined by character
                          # absence

            # action not none or single character
            if complex_regex[pos + 1] != delim:
                raise RegexParseError("Invalid regular expression '%s'" %
                                      complex_regex)

            pos += 2
            regex_start = pos
            state = STATE_PARTS

        elif state == STATE_PARTS:
            if ch == delim:
                parts.append(complex_regex[regex_start:pos])
                if len(parts) == 2:
                    if action != ACTION_SUB:
                        raise RegexParseError("Invalid action or regular expression '%s'" %
                                          complex_regex)
                    state = STATE_FLAGS

                regex_start = pos + 1  # character after delimeter

            pos += 1

        elif state == STATE_FLAGS:
            if ch in 'gi':
                flags.add(ch)
            else:
                raise RegexParseError("Unknown flag '%s'" % ch)

            pos += 1

    if not (action is not None and parts):
        raise RegexParseError("Invalid regular expression '%s'" %
                              complex_regex)

    if action == ACTION_SUB and len(parts) != 2:
        raise RegexParseError("Substitution needs two parts of regular "
                              "expression")

    return action, parts, flags

def main():
    
    regex = sys.argv[1]
    
    try:
        print parse_regex(regex)
    except RegexParseError as e:
        print e


if __name__ == "__main__":
    main()