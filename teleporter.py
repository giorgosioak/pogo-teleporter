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

COORD_PATTERN = r"-?(\d{1,3})\.(\d{1,15})[ ]?,[ ]?-?(\d{1,3})\.(\d{1,15})"

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
    km = [0,1,5,10,25,30,65,81,100,250,500,750,1000,1500]
    cd = ["0s","30s","2m","6m","11m","14m","22m","25m","35m","45m","1h","1.3h","1.5h","2h","2h"]
    if dist > 1500:
        return "2h", "2h"
    for i,v in enumerate(km):
        if v > dist:
            return cd[i-1], cd[i]

def yellowprint(text):
    """Print in yellow"""
    print( + text + '\033[0m')

def main(argv):
    """Main fuction."""
    lc = [200.0 , 200.0] # last coords
    blc = lc # before last coords
    
    # read line from input
    for line in sys.stdin:
        regex = re.search(COORD_PATTERN, line)
        matched = regex.group(0) if regex else ""
        if matched == "" and "back" not in line:
            print('\033[91m' + "× No coords match! Skipping..." + '\033[0m')
            continue
        elif matched == "" and "back" in line:
            lat = str(blc[0])
            lon = str(blc[1])
        else:
            line = matched.split(',')
            lat  = str(line[0].strip())
            lon = str(line[1].strip())

        # Setup teleport command
        cmd = "adb.exe" if platform.system() == "Windows" else "adb"
        cmd += " shell am start-foreground-service -a theappninjas.gpsjoystick.TELEPORT --ef lat " + lat + " --ef lng " + lon
        cmd += " >nul 2>&1" if platform.system() == "Windows" else " > /dev/null 2>&1" # ignore output
        os.system(cmd)

        lat = float(lat)
        lon = float(lon)

        dist = get_distance(lat,lon,lc[0],lc[1])
        cd,safe = get_cooldown(dist)
        

        if 200.0 in lc:
            print('\033[93m' + "» Teleporting..." + '\033[0m')
            lc = [lat, lon] # for back command
        elif "2h" in cd:
            print('\033[93m' + "» Teleporting... Distance: " + '\033[94m' + '\033[1m' + str(round(dist,2)) + "km" +  '\033[0m' + '\033[93m' + " Cooldown: " + '\033[92m' + '\033[1m' + cd + '\033[0m')
        else:
            print('\033[93m' + "» Teleporting... Distance: " + '\033[94m' + '\033[1m' + str(round(dist,2)) + "km" +  '\033[0m' + '\033[93m' + " Cooldown: " + '\033[92m' + '\033[1m' + cd + "~" + safe + '\033[0m')

        # Save last coords
        blc = lc
        lc = [lat, lon]
#End

# CALL MAIN
if __name__ == "__main__":
    main(sys.argv[1:])
