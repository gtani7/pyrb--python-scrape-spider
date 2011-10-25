#!/usr/bin/env python
import re
def strip2quote(str_arg):
    re_lead_trail_2quote=re.compile(r'^"(.*)"$')
    try:
        matchobject=re_lead_trail_2quote.match(str_arg)
        return matchobject.group(1)
    except AttributeError:
        return ""

import sys, os, re, copy, pickle
if len(sys.argv)==1:            ## NO switches
    in_rowheadgs_file = open('pyrbhead.txtout.txt','r')         ## FILES
    out_rowheadgs_file=open('pyrbhead2.txtout.txt','w')
else:                           ## "r" switch
    in_rowheadgs_file = open('railshead.txtout.txt','r')         ## FILES
    out_rowheadgs_file=open('railshead2.txtout.txt','w')

                    #REG EX
re_2dblquote=re.compile(r'""')
re_leadgdblquote=re.compile(r'^"');         re_trailgdblquote=re.compile(r'"$')

lines_normal_order=in_rowheadgs_file.readlines( )
mat_celldiffs=[]
num_cantfind1=0;                num_not8cells=0
for indx,oneline in enumerate(lines_normal_order):
    immed_parent_rownum=None
    rownum_col1headg, rownum_thisrow, fourrowheadgs=oneline.split(',',2)
    fourrowheadgs=fourrowheadgs.rstrip()
    #fourrowheadgs=[strip2quote(x) for x in fourrowheadgs]
    try:
        rownum_col1headg, rownum_thisrow=int(rownum_col1headg), int(rownum_thisrow)
    except ValueError:
        print "VALUE ERR: rownum_col1headg, rownum_thisrow: ***" +  rownum_col1headg + "***"+rownum_thisrow+"~~~"
    if rownum_col1headg==rownum_thisrow:
        immed_parent_rownum=0       #rewrite for each row in Part 2: 0 or pos integ.  "None" shd be error-trapped
    rowheadgs_arr=fourrowheadgs.split('","')
                                                                    ## FIXME: rowheadgs_arr[0] needs to be cleaned of 2 leading int's
    rowheadgs_arr[0]=re_leadgdblquote.sub("",rowheadgs_arr[0])
    try: 
        rowheadgs_arr[3]=re_trailgdblquote.sub("",rowheadgs_arr[3])
        
    except IndexError:
        print "IndErr  "+"indx: "+str(indx)
        print "oneline: "+oneline.rstrip() + "  ## ok if: Last Line"
        continue
    #if indx>6519:
    #    print "indx: "+repr(indx)
    #    print "rowheadgs_arr[]: "+repr(rowheadgs_arr)
    mat_celldifs_onerow=[rownum_col1headg, rownum_thisrow, immed_parent_rownum]
    #if indx>6519 and indx<6526:
    #    print "indx: "+repr(indx)
    #    print "mat_celldifs_onerow, 1st 3 entries: "+repr(mat_celldifs_onerow)
    #
    for indx_0to3, cellcontent in enumerate(rowheadgs_arr):
        try:
            if 0==len(cellcontent ):        ## 
                mat_celldifs_onerow.append(0)
            elif cellcontent != rowheadgs_prevrow[indx_0to3]:
                mat_celldifs_onerow.append(1)
            else: 
                mat_celldifs_onerow.append(0)
        except IndexError:
            print "Find col. of 1st diff fr row above:: row # of IndErr: "+repr(indx)
            print "Addit info: cellcontent: "+repr(cellcontent)
            print "Addit info: rowheadgs_prevrow: "+repr(rowheadgs_prevrow)
            
        except NameError:       #1st row of pyrbhead.txt, which is row 1 fo pyrb.xls, which is just col. headgs
            print "Line 64: Name err when Find col. of 1st diff fr row above::"
            continue
    try:
        mat_celldifs_onerow.insert(3,mat_celldifs_onerow[3:].index(1))
    except ValueError:
        num_cantfind1+=1
        if num_cantfind1<142:    ## 2 follow'g Err msgs "Can't find 1" and "NOT 8 cells" occur where set of row head'gs is repeated
                                                    ## i.e., shd not recv Err msg, so fix in .XLS
            print "Can't find 1 in vec of 4 row diffs: Record "+repr(indx)+": "+repr(rowheadgs_arr)           ## 1st EXPLODE
    if 8==len(mat_celldifs_onerow):
        mat_celldiffs.append(mat_celldifs_onerow)
    else:                                                                               ## 2nd EXPLODE
        num_not8cells+=1
        if ((num_not8cells>37 and len(sys.argv)==1) or (len(sys.argv)>1 and num_not8cells>56)):                    ## threshold val (34) set for py/rb, NOT rails
            print "NOT 8 cells to append to mat of row diffs: "+repr(indx)+":  "+repr(rowheadgs_arr) #shd only be 1st, last line of pyrbhead.txtout
    rowheadgs_prevrow  =   rowheadgs_arr
print "Total recs, can't find 1 in vec of 4 row diffs: "+repr(num_cantfind1)
print "Total recs, not 8 cells to append: "+repr(num_not8cells)+"\n"
print "len(mat_celldiffs): "+repr(len(mat_celldiffs))

if len(sys.argv)==1:
    mat_concatted_rowheadgs=[ ["Language Comparisons","","",""] ]
else:
    mat_concatted_rowheadgs=[ ["Overview/architecture diagram","","",""] ]
num_indx_err=0
for indx2,oneline in enumerate(lines_normal_order):
    if 0==indx2:
        continue
    immed_parent_rownum=None
    rownum_col1headg, rownum_thisrow, fourrowheadgs=oneline.split(',',2)
    fourrowheadgs=fourrowheadgs.rstrip().split('","')
    #if indx2 <4:
    #    print "l.62: fourrowheadgs"+repr(fourrowheadgs)
    try:
        col_firstdiff=mat_celldiffs[indx2-1][3]
        #if indx2<4:
        #    print "col_firstdiff: "+repr(col_firstdiff)
    except IndexError:
        num_indx_err+=1
        if num_indx_err<5:
            print "IndErr: indx for building array of concatted row headgs: "; print indx2
        
    #curr_rowheadgs[col_firstdiff:]=copy.copy(fourrowheadgs[col_firstdiff:])    ##HOPELESS: deep copy? or 
    #mat_concatted_rowheadgs.append(copy.copy(curr_rowheadgs))
    mat_concatted_rowheadgs.append(["","","",""])
    for i in range(4):
        mat_concatted_rowheadgs[indx2][i]=mat_concatted_rowheadgs[indx2-1][i]
        
    for j in range(col_firstdiff,4):
        try:
            mat_concatted_rowheadgs[indx2][j]=    fourrowheadgs[j]
        except IndexError:
            print "line giv'g IndxErr: "+str(indx2)
            continue
    
## pickle it for cons_outfile1.py
if len(sys.argv)==1:
    f = open("array_concatted_headgs.pkl", "wb");    pickle.dump(mat_concatted_rowheadgs, f)
    print "array_concatted_headgs.pkl: len: "+repr(len(mat_concatted_rowheadgs))
else:
    f = open("array_concatted_headgs_rails.pkl", "wb");    pickle.dump(mat_concatted_rowheadgs, f)
    print "array_concatted_headgs_rails.pkl: len: "+repr(len(mat_concatted_rowheadgs))
for i in range(2):                        ## DEBUG
    print "row: "+repr(i)+"   "+repr(mat_celldiffs[i])  ## DEBUG
            # mat_celldiffs:
            #    [0,1] ultimate, this parent from pyrbhead.txtout
            #    [2] 0 or None ## precursor to immed parent
            #    [3] index of col of first diff i.e. blank to nonblank row head'g.  NOT: nonblank to blank row head'g
            #    [4-7] diff from prev row?  (0/1)
indx_pyrbhead=2
indx_mat_celldiffs=1    # mat_celldiffs[1] <=> pyrbhead.txtout[2];; 1st row of mat_celldiffs is throwaway
####  find "rgt" value for each row
no_rgtval_err=0
to_push=copy.copy(mat_celldiffs[0])
to_push[1]=to_push[0]
to_push[3:]=[0,1,0,0,0]
mat_celldiffs.insert(0,to_push)
array_rgt_values=[]
#print "mat_celldiffs: "; print repr(mat_celldiffs[0]); print repr(mat_celldiffs[1]);print repr(mat_celldiffs[2]);   ## DEBUG
#print "len(mat_celldiffs): "+repr(len(mat_celldiffs))
for indx_mat_celldiffs in range(0,-1+len(mat_celldiffs)):
    current_indent=mat_celldiffs[indx_mat_celldiffs][3]
    for indx_searchfor_rgt in range(indx_mat_celldiffs +1,-1+len(mat_celldiffs)):
        if (indx_searchfor_rgt == 1+indx_mat_celldiffs) and (mat_celldiffs[indx_searchfor_rgt][3] <= current_indent):
            array_rgt_values.append(1+mat_celldiffs[indx_mat_celldiffs][1])     ## leaf node:: rgt=lft + 1
            break
        elif mat_celldiffs[indx_searchfor_rgt][3] <= current_indent:
            array_rgt_values.append(mat_celldiffs[indx_searchfor_rgt][1])
            break
        if indx_searchfor_rgt==-1+len(mat_celldiffs):
            no_rgtval_err+=1
            if no_rgtval_err<6:    
                print "No RGT value found: row"
                print repr(indx_mat_celldiffs )
                array_rgt_values.append(None)
#print "array_rgt_values";  print array_rgt_values[0:22]; print array_rgt_values[-6:-1]      ##  DEBUG
print "len(array_rgt_values): "+str(len(array_rgt_values))
if len(sys.argv)==1:
    f = open("array_rgt_values.pkl", "wb");    pickle.dump(array_rgt_values, f)
else: 
    f = open("array_rgt_values_rails.pkl", "wb");    pickle.dump(array_rgt_values, f)
### find immed par
mat_celldiffs=mat_celldiffs[1:]
for indx_mat_celldiffs in range(1,len(mat_celldiffs)):
    ## go up to x rows up in mat_celldiffs, OTW report ImmedPar > XX rows up
    
    if 0==mat_celldiffs[indx_mat_celldiffs][2]:
        flds=lines_normal_order[indx_mat_celldiffs+1].split(",",1)
        lines_normal_order[indx_mat_celldiffs+1]=flds[0]+",0,"+flds[1]
    col_of_1stdiff=mat_celldiffs[indx_mat_celldiffs ][3]
    for i in range(130):        ## not enuf for e.g. acts_as_* in rails sheet;; also:  SVN, capistr, caching,input form, 
                                ## lang sheet: textmate, vim, emacs, SVN, 
        if (indx_mat_celldiffs-i<0):
            # print "Oh, oh ran off top of mat_celldiffs, can't find imm.parent: "+repr(indx_mat_celldiffs) #DEBUG
            break
        if (mat_celldiffs[indx_mat_celldiffs-i][3]<col_of_1stdiff):
            #mat_celldiffs[indx_mat_celldiffs][2]=mat_celldiffs[indx_mat_celldiffs-i][1]    ##
            flds=lines_normal_order[indx_mat_celldiffs+1].split(",",1)
            lines_normal_order[indx_mat_celldiffs+1]=flds[0]+","+repr(mat_celldiffs[indx_mat_celldiffs-i][1] )+","+flds[1]
            break
        if i==130:          ## XX
            print "Oh, oh, this row immed parent more than 130 rows up?! "+repr(indx_mat_celldiffs)
#lines_normal_order.insert(0,           #fix 1st line

#for i in range(1,4):
#    print lines_normal_order[i]+"\n"
out_rowheadgs_file.writelines(lines_normal_order)
out_rowheadgs_file.close()
    