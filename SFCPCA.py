#!/usr/bin/env python

infile = open('csvtest.csv','r')
lineNO=0
fieldsPERline=[]
### TEST: simple comma-split 
for line in infile:
    lineNO+=1
    fields_array=line.split(",")
    fieldsPERline.append(len(fields_array))
fieldsPERline.sort()
if fieldsPERline[0]!=fieldsPERline[-1]:
    print("simple comma split of CSV didn't work")
    
## end TEST: simple comma-split

##regexes
dblquote_re=re.compile(r'\"(.*\"))
sglquote_re=re.compile(r'\'(.*\'))
paren_re=re.compile(r'\((.*\)))                    


## ##########from erik
#Questions marks should be erased
#"aka" should be erased
#Names that are in quotes or paranthese need put into the Alias field and the quote or parentheses need to be deleted
#Names that come after "or" need to be moved into the Alias field
#Family relationships: niece, nephew, grand, grandchild, grand*, neph
#Step, twin, triplet should be deleted
                       
    
    
