#!/usr/bin/env python

class Swik_BSoup(object):
    
    def __init__(self,swik_file):
        from BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(swik_file)
        self.__class__.all_script=soup.findAll(name='script')
        print "Num of scripts found (not neces. javascript: \n"
        print 
        print "%i"%self.__class__.len(all_script)
        
if __name__ == "__main__":
    import os,fileinput, glob
    os.chdir("C:\\kacc\\pyrb\\swik_pages")
    for swikfilename in glob.glob("rub*.htm*"):      ## EDIT filename glob as neces
        swikfilehand=open(swikfilename)
        ent_swikfile=swikfilehand.read()        
        swikfileparsed=Swik_BSoup(ent_swikfile)
