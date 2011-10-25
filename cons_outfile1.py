#!/usr/bin/env python
### BEFORE RUN this prog: edit pyrbhead2.txtout.txt, insert immed_par for 1st few records
import re, sys, pickle

def add100k(int_as_str,increm_100k_200k):
    if "\\N"==int_as_str:
        return "\\N"
    try: 
        return repr(increm_100k_200k+int(int_as_str))
    except TypeError:
        print "add100k(): can't convert int_as_str"
    
FIELD_TERMINATED_BY="~~~~,"                         #########  CONSTANTS, counters
numrows_noimmedpar=0
#3/10/07: add "rgt" field for a_a_nested
if len(sys.argv)==1:
    f = open("array_rgt_values.pkl", "rb");  array_rgt_values = pickle.load(f)
    f = open("array_concatted_headgs.pkl", "rb");  array_concatted_headgs = pickle.load(f)
else:
    f = open("array_rgt_values_rails.pkl", "rb");  array_rgt_values = pickle.load(f)
    f = open("array_concatted_headgs_rails.pkl", "rb");  array_concatted_headgs = pickle.load(f)
    
print "array_concatted_headgs: "+repr(array_concatted_headgs[0:2])
                               
if len(sys.argv)<2:                                  #########  FILES                       
    in_rowheadgs_file=open('pyrbhead2.txtout.txt','r')
    in_dbin_txt=open('dbin.txt','r')
    out_noimmedpar_file=open('noimpar_pyrb.txt','w')
    out_dbin_rb=open('dbin_rb.txt','w')     #mySQL LOAD DATA INFILE
    out_dbin_py=open('dbin_py.txt','w')
elif "r"==sys.argv[1][0].lower():			#arg is "rails"
    in_rowheadgs_file=open('railshead2.txtout.txt','r')
    in_dbin_txt=open('dbin_rails.txt','r')
    out_noimmedpar_file=open('noimpar_rails.txt','w')
    out_dbin_py=open('dbin_rails2.txt','w')  
                                
re_leadingdigit=re.compile(r'\d')                 ######## REG EXes
re_5tilde=re.compile(r'~~~~~,')
re_newline=re.compile(r'\n')
re_allwhitespace_commas=re.compile(r'^,\w+$')
########                        #####
lines_normal_order=in_rowheadgs_file.readlines( )

# 
dbin_txt=in_dbin_txt.readlines()
print "length(dbin_txt)== "+repr(len(dbin_txt))         ## PERM DIAGnostic
i=0
for indx,oneline in enumerate(lines_normal_order):
    #if indx<2:
    #    i+=1
    #    continue
    rest_of_line=""
    ult=immed=thisrow=""            # strings, i.e. never cast to integ.
    (fld1, fld2, rest_of_line) = oneline.split(",",2)
                    ######### dbin.txt proc'd below, to 
    try:
        # dbin_flds=dbin_txt[i].split("~~~~,")
        dbin_fields=dbin_txt[i].split( FIELD_TERMINATED_BY )
        dbin_fields[-1].replace(FIELD_TERMINATED_BY ,"")
        #print "len(dbin_flds) => "+repr(len(dbin_fields))       ## DEBUG
    except IndexError:
        print "IndErr: row "+repr(i)            ## shd only be last line of pyrbhead2.txtout
    dbin_ult=dbin_fields[0];      dbin_this=dbin_fields[1];
    
    ## pyrbhead2.txtout
    if not(re_leadingdigit.match(rest_of_line[0])):
        out_noimmedpar_file.write("line "+repr(indx)+" missing immed par: "+rest_of_line )  ## BIG ASSUMPTION: all row headings enclosed dbl quotes only
        numrows_noimmedpar+=1
        immed=ult=fld1;         thisrow=fld2;
    else:
        ult=fld1; immed=fld2;
        (thisrow,rest_of_line)=rest_of_line.split(",",1)
    ## confirm 2 files are synced // corr index    
    if ( (thisrow != dbin_this) or (ult !=dbin_ult) ):
        print "!! ## !! Darn~! : misaligned files: row num: "+repr(i)+"row headgs:   " + rest_of_line
                                                                          ## ## ## check if py, rb rows BLANK
    dbin_fields_no_newline=[dbin_field.replace ("\n","") for dbin_field in dbin_fields]     ##DOESN'T DO ANYTHING
    #print "len(dbin_fields_no_newline: "+repr(len(dbin_fields_no_newline))         ##DEBUG
    row_headings=dbin_fields_no_newline[2:6]
    
    if len(sys.argv)<2:
        py_cells  = dbin_fields_no_newline[6:9];
        rb_cells = dbin_fields_no_newline[10:13]    ## elim blank cols won't speed up much.
        #rb_cells = dbin_fields_no_newline[9:12]
    else:
        rb_cells =["","","",""]
        py_cells  = dbin_fields_no_newline[6:9];
    for (pyrb_zero_orone, py_rb_3cols_data) in enumerate((py_cells, rb_cells) ):
        
        ## ignore 4th col.
        #if re_allwhitespace.match(py_rb_3cols_data[0]) and re_allwhitespace.match(py_rb_3cols_data[1]) and re_allwhitespace.match(py_rb_3cols_data[2]):
        tot=0
        for p in py_rb_3cols_data:         ## ( block to knock out blank db entries) FIXME: ",/n~~~~,/n~~~~,/n~~~~,"
            no_newline=p.replace('\\n',"")          ## edited 3/18/07 to reflect escaped "\\n"
            if re_allwhitespace_commas.match(no_newline):
                tot+=1
        if tot ==3:        
            continue
        ### 3/10/07: add "lft==thisrow", "rgt"
        try:            ## ult, immed, thisrow are strings
            if ""==immed or "\\N"==immed or thisrow==ult or 0==int(immed) :
                immed="\\N"          ## 3/18/07: ESCAPE NULL for MySQL
            fiverows_str_array=    (ult,immed, thisrow, thisrow, repr(array_rgt_values[indx]))
            if len(sys.argv)<2:
                if pyrb_zero_orone==1:
                    fiverows_str_array=[add100k(item,200000) for item in fiverows_str_array]
            else:
                fiverows_str_array=[add100k(item,400000) for item in fiverows_str_array]
            line_towriteout=FIELD_TERMINATED_BY.join(fiverows_str_array ) +FIELD_TERMINATED_BY
        except ValueError:
            pass
        except IndexError:
            print "l. 106, IndxErr:: row # in pyrbhead2.txtout.txt: "+ repr(indx)
            print "indx: "+str(indx  )
            print "length array_rgt_values"+str(len(array_rgt_values))
        line_towriteout+=FIELD_TERMINATED_BY.join(row_headings)+FIELD_TERMINATED_BY
        #line_towriteout+=FIELD_TERMINATED_BY.join((ult,immed, thisrow) ) +FIELD_TERMINATED_BY
        line_towriteout+=FIELD_TERMINATED_BY.join(py_rb_3cols_data[0:3])+FIELD_TERMINATED_BY
        line_towriteout=re_5tilde.sub( "~~~~,",line_towriteout)           ## doesn't do anything
        line_towriteout+=FIELD_TERMINATED_BY.join(array_concatted_headgs[indx])+FIELD_TERMINATED_BY
        if len(sys.argv)<2:
            if pyrb_zero_orone==0:
                out_dbin_py.write("0~~~~,"+line_towriteout+"\n")
            else: out_dbin_rb.write("1~~~~,"+line_towriteout+"\n")
        else: out_dbin_py.write("2~~~~,"+line_towriteout+"\n")      ## dbin_rails2.txt
        ## ## ##    add 0/1, FIELD_TERMINATED_BY.join(py or rb 3 cols. data)    ## ## ##  write out to rb, py if NON-BLANK    
        
    i+=1        ## End of    "for indx,oneline" 
print "no immed: "+repr(numrows_noimmedpar)
