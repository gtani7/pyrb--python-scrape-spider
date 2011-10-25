#!/usr/bin/env python
## do distributn for #s of mail.py.org URLs for each level of dbin.txt row head'gs (1-4)
infile = open('dbin.txt','r')
outfile = open('pyrbURLSbyROWheadg.txt','w')

import re
from regexes import split_clean

col1urls={};        col2urls={};        col3urls={};        col4urls={};

## reg exp's
cells_in_row=[]  ## test if all rows have 12 cells
rownum=0

for dbin_line in infile:
    split_line=split_clean(dbin_line)
    cells_in_row.append(len(split_line)    )
    if len(split_line)>19:
        print split_line
        print
    
    rownum+=1
    # determ if we're looking at col, 1,2,3,4
cells_in_row.sort()
print "lowest # of cells:\n"
print cells_in_row[0:25]
print "\nhighest # of cells:\n"
print cells_in_row[-25:-1]
    
    # split URLs in col. 3 for py, rb;;     look for mail.py.org, blade.nagaoka.ut
    # col 1: bucket by 1-2, 3-4, 5-8, 9+
    # col 2+: 0,1,2,3,4+
