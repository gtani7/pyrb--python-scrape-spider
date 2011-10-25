#!/usr/bin/env python
import sys

class Mag_BSoup(object):
    urlsExtracted=[]
    allh3tags=[];
    
#    import re
#    url_re=re.compile(r'<a href="(.*)" onmousedown=')
    def __init__(self,mag_file):     # mag_file is string, not file obj
        from BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(mag_file)
        self.__class__.allh3tags=soup('h3')        # shd be 13, 1st 10 are bookmark tags, last 3 are spurious
        self.__class__.allh3tags=self.__class__.allh3tags[0:10]

    def selecth3tag(self):
        for thish3tag in self.__class__.allh3tags:
#            urlextracted=self.__class__.url_re.match(string(h3tag) )   #TypeErr: tag is not str, can't be fed to regex
             print thish3tag.aTag['href']
             self.__class__.urlsExtracted.append(thish3tag.aTag.href)
#######    Reddit  ###########
class Red_BSoup(object):
    allcolspan3=[]
    urlsExtracted=[]
    
    def __init__(self,red_file):
        from BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(red_file)
        self.__class__.allcolspan3=soup.findAll(name='td',attrs={colspan:"3"})  
        
def build_dict(filename):
    ''' it's just too annoying trying to get Python SYCK or other YAML parsers to work'''
    import re
    blank_line=r'--- '      ## shd only be 1st line
    blankline_re=re.compile(blank_line)
    dict2return={}
    for inp_line in open(filename, "r"):
        if blankline_re.match(inp_line): continue
        (url, numoccur)=inp_line.split(r': ')
        dict2return[url]=int(numoccur)
    return dict2return
                
if __name__ == "__main__":
    import os,fileinput, glob
    [pyurls,rburls,railsurls]=map(build_dict, ["pyurls.yml","rburls.yml","railsurls.yml"])
    sys.stdout.write("Len of py, rb URLs dicts: " +repr(len(pyurls.keys()))+", "+repr(len(rburls.keys()))+"\n")
    sys.stdout.write("Len of rails urls dict: " +repr(len(railsurls.keys()))+"\n")
#    pyurls=pyurls.keys();       rburls=rburls.keys();       railsurls=railsurls.keys();
    allurls=pyurls.keys() + rburls.keys() + railsurls.keys()
                                                        ## EDIT "cwd" as neces
#    os.chdir("C:\\kacc\\pyrb\\magnol_pages")                    
    os.chdir("C:\\kacc\\pyrb\\reddit_pages")
    for magfilename in glob.glob("rub*.htm*"):      ## EDIT filename glob as neces
        magfilehand=open(magfilename)
        ent_magfile=magfilehand.read()        
        magfileparsed=Mag_BSoup(ent_magfile)
        magfileparsed.selecth3tag()
        
        
        
        
