import os,sys
import json
import time
import subprocess
from subprocess import Popen,PIPE,STDOUT,call

def download(files, authData, currentDirName, course_Name):
  print files

  #Store the parameters to variables
  username = authData[0]
  password = authData[1]

  try:
    os.mkdir("Files\\" + course_Name + "\\" + currentDirName)
  except:
    pass

  #Get individual files
  for i, entry in enumerate(files):
    #print entry


    if "File" in entry:
      #Create a database of files already downloaded
      currentEntry = {}


      #with open('LMS_History.lms', 'w') as outfile:
      #  json.dump(data, outfile)


      #Check the filesize to ensure we don't download huge files
      cmd = ("wget.exe --spider --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" +
        entry["File"]["URL"] + " -P " + "\"" + "Files" + "\\" + course_Name + "\\" + currentDirName)

      #Get the filesize data from stderr
      command = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
      out, err = command.communicate()
      print err
      startLengthIndex = err.find("Length:")
      endLengthIndex = err.find(" ", startLengthIndex + 8)
      fileSize = err[startLengthIndex+8:endLengthIndex]
      print fileSize
      fileSize = int(fileSize)

      print "File Size: " + str(fileSize)

      #Skip file if greater than 5MB
      #JUST FOR DEBUG
      if fileSize > 500000:
        print "---------------------------SKIPPING FILE: GREATER THAN  5MB--------------------------"
        time.sleep(5)
        continue







      #wget Commands Used
      #  --content-disposition => names the file with the name specified in the response header without any redirecting required
      #  -nc => skip downloads that would download to existing files.
      #  --user => Username
      #  --password => Password
      os.system("wget.exe --content-disposition -nc --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" +
        entry["File"]["URL"] + " -P " + "\"" + "Files" + "\\" + course_Name + "\\" + currentDirName)

