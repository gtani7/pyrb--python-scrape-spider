#!/usr/bin/env python
# as taken from cookbk: 

import re
htmlDICT = {r'<':r'&lt;',r'>':r'&gt;',r'"':r'&quot;',r'&':r'&amp;' }

# the simplest, lambda-based implementation
def mult_rplc(adict, text):
  # Create a regular expression from all of the dictionary keys
  regex = re.compile("|".join(map(re.escape, adict.keys())))
  # For each match, look up the corresponding value in the dictionary
  return regex.sub(lambda match: adict[match.group(0)], text)

if __name__=='__main__':
    
    testtxt=r'waht HERE<the HERE> HERE<> hay; "is" & '
    outtest=mult_rplc(htmlDICT,testtxt)
    print outtest