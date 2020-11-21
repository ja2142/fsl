#!/usr/bin/python3

import pathlib
import shutil
import os
import sys
import copy
import argparse

from dirpointer import DirPointer
from instructions import instructions
from str_bytes import *

def log_state(ip, dp, op):
    ip_path = path_to_str_or_bytes(ip.path)
    dp_path = path_to_str_or_bytes(dp.path)
    op_path = path_to_str_or_bytes(op.path)
    instruction = str_to_str_or_bytes(ip.get_instruction())
    if instruction in instructions:
        instruction_description = instructions[instruction][1]
    else:
        instruction_description = 'nop'
    print('IP: {}'.format(ip_path), file=sys.stderr)
    print('DP: {}'.format(dp_path), file=sys.stderr)
    print('OP: {}'.format(op_path), file=sys.stderr)
    print('instr: {} ({})'.format(instruction, instruction_description), file=sys.stderr)
    print('', file=sys.stderr)

def wait_for_return():
    while sys.stdin.read(1) != '\n':
        pass

def load_register(reg_path, default):
    if reg_path.is_symlink():
        reg = os.readlink(reg_path)
    else:
        if reg_path.exists():
            raise RuntimeError('{} exists and is not a symlink'.format(reg_path))
        os.symlink(default, reg_path)
    return default

def load_state(directory):
    directory = DirPointer(os.path.abspath(directory))
    regs_dir = directory.path / '='
    if not regs_dir.exists():
        regs_dir.mkdir()
    IP_path = regs_dir / 'IP'
    DP_path = regs_dir / 'DP'
    OP_path = regs_dir / 'OP'
    directory.into()
    ip = DirPointer(load_register(IP_path, directory.path))
    dp = DirPointer(load_register(DP_path, directory.path))
    op = DirPointer(load_register(OP_path, directory.path))
    return (ip, dp, op)

def main():
    parser = argparse.ArgumentParser(description='fsl++# interpreter. CAUTION: MIGHT DELETE FILES AND DIRECTORIES!')
    parser.add_argument('-l', '--log', help='log registers at each step', action='store_true')
    parser.add_argument('-s', '--step', help='wait for return before each instruction', action='store_true')
    parser.add_argument('-c', '--instruction-count', help='execute at most n instructions', type=int, default=1000)
    parser.add_argument('directory', help='directory to be executed')
    args = parser.parse_args()
    ip2, dp2, op2 = load_state(args.directory)
    log_state(ip2, dp2, op2)
    ip = DirPointer(args.directory)
    ip.into()
    dp = copy.deepcopy(ip)
    op = copy.deepcopy(ip)
    instruction = ''
    instruction_limit = args.instruction_count
    while instruction != '!':
        instruction = ip.get_instruction()
        if args.log:
            log_state(ip, dp, op)
        if args.step:
            wait_for_return()
        if instruction in instructions:
            ip, dp, op = instructions[instruction][0](ip, dp, op)
        else:
            ip.next_instruction()
        instruction_limit -= 1
        if instruction_limit <= 0:
            break


if __name__ == '__main__':
    main()

