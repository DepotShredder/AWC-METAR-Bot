#! /usr/bin/env python3

# Input desired time for email here
# Time zone should be time zone of system on which this code is being run
sendHr = 21
sendMin = 22

# Imports modules
import os
from shutil import move

# Change this variable to the desired folder name
pathName = "METARbot_Github"

# This portion of the code makes sure the directories are set up correctly
if os.path.isdir("../" + pathName) == False:
    if os.path.isdir("./" + pathName) == False:
        os.makedirs("./" + pathName)
        os.makedirs("./" + pathName + "/BotLogs")
    if os.path.isdir("./" + pathName + "/BotLogs") == False:
        os.makedirs("./" + pathName + "/BotLogs")
    if os.path.exists("./METARbot_Github.py"):
        move("./METARbot_Github.py", "./" + pathName)
    if os.path.exists("./emailList_example.txt"):
        move("./emailList_example.txt", "./" + pathName)
    move("./METARbot_setup_Github.py", "./" + pathName)

