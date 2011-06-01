from lxml import etree
import urllib
import subprocess
import pickle
import sys
import time
import optparse
import sys
import os
import myurl

url=''
os.chdir(sys.path[0])

#This is the function which will do all the processing of the feed xml file 
def notifier(fbfeedurl):
#first of all i fetched the data and stored it into a local file named "rssfile.xml" in oder to do the parsing.This file will be removed from harddisk when this function quits 
 if fbfeedurl!="":
     try:
      f=urllib.urlopen(fbfeedurl)
     except:
      subprocess.call("notify-send 'Network Error' 'Check your internet connection'",shell=True)
 else:
     subprocess.call("notify-send 'No Facebook Feed URL' 'Please enter your feed url first'",shell=True)

 rssfile=open("rssfile.xml","w")
 for each in f:
     rssfile.write(each)
 rssfile.close()
 notes=[]
 tree=etree.parse('rssfile.xml')
 root=tree.getroot()
 #print(root)
 channel=tree.find("channel")
 print(channel[0].text)
 print("-----------------------------------------------------------------------------------------------------------------------------------------")
 notifications=channel.findall('item')
 for each in notifications:
     title=each.find('title')
     #print(title.text)
     notes.append(title.text)
#We now load the saved old notifications data and put new notification data into the pickle file
 try:
     with open("note.pickle","rb") as myresdata:
         notesold=pickle.load(myresdata)
 except IOError as err:
     print("File Error: "+str(err))
 finally:
     subprocess.call("rm note.pickle",shell=True)
     with open("note.pickle","wb") as mysaveddata:
         pickle.dump(notes,mysaveddata)
#This is the main body which will check whether there is new notification for you or not.
#Here we are making the comparision between previously pickled data and newly pickled data in order to know the difference
 try:
  if notes[0]!=notesold[0]:
      print("You have new notification:"+str(notes[0]))
      workstring='notify-send "Facebook" "'+str(notes[0])+'"'
      subprocess.call(workstring,shell=True)
  else:
      print("No new notifications")
 except UnboundLocalError:
     print("Running for the first time")
     workstring='notify-send "Facebook" "'+str(notes[0])+'"'
     subprocess.call(workstring,shell=True)
 subprocess.call("rm ./rssfile.xml",shell=True)
if __name__=="__main__":
    parser=optparse.OptionParser(usage='Usage: %prog <options>')
    parser.add_option('-u','--url',dest='url',help='enter new fb feed url')
    parser.add_option('-v','--vella',help='this is faltu option')
    (opts,args)=parser.parse_args()
    if opts.url is not None:
        with open("myurl.py","w") as myurlf:
            writestring='url="'+opts.url+'"'
            for each in writestring:
                myurlf.write(each)
    else:
        while(True):
         notifier(myurl.url)
         time.sleep(10)

