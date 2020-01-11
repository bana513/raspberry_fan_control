# Raspberry Pi 3 automatic fan control
Automatic fan control based on CPU temperature using PWM signal
![alt text](./images/upper_view.jpg)
![alt text](./images/open_case.jpg)

## Create circuit
Circuit sketch:  
<img src="images/sketch.jpg"  height="200">

Final circuit:  
<img src="images/circuit.jpg"  height="250">

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
