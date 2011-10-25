import re, sys
import os             
# EVERY RUN: choose inputfile: rails or rb/py
# BUFLINES=35

if len(sys.argv)<2:
	infile = open('csvtest12cols.csv','r')
	NUMCOLS=12
else: 
	infile=open("railscsvtest8cols.csv", 'r')
	NUMCOLS=7

# reg ex's for removing spurious " from CSV delimiters
from regexes import lead2quote,leaddelim
from regexes import trail2quote,traildelim

delim_re=re.compile(r'~~~,~~~')
delim=r'~~~,~~~'
allblank=re.compile(r'^\s*$')

if len(sys.argv)<1:
	print "Usage: flatfile.py whatever.CSV"
	sys.exit(0)

lineno=0
linesWrongLen=0
unbalDblQte=0
cellTotCols=[0]*NUMCOLS

for line in infile:
	lineno+=1
	# some cells have " appended outside |^ delimiters (?) so s/,"|^/,|^/ and s/|^",/|^,/
	# test: even number of gsub! 
	
	indces_l2q=lead2quote.findall(line)
	indces_t2q=trail2quote.findall(line)
	if (len(indces_l2q) != len(indces_t2q) ):
		unbalDblQte+=1
		if unbalDblQte < 5:
			print
			print line[:38]
			print indces_l2q, "trail'g 2-quote", indces_t2q
			print "CSV has unbalanced double quotes, line # %i" % lineno

	line=lead2quote.sub(r',~~~',line)
	line=trail2quote.sub(r'~~~,',line)

	# remove lead/trail |^, split, check # cells\
	line=leaddelim.sub(r'',line)
	line=traildelim.sub(r'',line)
	line_exploded=delim_re.split(line,15)

	if len(line_exploded)!=NUMCOLS:
		linesWrongLen+=1
		if linesWrongLen <8:
			print "Line %i: # %i w/wrong # cells aft split" % (lineno,linesWrongLen) 
			print "Len(line exploded: %i: " %len(line_exploded)
	# totals for CSV 
	i=0
	try:
		while(i<NUMCOLS):
			if not allblank.match(line_exploded[i]):
				cellTotCols[i]+=1
			i+=1
	except IndexError: 
		print line
	# end "for line in infile"

i=0
## print # cells for row head'gs, py,rb
print "cell counts: row headgs:      ", ['%4i' % x for x in cellTotCols[0:4] ]	# 
print "cell counts: Pyth/RAILS:      ", ["%4i" % x for x in cellTotCols[4:8] ]
print "cell counts: Ruby:            ", ["%4i" % x for x in cellTotCols[8:12] ]
print
print "Unmatched dbl quotes: %i" % unbalDblQte

#################3
# row head'gs, levels 1-4, for HEADINGS table
#











######################
# Heuristic 1:Start new cell if there's any non-blank in cols 1-4
#		EXCEPT: non-b in 1-4 directly below non-b cell above
#		OR: 	all py and rb cols blank
#
