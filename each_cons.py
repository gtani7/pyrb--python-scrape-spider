#!/usr/bin/env python
# each_cons.py, like ruby Array#each_cons (moving win), each_slice
# (sublists returned are disjoint sets)

def each_cons(listin,n):        # moving window
                #known defect: if n>len(listin)
                #not tested: sequences other than lists
    i=0
    while (i<len(listin)-n+1 ):
        yield listin[i:i+n]
        i+=1
        
def each_slice(listin,n):       # non-overlapp'g slices, ret iterator fr yield
    i=0;        len_listin=len(listin)
    while (i<len_listin ):
        yield listin[i:min(len_listin,i+n)]
        i+=n
        
def each_cons2(listin,n):        # moving window, ret list of lists
    return [listin[i:i+n] for i in range(len(listin)-n+1)]
     
def each_slice2(listin,n):        # non-overlapp'g slices,, ret list of lists
    len_listin=len(listin)
    return [listin[i:min(len_listin, i+n)] for i in range(0,len_listin,n)]

if __name__=="__main__":
    testlist=[1,3,"wha",4.9,"ok","3.14",3.14,[3,3]]
    print "each_cons(testlist,5): \n"
    for x in each_cons(testlist,5):
        print x
    print "\neach_slice(testlist,5): \n"
    for x in each_slice(testlist,5):
        print x

    print "\neach_cons2(testlist,5): \n"
    print each_cons2(testlist,5)

    print "\neach_slice2(testlist,5): \n"
    print each_slice2(testlist,5)