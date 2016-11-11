import os,sys
import json

def download(files, authData, currentDirName, course_Name):
  print files

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





      #wget Commands Used
      #  --content-disposition => names the file with the name specified in the response header without any redirecting required
      #  -nc => skip downloads that would download to existing files.
      #  --user => Username
      #  --password => Password
      os.system("wget.exe --content-disposition -nc --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" +
        entry["File"]["URL"] + " -P " + "\"" + "Files" + "\\" + course_Name + "\\" + currentDirName)

