## BEFORE RUN prog: edit beg line num in .XLS, line 27 this file
import re, sys
import os             

# BUFLINES=35
HEADCOLS=4

# reg ex's for removing spurious " from CSV delimiters
from regexes import lead2quote,leaddelim
from regexes import trail2quote,traildelim, allblank, delim_re
re_onetilde=re.compile(r'\"\~\"'); 			re_twotildes=re.compile(r'\"\~\~\"')
re_trailingtildes=re.compile(r'\~+\"');		re_leadingtildes=re.compile(r'\",\~+');

#  allblank=re.compile(r'^\s*$')

if len(sys.argv)<2:
	infile = open('csvtest12cols.csv','r')
	outfile = open('pyrbhead.txt','w')		## 4 cells of headers dup'd for each row of info cell
	REAL_1ST_LINE_NUM=4	## 0-based count!  EDIT as # delic users grows ("Lang COmparison")
elif "r"==sys.argv[1][0].lower():			#arg is "rails"
	infile = open('railscsvtest8cols.csv','r')
	outfile = open('railshead.txt','w')		## 4 cells of headers dup'd for each row of info cell
	REAL_1ST_LINE_NUM=100004	## EDIT as # delic users grows ("Overview/archit")
								## XLS row 93 has "Lang Comparisons"
	#REAL_1ST_LINE_NUM=92		## 2/28/07: adding 100k: IndxErr in flatfile4a.py
# data struct to hold line#, 4 cumul.row headings
import rowheadgs
lineNO=0					## DON'T edit for start row in perlPYrb.XLS  (0 or 68)

# setup, clean up delimiters and split line
for line in infile:
	lineNO+=1

	# some cells have " appended outside |^ delimiters (?) so s/,"|^/,|^/ and s/|^",/|^,/
	# test: even number of gsub! 
	if (len(lead2quote.findall(line)) != len(trail2quote.findall(line)) ):
		print "l. 36: CSV has unbalanced double quotes, line # %i" % lineNO		##DEBUG
		print "len(lead2quote.findall(line)): "+str(len(lead2quote.findall(line)))
		print "len(trail2quote.findall(line)): "+str(len(trail2quote.findall(line)))
		sys.exit()												##KILL PRogram if throw excep
	line=lead2quote.sub(r',~~~',line)
	line=trail2quote.sub(r'~~~,',line)

	# remove lead/trail |^, split, check # cells\
	line=leaddelim.sub(r'',line)
	line=traildelim.sub(r'',line)
	line_exploded=delim_re.split(line,15)		# FIX: pyrb: trail'g "~";; rails: no trail'g
	
# Line # in CSV file is 1-indexed, 
	colNO=0
	while(colNO<HEADCOLS):
		try: 
			if not allblank.match(line_exploded[colNO]):
				if 255<len(line_exploded[colNO]):
					print "!!!! col headg too long: " +line_exploded[colNO]
					print "row num in XLS: "+ repr(lineNO+ REAL_1ST_LINE_NUM)
				if colNO==0:
					rowheadgs.initheadgs()				## rowheadgs=[0,"","","",""]
				rowheadgs.rowheadgs[0] = lineNO+ REAL_1ST_LINE_NUM
				rowheadgs.rowheadgs[1+colNO] = line_exploded[colNO]
							# fix case: same-col head'g split over 2 vert cells
				subseqcolNO=colNO+1
				while subseqcolNO<HEADCOLS:
					rowheadgs.rowheadgs[1+subseqcolNO]=""
					subseqcolNO+=1
		except IndexError:
			print "index error, line %i (colNO %i)" % (lineNO, colNO)
			print "length of line_exp'd %i"% len (line_exploded)
			print "line_exp'd: %s"% line_exploded
				# S.B. NOT allblank...		if (colNO==3 and reduce(or,map(allblank.match,line_exploded[:4] ) ) ):
				# SO: dedup the outfile in rm_duplines2.rb  !
				# OR: def func to determine if all items in list blank
#		if (colNO==3 and reduce(or,[not(allblank.match(item) ) for item in line_exploded[:4] ] ) ):
		if (colNO==3):					## 12/11/06 get rid of "~" and "~~" tildes
										## 12/11/06 FIXME: get rid of trail, leading "~"
			formatted_output_string='%i,\"%s\",\"%s\",\"%s\",\"%s\"\n' % tuple(rowheadgs.rowheadgs)
			#print "formatted_output_string: "+formatted_output_string
			#formatted_output_string=formatted_output_string.replace('\"\~\~\"','\"\"'); 		## string.replace: doesn't work?!
			formatted_output_string=re_onetilde.sub('""',formatted_output_string);
			formatted_output_string=re_twotildes.sub('""',formatted_output_string);
			formatted_output_string=re_trailingtildes.sub('"',formatted_output_string);
			formatted_output_string=re_leadingtildes.sub('"',formatted_output_string);
			outfile.write(formatted_output_string )
		colNO += 1		
# end "for line in infile"
outfile.write('%i,"last line"' % lineNO )

# # # # # # # # # # #############
# Heuristic 1:Start new cell (row head'g combo) if there's any non-blank in cols 1-4
#		EXCEPT: non-b in 1-4 directly below non-b cell above
#		OR: 	all py and rb cols blank
#
