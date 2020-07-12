#!/usr/bin/python
# coding=utf-8
'''
Python 3 - Teleport to coords
Developed by George Ioakeimidis <giorgosioak95@gmail.com>
'''
import os
import sys

def main(argv):

    # read line from input
    for line in sys.stdin:
        line = line.split(',')    
        lat  = str(line[0].strip())
        long = str(line[1].strip())
        
        # Setup teleport command 
        cmd = "adb shell am start-foreground-service -a theappninjas.gpsjoystick.TELEPORT --ef lat " + lat + " --ef lng " + long
        cmd += " > /dev/null 2>&1" # ignore output
        os.system(cmd)

#End

# CALL MAIN
if __name__ == "__main__":
    main(sys.argv[1:])
