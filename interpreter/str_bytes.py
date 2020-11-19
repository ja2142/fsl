#!/usr/bin/python3

import os

def path_to_str_or_bytes(path):
    try:
        return str(path).encode('utf8').decode('utf8')
    except UnicodeEncodeError:
        return bytes(path)

def str_to_str_or_bytes(s):
    try:
        return str(s).encode('utf8').decode('utf8')
    except UnicodeEncodeError:
        return os.fsencode(s)

def bytes_to_str_or_bytes(b):
    try:
        return b.decode('utf8')
    except UnicodeDecodeError:
        return b

