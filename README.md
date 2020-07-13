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
29.580623,-98.694229
» Teleporting...
 43.895691,-79.234850
» Teleporting... Distance: 2348.67km Cooldown: 2h
```

More info:
* [GPS Joystick](http://gpsjoystick.theappninjas.com/)