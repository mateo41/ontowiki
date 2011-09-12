import sys
import re
sys.path.append("../pywikipedia")
sys.path.append("../pywikipedia/families")
import wikipedia, login

def put_callback(page, ex):
    print "in callback"
    print page
    print ex

ow = wikipedia.Site('en', 'ooi')
login.LoginManager('R0b0W1k1', sysop=False, site=ow) 
f = open("wikipages_fixed.txt")
for line in f:
    page,pagetext = line.strip().split("@") 
    wikipage = wikipedia.Page(ow, page)
    wikipage.put_async(pagetext, callback=put_callback)
    #print "generating page: ",pagetext

wikipedia.stopme()

