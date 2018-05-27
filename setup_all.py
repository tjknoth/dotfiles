#!/usr/bin/python3

import sys
import os, os.path
import platform
import shutil 

SCRIPT_SOURCE_PATH = "./scripts"
I3_SOURCE_PATH = "./"
I3_CONFIG_FILES = ["config", "i3blocks.conf", "i3status.conf"]

# Set destinations before using script
SCRIPT_DST = ""
CONFIG_DST = ""

HOME = os.path.expanduser("~")

def cmdline():
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument("--configs", action="store", help="Config file path")
    a.add_argument("--scripts", action="store", help="Script path")
    return a.parse_args()

def copy(filename, srcpath, dstpath):
    msg = "COPYING %s FROM %s TO %s" % (filename, srcpath, dstpath)
    print(msg)
    shutil.copyfile(srcpath + filename, dstpath + filename)

a = cmdline()

if a.configs:
    CONFIG_DST = a.configs

if a.scripts:
    SCRIPT_DST = a.scripts

# Check destinations are defined
if (SCRIPT_DST == "" or CONFIG_DST == ""):
    raise Exception("Set script and config file destinations.")

# Copy configs
for f in I3_CONFIG_FILES:
    copy(f, I3_SOURCE_PATH, CONFIG_DST)

# Copy scripts
for f in os.listdir(SCRIPT_SOURCE_PATH):
    copy(f, SCRIPT_SOURCE_PATH, SCRIPT_DST)

# Copy vimrc
copy(".vimrc",I3_SOURCE_PATH,HOME)
