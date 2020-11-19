#!/usr/bin/python3

import sys
import os

MK_FILES = '-f' in sys.argv
for arg in sys.argv:
    try:
        n = int(arg)
        break
    except ValueError:
        pass

if type(n) != int:
    sys.exit('no number of directories provided')

for i in range(n):
    if MK_FILES:
        os.system('touch {}'.format(i))
    else:
        os.system('mkdir {}'.format(i))

