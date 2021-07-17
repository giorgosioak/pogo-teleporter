#!/usr/bin/python
# coding=utf-8
'''
Python 3 - Teleport to coords
Developed by George Ioakeimidis <giorgosioak95@gmail.com>
'''
import os
import platform
import re
import sys
from math import sin, cos, sqrt, atan2, radians
from time import time

COORD_PATTERN = r"-?(\d{1,3})\.(\d{1,15})[ ]?,[ ]?-?(\d{1,3})\.(\d{1,15})"
pc = [0.0 , 0.0] # previous coords
lc = [0.0 , 0.0] # latest coords
# TODO: tp_time = time() # time since last teleport

def get_distance(lat1, lon1, lat2, lon2):
    """Return distance of two coordinates."""
    R = 6373.0 # approximate radius of earth in km

    if 200.0 in {lat1, lon1, lat2, lon2}:
        return 0 # 200 is default for non-set

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance # km

def get_cooldown(dist):
    """Return cooldown time of given distance."""
    km = [0,1,2,4,10,12,15,20,25,30,40,45,60,80,100,125,140,180,200,250,300,350,400,500,600,750,800,900,950,1000,1150,1200,1250,1266]
    cd = ["0s","1m","2m","8m","9m","11m","13m","15m","18m","22m","23m","25m","27m","30m","33m","34m","36m","39m","42m","46m","50m","53m","56m","64m","72m", "82m", "86m", "93m", "97m", "100m", "111m", "115m", "118m", "120m"]
    
    if dist > km[-1]:
        return "120m", "120m"
    for i,v in enumerate(km):
        # passed distance
        if v > dist:
            # return cd, safe times
            return cd[i-1], cd[i]

def yellowprint(text):
    """Print in yellow"""
    print( + text + '\033[0m')

def main(argv):
    """Main fuction."""

    global pc # previous coords
    global lc # latest coords
    # TODO: global tp_time # time since last teleport

    # print description message at start
    print("\033[94m~=~=~ ~=~=~ ~=~=~ ~=~=~ ~=~=~ ~=~=~ ~=~=~ ~=~=~\033[0m")
    print(" Pokemon Go Teleporter by \033[96m@giorgosioak\033[0m")
    print(" Enter coords from links or text to teleport")
    print("\033[94m~=~=~ ~=~=~ ~=~=~ ~=~=~ ~=~=~ ~=~=~ ~=~=~ ~=~=~\033[0m")

    # read line from input
    for line in sys.stdin:
        regex = re.search(COORD_PATTERN, line)
        matched = regex.group(0) if regex else ""

        if matched != "":
            line = matched.split(',')
            lat  = str(line[0].strip())
            lon = str(line[1].strip())
        elif "back" in line:
            lat = str(pc[0])
            lon = str(pc[1])
        elif any(x in line for x in ["quit", "exit"]):
            print('\033[94m' + "• Exiting..." + '\033[0m')
            exit()
        else:
            print('\033[91m' + "× No coords match! Skipping..." + '\033[0m')
            continue

        # Setup teleport command
        cmd = "adb.exe" if platform.system() == "Windows" else "adb"
        cmd += " shell am start-foreground-service -a theappninjas.gpsjoystick.TELEPORT --ef lat " + lat + " --ef lng " + lon
        cmd += " >nul 2>&1" if platform.system() == "Windows" else " > /dev/null 2>&1" # ignore output
        os.system(cmd)

        lat = float(lat)
        lon = float(lon)

        dist = get_distance(lat,lon,lc[0],lc[1])
        cd,safe = get_cooldown(dist)
        

        if 0.0 in lc:
            print('\033[93m' + "» Teleporting..." + '\033[0m')
            lc = [lat, lon] # for back command
        elif dist == 0:
            print('\033[93m' + "» Teleporting... Distance: " + '\033[94m' + '\033[1m' + str(round(dist,2)) + "km" +  '\033[0m' + '\033[93m' + " Cooldown: " + '\033[92m' + '\033[1m' + cd + '\033[0m')
        elif "120m" in cd:
            print('\033[93m' + "» Teleporting... Distance: " + '\033[94m' + '\033[1m' + str(round(dist,2)) + "km" +  '\033[0m' + '\033[93m' + " Cooldown: " + '\033[92m' + '\033[1m' + cd + '\033[0m')
        else:
            print('\033[93m' + "» Teleporting... Distance: " + '\033[94m' + '\033[1m' + str(round(dist,2)) + "km" +  '\033[0m' + '\033[93m' + " Cooldown: " + '\033[92m' + '\033[1m' + cd + "~" + safe + '\033[0m')

        # Save coords
        pc = lc # save to previous
        lc = [lat, lon] # replace latest
#End

# CALL MAIN
if __name__ == "__main__":
    main(sys.argv[1:])
