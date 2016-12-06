#LMS Grabber


##Goal

To be able to download files from a users LMS (Blackboard) account to their local computers.
This program is written to interface directly with the Rensselaer Polytechnic Institute  (RPI)
interface.


This application is written in Python 2.x.  It uses the Selenieum webbrowser module
in order to parse through the LMS webpages.




##Usage

###Required Python Libraries

* selenium


###Other required tools

* wget

* Firefox web browser (Can be ported for other browsers)



###Other notes

* Only been tested on Windows 7 64bit

* At the time of writing this, Selenium has been problematic on verisons greater that 47.x.x



###How to use


Edit the 'PW.txt' file to include your LMS Username and Password, for easy login

Run the program in a CMD window.

The user should be prompted to enter the following information:

* LMS Username and password

* Select which courses to downloaded

* Max file size allowed

* File download location

The program should then run without error until it downloads all files


###Issues

* The program only goes one directory deep in an LMS course.  Potentially this could be problematic
    depending on how the course is set up.
