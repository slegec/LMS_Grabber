import os,sys
import json
import time
import subprocess
from subprocess import Popen,PIPE,STDOUT,call


#Method to check out the file size
def checkFileSize(username, password, entry, currentDirName, course_Name, maxFileSize):

  #Check the filesize to ensure we don't download huge files
  cmd = ("wget.exe --spider --max-redirect 2 --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" +
    entry["File"]["URL"] + " -P " + "\"" + "Files" + "\\" + course_Name + "\\" + currentDirName)


  #Return true because there is no limit on filesize
  if maxFileSize == -1:
    return True



  #Get the filesize data from stderr
  command = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
  out, err = command.communicate()
  #print "-----"
  #print err
  startLengthIndex = err.find("Length:")
  endLengthIndex = err.find(" ", startLengthIndex + 8)
  fileSize = err[startLengthIndex+8:endLengthIndex]

  fileSize = int(fileSize)

  #Do conversion on file size just for user ease
  prettyPrintSize = ""
  if fileSize >= 1000000:
    prettyPrintSize = str(fileSize/(1024*1024)) + "MB"
  elif fileSize < 1000000:
    prettyPrintSize = str(fileSize/1024) + "KB"



  #Skip file if greater than 5MB
  #JUST FOR DEBUG
  if fileSize > maxFileSize:
    print "---------------------------SKIPPING FILE: GREATER THAN " + prettyPrintSize + " --------------------------"
    print "File Size: " + str(fileSize)
    print entry["File"]["URL"]
    time.sleep(5)
    return False
    #continue

  return True


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


      #Check the size of the file that we are downloading
      # Depending on the max size allowed, if any, this will determine if we
      # need to download it or not.
      maxFileSize = 500000

      if (checkFileSize(username, password, entry, currentDirName, course_Name, maxFileSize) == False):
        continue









      #wget Commands Used
      #  --content-disposition => names the file with the name specified in the response header without any redirecting required
      #  -nc => skip downloads that would download to existing files.
      #  --user => Username
      #  --password => Password
      os.system("wget.exe --content-disposition -nc --max-redirect 2 --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" +
        entry["File"]["URL"] + " -P " + "\"" + "Files" + "\\" + course_Name + "\\" + currentDirName)

