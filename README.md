SensorShip
==========

Sensorship is a container orchestration framework that allows you to ship Docker containers as physically close as possible to your sensors.

Currently Supported Stack:
- Raspberry Pi 2
- GrovePi+ board
- Grove Kit sensors


Platform Configuration
======================

- Format the SD card as FAT32 and write the Hypriot OS v0.5 “Will” image: http://downloads.hypriot.com/hypriot-rpi-20151004-132414.img.zip
- Put the SD card in the Raspberry Pi, connect a Power Cable and an Ethernet Cable
- Discover the IP of the Raspberry Pi in the network (Linux: arp-scan --interface eth0 10.0.0.0/24)
- ssh root@ip, password: hypriot
- Test Docker with “docker info”
- Pull our (future) base image: docker pull resin/rpi-raspbian
- sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y git python
- http://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/


Wi-Fi Configuration
===========
- sudo apt-get install -y wicd-cli wicd-curses
- wicd-curses
- Find the preferred network to connect to, press the right arrow key, scroll down to "connect to this network automatically" and press space
- Reboot the device
