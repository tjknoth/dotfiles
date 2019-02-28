#!/usr/bin/python3

import sys
import os, os.path
import platform
import shutil

# Parameters
SCRIPT_SOURCE_PATH = "./Code/misc/scripts/"
I3_CONFIG_SOURCE_PATH = "./.config/i3/"
I3_CONFIG_FILES = ["config", "i3blocks.conf", "i3status.conf"]

DESTINATION_PATH = "./Code/dotfiles/"
SCRIPT_DESTINATION_PATH = DESTINATION_PATH + "scripts/"

HOME = os.path.expanduser("~")


def copy(filename, srcpath, dstpath):
    msg = "COPYING %s FROM %s TO %s" % (filename, srcpath, dstpath)
    print(msg)
    shutil.copyfile(srcpath + filename, dstpath + filename)

print("Moving to %s" % HOME)

os.chdir(HOME)

# Copy configs
for f in I3_CONFIG_FILES:
    copy(f, I3_CONFIG_SOURCE_PATH, DESTINATION_PATH)

os.chdir(HOME)

# Copy scripts
for f in os.listdir(SCRIPT_SOURCE_PATH):
    copy(f, SCRIPT_SOURCE_PATH, SCRIPT_DESTINATION_PATH)

os.chdir(HOME)

# Copy vimrc
copy(".vimrc", "./", DESTINATION_PATH)
