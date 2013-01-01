# Pyplex

## Introduction

This is an implementation of an idea on the Plex forums - that the Raspberry Pi
could use a Plex client that had no interface, and was just designed to be 
operated using an iOS device or similar as a remote. Only the very barest bones
functionality is here, but I hope that it is reasonably easy to extend.

## Before you install

	sudo apt-get update && sudo apt-get upgrade
	sudo wget https://raw.github.com/Hexxeh/rpi-update/master/rpi-update
	sudo cp rpi-update /usr/local/bin/rpi-update
	sudo chmod +x /usr/local/bin/rpi-update 
	sudo rpi-update 192
	sudo reboot
	sudo vim config.txt > to set arm_freq to 1000
	sudo reboot
	sudo apt-get install avahi-daemon
	sudo apt-get install python-pip
	sudo pip install tornado
	sudo pip install pexpect
	sudo apt-get install python-avahi 
	sudo aptitude install python-gobject
	
## How to use

Launch with 

    python pyplex [hdmi] &

Where [hdmi] is optional to make sure audio is going
over hdmi, leaving it out will devault to the 3,5mm jack output.
The `&` makes it run in the background.

Then 'Raspberry Plex' should appear as a player you can choose in your Plex
client. Choose your media, and select this as the player to play it on. It should 
begin playing on your Raspberry Pi! 

Stop with 

	python pyplex stop

## Debugging and logging

In the root folder of pyplex do
	
	tail -f pyplex.log

to see all logging information.

To control playback you can use the remote tab on your iDevice or android device.
Currently the following commands are supported:
```
Play
Pauze
Fastforward
Fastbackward
Stop
```

Support can be found on the [Plex forum][plexForum] 


[plexForum]: http://forums.plexapp.com/index.php/topic/35906-raspberry-pi


