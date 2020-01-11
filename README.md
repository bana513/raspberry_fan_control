# Raspberry Pi 3 automatic fan control
Automatic fan control based on CPU temperature using PWM signal
![alt text](./images/upper_view.jpg)
![alt text](./images/open_case.jpg)

## Create circuit
Circuit sketch:  
  
<img src="images/sketch.jpg"  height="200">

Final circuit:  
  
<img src="images/circuit.jpg"  height="250">

## Pinout
I chose the GPIO pin 18 (pin 12) as it is the closest to power pins. However you can use other GPIO pins as well.  
Raspberry Pi 2/3 pinout ():
  
<img src="https://camo.githubusercontent.com/c3197e779c0fbb43b610f7260099065c2c9629d1/68747470733a2f2f646f63732e6d6963726f736f66742e636f6d2f656e2d75732f77696e646f77732f696f742d636f72652f6d656469612f70696e6d617070696e67737270692f7270325f70696e6f75742e706e67"  width="500">

## Write Python script
I used Python 3.5 for my code. See the code in ```fancontrol.py```.


## Run script on startup
You will need to add startup script as root because of GPIO pins (more sophisticated permissions would be nice if you care more about security, e.g. create a group, allow GPIO pin access to the group, then add your user to the group). Now I want to keep it simple.
```console
bana@banarpi:~ $ sudo su
```

Edit root´s crontab file:
```console
root@banarpi:/home/bana# crontab -e
```

Add the following line to your crontab file which will always start to run in background on startup:
```shell
...
@reboot python /location/to/file/fancontrol.py /location/to/file/config.json
```

## Config
You can choose 2 different modes:
1. PWM controlled fan - fan speeds for each temperature level are specified in config file
2. Binary ON/OFF - turn ON/OFF temperature can be specified

Option 1 can handle variable speeds, however you may hear some PWM noise, which is a deaden with a capacitor, depends also on the fan, how annoying is this phenomenon, so you can choose the other mode if you want to.  
