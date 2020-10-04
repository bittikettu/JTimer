# JTimer
A piece of timing sw for competitions such as marathons, cross country mountainbiking, triathlon. Was designed to replace all sorts of Excel/Google Sheets based solutions trying to keep in mind that it should be easy to use.

Idea is to read all the competitors from a csv-file. You can create the file using your favourite tools like excel or whatever.

Everybody starts at the same time and if there is mqtt broker configured all the data is sent to a wanted channel for monitoring.

This SW has been in use for many years and served in multiple competitions with varying amount of competitors.

A lot of the stuff is in Finnish in the code. Sorry about that.

## Developement history
Initial prototype was designed for XCM(Cross Country Mountainbiking) where all the classes leave at the same time. This early prototype had the basic concept but there were no proper GUI. First tested in 5.5.2013.

Later in 2013: Second evolution started by implementing TkInter to the program and "normal" software capabilities such as reading and writing data to diffrent formats. CSV, XLSX etc. This prototype was tested in multiple marathons, mountainbiking, one duathlon and one triathlon. This version is the foundation for this current prototype version.

2014-2016 Working like a charm if user errors were not counted.

Late 2016: MQTT support added for live monitoring and other fun stuff yet to be designed. :D

Late 2018: Removed deprecated functions.

June 2019: Minor readability enhancements.

# Installation
Get ourself a fresh version of Python 3,  
 ```pip install openpyxl```
, ```pip install paho-mqtt```,  that is all.

Open console to install folder and run ```python ajanotto_menu.py```
