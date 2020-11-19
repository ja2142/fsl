#!/usr/bin/python3

import os
import argparse
import colorama

from interpreter.dirpointer import DirPointer
from interpreter.str_bytes import bytes_to_str_or_bytes

def main():
    parser = argparse.ArgumentParser(description='simple ls, with sorting according to fsl')
    parser.add_argument('-l', '--long', help='long list', action='store_true')
    parser.add_argument('-c', '--count', help='print children count', action='store_true')
    parser.add_argument('directory', help='directory to be executed', default='.', nargs='?')
    args = parser.parse_args()

    print(args)

    path = DirPointer(args.directory)
    if not path.path.is_dir():
        print('{} isn''t a directory'.format(path.path))
        return
    
    children = path.get_children()
    for child in children:
        child = bytes_to_str_or_bytes(child)
        child_path = path.path / os.fsdecode(child)
        style = ''
        if child_path.is_dir():
            style = colorama.Fore.BLUE + colorama.Style.BRIGHT
        elif child_path.is_symlink():
            style = colorama.Fore.CYAN + colorama.Style.BRIGHT
        elif not child_path.is_file():
            style = colorama.Fore.YELLOW + colorama.Style.BRIGHT
        child_with_colors = '{}{}{}'.format(style, child, colorama.Style.RESET_ALL)
        if args.long:
            print('{}'.format(child_with_colors))
        else:
            print('{}'.format(child_with_colors), end='  ')
    
    if not args.long:
        print('')
    
    if args.count:
        print('count: {}'.format(len(children)))

main()

