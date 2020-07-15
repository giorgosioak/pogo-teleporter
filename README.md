### GPS teleport via adb (GPS Joystick)

Teleporter for PoGo written in python 3.<br>
Uses "GPS Joystick" adb commands to connected device.

How it works:
```
Insert gps coords ( one per line )
Teleports you directly and informs you for the cooldown.
Cooldown time is based on distance from last coords.
```

Runtime Example:
``` bash
$ python teleporter.py 
41.668097,-0.897650
» Teleporting...
29.561898,-95.281464
» Teleporting... Distance: 8213.16km Cooldown: 2h
  @Shundo💯✨ 29.561898,-95.281464
» Teleporting... Distance: 0.0km Cooldown: 0s~30s
this should throw error
× No coords match! Skipping...
```

More info:
* [GPS Joystick](http://gpsjoystick.theappninjas.com/)