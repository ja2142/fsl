#!/usr/bin/python3

import pathlib
import shutil
import os
import struct
import copy

import dirpointer

# DP operations
def dp_next(ip, dp, op):
    dp.next()
    ip.next_instruction()
    return (ip, dp, op)

def dp_previous(ip, dp, op):
    dp.previous()
    ip.next_instruction()
    return (ip, dp, op)

def dp_out(ip, dp, op):
    dp.out()
    ip.next_instruction()
    return (ip, dp, op)

def dp_into(ip, dp, op):
    dp.into()
    ip.next_instruction()
    return (ip, dp, op)

def dp_last(ip, dp, op):
    dp.last()
    ip.next_instruction()
    return (ip, dp, op)

# OP operations
def op_next(ip, dp, op):
    op.next()
    ip.next_instruction()
    return (ip, dp, op)

def op_previous(ip, dp, op):
    op.previous()
    ip.next_instruction()
    return (ip, dp, op)

def op_out(ip, dp, op):
    op.out()
    ip.next_instruction()
    return (ip, dp, op)

def op_into(ip, dp, op):
    op.into()
    ip.next_instruction()
    return (ip, dp, op)

# DP amd OP operations
def op_to_dp(ip, dp, op):
    op = copy.deepcopy(dp)
    ip.next_instruction()
    return (ip, dp, op)

def dp_to_op(ip, dp, op):
    dp = copy.deepcopy(op)
    ip.next_instruction()
    return (ip, dp, op)

# flow control
def skip_dir(ip, dp, op):
    ip.next_instruction(first_into=False)
    return (ip, dp, op)

def conditional_execute(ip, dp, op):
    ip.next_instruction(first_into=(dp.get_child_count() > 0))
    return (ip, dp, op)

# dir IO
def mkdir(ip, dp, op):
    dp.mkdir()
    ip.next_instruction()
    return (ip, dp, op)

def rm(ip, dp, op):
    dp.rm()
    dp.out()
    ip.next_instruction()
    return (ip, dp, op)

def rm_at(ip, dp, op):
    children = dp.get_children()
    if len(children) > 0:
        child = dirpointer.DirPointer(dp.path / os.fsdecode(children[0]))
        child.rm()
    ip.next_instruction()
    return (ip, dp, op)


# file IO
def file_write(ip, dp, op):
    with open(op.path, 'wb') as out_file:
        byte_out = dp.get_child_count() % 256
        out_file.write(struct.pack('B', byte_out))
    ip.next_instruction()
    return (ip, dp, op)

def file_read(ip, dp, op):
    with open(op.path, 'rb') as in_file:
        byte_in = struct.unpack('B', in_file.read(1))[0]
        dp.mkdir(byte_in)
    ip.next_instruction()
    return (ip, dp, op)

def nothing(ip, dp, op):
    return (ip, dp, op)

instructions = {
        '>': (dp_next, 'DP next'),
        '<': (dp_previous, 'DP previous'),
        '^': (dp_into, 'DP into'),
        '_': (dp_out, 'DP out'),
        '$': (dp_last, 'DP to last'),
        
        '}': (op_next, 'OP next'),
        '{': (op_previous, 'OP previous'),
        '`': (op_into, 'OP into'),
        ',': (op_out, 'OP out'),

        '&': (op_to_dp, 'OP=DP'),
        '%': (dp_to_op, 'DP=OP'),
        
        # loop and if are handled the same here, because the loop is handled
        # differently at next_instruction()
        '?': (conditional_execute, 'if DP not empty'),
        '+': (conditional_execute, 'while DP not empty'),
        '=': (skip_dir, 'ignore dir'),
        
        '*': (mkdir, 'create dir at DP'),
        'x': (rm, 'remove file at DP, DP out'),
        'X': (rm_at, 'remove first child of DP'),
        
        'o': (file_write, 'write to OP'),
        'i': (file_read, 'read from OP'),

        # program termination is handled at the top level
        '!': (nothing, 'terminate program'),
}

def main():
    pass

if __name__ == '__main__':
    main()

