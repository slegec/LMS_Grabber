import selenium
import time
import getpass
#from bs4 import BeautifulSoup
import os, sys

import signal

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#Repairs some problems in how the source code is pulled from the webpage
#  Known Problems, but ar fixed:
#  - &amp; => &
def htmlRepair(myStr):
  #Fixes '&'
  myStr = myStr.replace("&amp;", "&")
  return myStr



#Parses the mobile site version of LMS to access all of the courses and get their id's
#  so we can look at the actual URL's on the main LMS site
def getCourseInfo(src):

  #Stores a list of dictionaries...each dictionary contains a course and id
  listOfCourses = []

  #Stores course name and id
  courseDict = {}

  #CurrentIndex in the string
  currentIdx = 0

  #bbid_Offset = number of chars in < bbid=" >
  bbid_Offset = 6

  #Loop through XML file to find the id and course name
  while True:

    #Find the LMS course number
    currentIdx = src.find("bbid", currentIdx+1)

    #Found all courses so leave
    if currentIdx == -1:
      break

    #Iterate over the string to find the end of the id
    for i in range(0,100):
      endPos = currentIdx + bbid_Offset + i

      #Check if we found the end of the id
      if src[endPos]  == "\"":
        courseDict["bbid"] = src[currentIdx + bbid_Offset:endPos]
        break



    #Find the LMS Course Name
    currentIdx = src.find("name=\"", currentIdx+1)


    #Iterate over the string to find the end of the course name
    for i in range(0,1000):
      endPos = currentIdx + bbid_Offset + i

      #Check if we found the end of the name
      if src[endPos]  == "\"":
        courseDict["name"] = src[currentIdx + bbid_Offset:endPos]
        break

    #Append courseDict to listOfCourses, and reset for the next course
    listOfCourses.append(courseDict)
    courseDict = {}

  print listOfCourses

  return listOfCourses




#Grab the files that we can download
#  Files: pdf, doc, etc.
#  Dirs: Links to other pages on LMS
def findFilesAndDirs(src):

  #
  href_Offset = 7

  #This list contains:
  #  dict_Dir:
  #  dict_File:
  listOfFilesAndDirs = []


  #dict_Dir - A Single Dir
  # { Dir :
  #   { Name : "",
  #     URL  : ""
  #   }
  # }
  dict_Dir = {}

  #dict_File - A Single File
  # { File :
  #   { Name : "",
  #     URL  : ""
  #   }
  # }
  dict_File = {}


  #Loop through HTML file to find the hrefs
  for idx, line in enumerate(src):

    #Flag used to make sure the href is a file or dir
    isFile = False
    isDir = False


    #Find the links for files or dirs
    # Note the space is required, or else it will pick up this.ref
    currentIdx = line.find(" href=")


    if currentIdx == -1:
      continue

    #Cycle through string to find the last character needed
    for i in range(0,1000):
      endPos = currentIdx + href_Offset + i

      if line[endPos]  == "\"":
        tmpStr = line[currentIdx + href_Offset:endPos]

        #Check if this is a file
        if "/xid" in tmpStr:
          isFile = True
          print tmpStr

          #Create a new entry for a file - add the URL
          dict_File["URL"] = tmpStr
          break

        #Check if this is a dir
        elif "content_id=" in tmpStr:
          isDir = True

          #Call this function to fix any problems that may appear when the source code is
          #  pulled form the website
          tmpStr = htmlRepair(tmpStr)

          print tmpStr


          #Create a new entry for a dir - add the URL
          dict_Dir["URL"] = tmpStr
          break

        else:
          break

    #We did not find a downloadable file on this line, so we can leave this for loop now
    #if isFile == False:
    #  continue






    #GET FILENAME
    #If we got to here, the file must have been successfully found, so let's get the name of the file

    currentIdx = line.find("</span></a>")


    #Let's count backwards to get the beginning of the file name
    for i in range(0,1000):
      startPos = currentIdx - i

      if line[startPos:startPos+2]  == "\">":
        tmpStr = line[startPos+2:currentIdx]

        #Check if it is a file
        if isFile == True:
          print tmpStr

          #Add to the file entry - Filename
          dict_File["Name"] = tmpStr

        #Check if it is a file
        elif isDir == True:
          print tmpStr

          #Add to the file entry - Filename
          dict_Dir["Name"] = tmpStr

        break


    #Add the file/dir dictionary to the list and reset for the next loop
    tmpDict = {}
    if isFile == True:
      tmpDict["File"] = dict_File
      listOfFilesAndDirs.append(tmpDict)
      dict_File = {}

    elif isDir == True:
      tmpDict["Dir"] = dict_Dir
      listOfFilesAndDirs.append(tmpDict)
      dict_Dir = {}


    #Reset isDir and isFile back to False
    isDir = False
    isFile = False

  print listOfFilesAndDirs

  return listOfFilesAndDirs



def main():

  preURL = "https://lms9.rpi.edu:8443"

  browser = webdriver.Firefox()
  #browser = webdriver.PhantomJS()
  browser.get('https://lms9.rpi.edu:8443/')


  username = browser.find_element_by_id("user_id")
  password = browser.find_element_by_id("password")

  inputUsername = raw_input("Username: ")
  inputPassword = getpass.getpass("Password: ")

  username.send_keys(inputUsername)
  password.send_keys(inputPassword)

  browser.find_element_by_id("entry-login").click()


  all_cookies = browser.get_cookies()

  time.sleep(2)

  browser.get("https://lms9.rpi.edu:8443/webapps/Bb-mobile-BBLEARN/enrollments?course_type=COURSE")
  courseInfo_src = browser.page_source.encode('ascii', 'ignore')
  #soup = BeautifulSoup(source, "html.parser")
  #print soup
  print courseInfo_src

  courseInfoList = getCourseInfo(courseInfo_src)

  #IED
  testCourse = courseInfoList[2]['bbid']


  browser.get("https://lms9.rpi.edu:8443/webapps/blackboard/content/listContent.jsp?course_id=" + testCourse)

  coursePage = browser.page_source.encode('ascii', 'ignore')
  coursePage = coursePage.splitlines()
  #print coursePage


  listOfFilesAndDirs = findFilesAndDirs(coursePage)


  for entry in listOfFilesAndDirs:

    if 'Dir' in entry:
      URLpath = (entry.get('Dir')).get('URL')
      print URLpath
      browser.get(preURL + URLpath)
      coursePage = browser.page_source.encode('ascii', 'ignore')
      coursePage = coursePage.splitlines()

      temp = findFilesAndDirs(coursePage)




  #browser.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
  browser.quit()                                      # quit the node proc



if __name__ == "__main__":
    main()
