import os,sys

def download(files, authData, currentDirName):
  print files

  username = authData[0]
  password = authData[1]

  try:
    os.mkdir("Files\\" + currentDirName)
  except:
    pass

  #Get individual part .sco files
  for i, entry in enumerate(files):
    #print entry


    if "File" in entry:
      #print "wget.exe --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" + entry["File"]["URL"] + " -O " + "Files" + "\\" + entry["File"]["Name"]
      os.system("wget.exe --content-disposition --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" +
        entry["File"]["URL"] + " -P " + "\"" + "Files" + "\\" + currentDirName)

