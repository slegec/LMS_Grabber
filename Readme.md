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


###How to use

Run the program in a CMD window.

The user should be prompted to enter the following information:

* LMS Username and password

* Select which courses to downloaded

* Max file size allowed

* File download location

The program should then run without error until it downloads all files
