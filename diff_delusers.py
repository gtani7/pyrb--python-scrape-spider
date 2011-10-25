#!/usr/bin/env python
import re
in_rowheadgs_file = open('delic_pyrbrails_diff.txt','w')
py_users=''' '''
rb_users=''' '''
rails_users=''' '''

def users2vecofusers(string_embedded_newline):
    returnvalue_vec=[]
    tempstr=string_embedded_newline.split("\n")
    for str in tempstr:
        oneline=str.split(', ')
        split_1stelem=oneline[0].split()
        if 0==len(split_1stelem):
            continue
        oneline[0]=split_1stelem[1]
        returnvalue_vec.extend(oneline)
    return returnvalue_vec

py_users_vec=users2vecofusers(py_users)
rb_users_vec=users2vecofusers(rb_users)
rails_users_vec=users2vecofusers(rails_users)
print "Length of py user vec: "+repr(len(py_users_vec))
print "Length of rb user vec: "+repr(len(rb_users_vec))
print "Length rails user vec: "+repr(len(rails_users_vec))

print "ruby users, NOT in rails users: "
for railsuser in rails_users_vec:
    if not(railsuser in rb_users_vec):
        print railsuser
