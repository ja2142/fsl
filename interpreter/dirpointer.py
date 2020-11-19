#!/usr/bin/python3

import pathlib
import shutil
import os

PATH_ALLOWED_SYMBOLS = ' !"#$%&''()*+,-0123456789:;<=>?@ABCDEFGHIJKLMNOPRSTUVWXYZ[\\]^_`abcdefghijklmnoprstuvwxyz{|}~'

def bytes_to_int(b):
    return int.from_bytes(b, 'big')

def path_index_to_name(i):
    result = ''
    base = len(PATH_ALLOWED_SYMBOLS)
    while i>0:
        result = PATH_ALLOWED_SYMBOLS[i%base] + result;
        i //= base
    if result == '':
        return PATH_ALLOWED_SYMBOLS[0]
    return result

class DirPointer:
    def __init__(self, directory='.'):
        self.path = pathlib.Path(directory).resolve()
    
    def get_child_count(self):
        if not self.path.is_dir():
            return 0
        return len(self.get_children())
    
    def get_children(self):
        if self.path.is_dir():
            entries = os.listdir(bytes(self.path))
            entries.sort(key=bytes_to_int)
            return entries

    def get_siblings(self):
        entries = os.listdir(bytes(self.path.parent))
        entries.sort(key=bytes_to_int)
        return entries

    def get_entry_place(self, entries, name):
        return entries.index(name)
    
    def move(self, n):
        name = os.fsencode(self.path.name)
        entries = self.get_siblings()
        index = self.get_entry_place(entries, name)
        if 0 < index+n < len(entries):
            new_name = entries[index+n]
            self.path = self.path.with_name(os.fsdecode(new_name))
            return True
        return False
    
    def next(self):
        return self.move(1)

    def previous(self):
        return self.move(-1)

    def into(self):
        if self.get_child_count() > 0:
            children = self.get_children()
            self.path = self.path/pathlib.Path(os.fsdecode(children[0]))
            return True
        return False

    def out(self):
        old_path = self.path
        self.path = self.path.parent
        return not (old_path.exists() and self.path.samefile(old_path))
    
    def get_instruction(self):
        #if there's no name the path is at root
        if len(self.path.name) == 0:
            return '!'
        return self.path.name[-1]

    def next_instruction(self, first_into=True):
        if first_into and self.into():
            return
        while not self.next():
            if not self.out():
                return
            if self.get_instruction() == '+':
                return

    def mkdir(self, n=1):
        i = 0
        while n>0:
            try:
                new_path = self.path / path_index_to_name(i)
                new_path.mkdir()
                n -= 1
            except FileExistsError:
                pass
            i += 1

    def rm(self):
        if self.path.is_dir():
            shutil.rmtree(self.path)
        else:
            self.path.unlink()

def main():
    d = DirPointer()
    while d.next_instruction() != '!':
        print(bytes(d.path))

if __name__ == '__main__':
    main()

