import os,sys

def download(files, authData):
  print files

  username = authData[0]
  password = authData[1]

  currentDirName = ""


  #Get individual part .sco files
  for i, entry in enumerate(files):
    #print entry

    if "Dir" in entry:
      currentDirName = entry["Dir"]["Name"]
      try:
        os.mkdir("Files\\" + currentDirName)
      except:
        os.mkdir("Files\\" + currentDirName + "1")


    if "File" in entry:
      #print "wget.exe --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" + entry["File"]["URL"] + " -O " + "Files" + "\\" + entry["File"]["Name"]
      os.system("wget.exe --user " + username + " --password " + password + " https://lms9.rpi.edu:8443" +
        entry["File"]["URL"] + " -O " + "\"" + "Files" + "\\" + currentDirName + "\\" + entry["File"]["Name"] + "\"")

