#!/usr/bin/env python
import re
lead2quote=re.compile(r'(^|\,)\"~~~')		##inserted: (^|\,)
trail2quote=re.compile(r'~~~\"(\,|$)')		##insert: (\,|$)
leaddelim=re.compile(r'^\"?~~~')		## this and next re: ins'd \"?
traildelim=re.compile(r'~~~\"?$')

front2quote=re.compile(r'^\"')
back2quote=re.compile(r'\"$')	

allblank=re.compile(r'^\s*$')
delim_re=re.compile(r'~~~,~~~')
delim=r'~~~,~~~'


## for splitting, cleaning dbin.txt     ## 4 tildes bef, aft each field
delim4_re=re.compile(r'~~~~,~~~~')
delim4=r'~~~~,~~~~'

def split_clean(dbin_line):
        # split > 12 flds;;     excl cols. 5,9 (count'g from 1)
    dbin_line_split=delim_re4.split(dbin_line)
    dbin_line_split[0]= dbin_line_split[0].replace("~~~~","")
    dbin_line_split[-1]= dbin_line_split[11].replace("~~~~","")
    
    
    return dbin_line_split