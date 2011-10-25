# rel 1: read whole CSV into mem,
# rel 1: 1 humongous table 12 fields: 4 fields row headgs, 4 for each:py,rb
# !!!FIXME will only work IF: last line in csv input file (line 25) is blank !!!

# mySQL LOAD DATA round 1: fields sep'd by "{4},"{4}

import re, sys, os, time
from each_cons  import each_cons
import multrplc
from multrplc import mult_rplc
HEADCOLS=4
DEPTH_NOSUMMARY=4				## GETOPT:: edit for each execution
							# reg ex's for removing spurious " from CSV delimiters
from regexes import lead2quote,leaddelim
from regexes import trail2quote,traildelim, front2quote, back2quote, delim_re, delim, allblank
re_tildenewline=re.compile(r'~\n$')
re_trailingtilde=re.compile(r'~$')
re_httpslashslash=re.compile(r'http://')

# lead'g comma ONLY in delim, so adjacent cells that are only \n's SHD NOT overlap,
# i.e. DON'T have to .gsub!() each line 2x, or mess w/lookaheads
newlineonly_re=re.compile(r'(\,\"{4})\s*(\\n){1,}(\"{4})')
				################ filehandles
if len(sys.argv)<2:				
	incsv = open('csvtest12cols.csv','r')			## 9/20/06:: 12 cols. of data ONLY
	inrownums= open('pyrbhead.txtout.txt','r')
	outfile = open('dbin.txt','w')		# fields delimited by 4 dbl-quote,comma,4 dbl-quote; chcklen.
	NUMCOLS=12;
	ROW1OFFSET=4;		## 0-based count i.e. 1 less than row num shown by Excel...EDIT as # delic users grows 
elif "r"==sys.argv[1][0].lower():
	incsv = open('railscsvtest8cols.csv','r')			## actually only 7 cols. data
	inrownums= open('railshead.txtout.txt','r')
	outfile = open('dbin_rails.txt','w')
	NUMCOLS=7;
	ROW1OFFSET=4;		## EDIT as # delic users grows
lineNO=0
	#### newcellrows:: list line #s where new cells begin + 1 rec:last line in CSV
	## 9/20/06:: insert row 0 as initializer (WAS: [])
newcellrows=[]

	####### arrayofrowhead all data in pyrbhead.txtout.txt, minus line #
arrayofrowhead=[]
i=0

for line in inrownums:
	line=line.rstrip()
	onecellrow=line.split(",",2)
	last4cells= onecellrow[2][1:-1].split('","')
	onecellrow=onecellrow[0:2]+last4cells
	# need to remove dbl quotes, chomp \n
	len_onecellrow=len(onecellrow)
	i=0
	while (i<len_onecellrow):
		onecellrow[i]=front2quote.sub('',onecellrow[i])
		onecellrow[i]=back2quote.sub('',onecellrow[i])
		i+=1
	# CHECK: taking 2nd row # from each line pyrbhead.txtout.txt
	#print "onecellrow[1]: "+str(onecellrow[1])		##DEBUG
	try:
		
		newcellrows.append(int(onecellrow[1])-ROW1OFFSET )			## 12/21/06: increment by ROW1OFFSET
	except ValueError:
		continue
	# 12/14/04: change to [0:] to make row # first field in dbin.txt; was: [1:] 
	# enhancement DONE: 1st field will be row# fr. pyrbhead.txtout.txt
	# 1/10/05: 1st 2 fields are both row #s, directly appended>>arrayofrowhead
	arrayofrowhead.append(onecellrow[0:])
	i+=1
inrownums.close
## print " ^^^^^ newcellrows:  ";		print newcellrows[0:20]		##debug

# print "len of arrayofrowhead: %i\t len of line 31: %i"%(len(arrayofrowhead),
	#len(arrayofrowhead[6]) )

########### setup, clean up delimiters and split line
arrayofcells=[];
pyURL_nosummary={}; rbURL_nosummary={}; 		## NOT USED yet
for line in incsv:
	line=line.rstrip()
	lineNO+=1
		# few cells:" appended outside "~~~"delimiters: srch/replc w/trail2quote & lead, SO
		# test: even number of gsub! 
	if (len(lead2quote.findall(line)) != len(trail2quote.findall(line)) ):
		print "CSV has unbalanced double quotes, line # %i" % lineNO
	line=lead2quote.sub(r',~~~',line)
	line=trail2quote.sub(r'~~~,',line)
		# remove lead/trail |^, split, check # cells\
	line = leaddelim.sub(r'',line)
	line = traildelim.sub(r'',line)
## 	these 4 chars become $lt; etc: & < > "
			## check/ test this method
##	line = mult_rplc(multrplc.htmlDICT,line)		## removed for debug, 9/19/06
	line_exploded=delim_re.split(line)		## 3 debug lines
	if len(line_exploded)!=NUMCOLS:
		print "PROB LIne numb: " ; 
		print lineNO
		print
		print "line_exploded: "
		print line_exploded
		print "PROBLEM:: Len(line_exploded_: "; print len(line_exploded)
							### arrayofcells is all data in CSVtest.csv	
	arrayofcells.append(line_exploded)
##	print "len(arrayofcells)"; print len(arrayofcells)
## print "()()()()     arrayofcells"; print arrayofcells		## debug
		############ build cells separated by \n for mysql LOAD IN INFILE

#1st diffs on newcellrows e.g. rb each_cons
firstdiff=[]
for x in each_cons(newcellrows,2):
    firstdiff.append(x[1]-x[0])
if (len(firstdiff)!= -1+len(newcellrows) ):
	print "Oh, oh, somethin wrong: remove_dups or each_cons"
	sys.exit(1)
## print firstdiff[20:40]						## debug

# start_depth: list of lists: [start row from "newcellrows", # rows from "firstdiff"]
start_depth=zip(newcellrows, firstdiff)
print "  start_depth:: "; print start_depth[0:25]			##debug
i=0
tot_indexerrors=0

for (startrow, depth) in start_depth:
	if 2==len(sys.argv):
		startrow=startrow-100000
	onerecord=[]
	onerecord.extend(arrayofrowhead[i])		# row head'gs
#	print "/\/\/\/\ len(onerecord) ::"; 		print len(onerecord)		##debug
				#   NICE TODO: if array of cells is all blank, go next rec in pyrbhead.txtout.txt
	try:						## 2/28/07: ugly 100k kludge
		onerecord.extend(arrayofcells[startrow-1][4:] )	# 1st row usage note cells
	except IndexError:
		print "Startrow, depth of IndErr:: "
		print [startrow, depth]
		
#	print "####1st row of cell entries aft onerec.extend"; print onerecord		##debug
#	print "******len(onerecord) ::"; 		print len(onerecord)		##debug
	appendrow=startrow
	while appendrow < startrow + depth-1:
		pyrbcol=0;					count_http_url=0;
		while pyrbcol<NUMCOLS-4:
#			if 				## 21/8/06: chng <br/> to "\n"  MUST BE LOWERCASE
			onerecord[pyrbcol+6]=re_trailingtilde.sub('',onerecord[pyrbcol+6])
			if re_httpslashslash.match(onerecord[pyrbcol+6]):
				count_http_url+=1
			
			##onerecord[pyrbcol+6]+='\\\\n'		#  TODO: skip 4 cols. of row head'gs		##3/18/07: escape "\n" as "\\n"
			onerecord[pyrbcol+6]+='<br/>'		# 7/12/08
			# onerecord[pyrbcol+6]=re_tildenewline.sub('\n',onerecord[pyrbcol+6])
			try:
				onerecord[pyrbcol+6]+=arrayofcells[appendrow] [pyrbcol+4]
			except IndexError:
				tot_indexerrors+=1
				#print "flatfile1.py and 2, rm_duplines.rb, flatfile4a.py\n"
				#print "pyrbcol is:\n";				#print pyrbcol
				print "   IndErr:: appendrow is: "; 		print appendrow
				#print "      lastly, arrayofcells is: \n"; 	print arrayofcells[appendrow]
				if tot_indexerrors>3:
					sys.exit(1)
				continue
			#if ((pyrbcol==NUMCOLS-5) and (appendrow == startrow + depth-2)):
			#	onerecord.append(repr(len(re.findall(re_httpslashslash, onerecord[-1]))))
			pyrbcol+=1
		appendrow+=1	

##	'\n instead <br /> ???
##	TODO escape these 6 chars for mySQL :' " \n \r NULL SUB (WTF is sub?)
##	TODO :may have to truncate cells to 255
##	NICE TODO: compress out any lines that are /^\w+$/

		# join() to write out varchars for mySQL
##	new fld separator, 1/10/05
	onerecord="~~~~,".join(onerecord)
	onerecord= onerecord+"~~~~,"			## 
##	11/1 9pm: leading "~~~~,~~~~" attempts to not fill in auto_increm key fld
###	mysql LOAD DATA INFILE: field TERMINATORS, not separators, NO beg. or end-of-record	
		#### knock out cells that are blank except for "\n"
	onerecord=newlineonly_re.sub(r'\1\3',onerecord)
		### DON'T HAVE TO APPLY 2X ANYMORE: cause only lead'g "," in re
#	onerecord=newlineonly_re.sub(r'\1\3',onerecord)	
	outfile.write("%s\n"% onerecord)
	i+=1
