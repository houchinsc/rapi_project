#!/usr/bin/env python
#
# Test SDL_Pi_SunControl
# John C. Shovic, SwitchDoc Labs
# April 27, 2017
#
#

#configuraton:
# Connect a Grove Cable from Grove I2C on SunControl to an I2C Port on Pi2Grover (Grove hat for the Raspberry Pi)
# Connect a Grove Cable from Grove USB Control on SunControl to  D21/D26 on Pi2Grover (Grove hat for the Raspberry Pi)


# imports

import sys
#import gpiozero

#led = gpiozero.LED(17)

import time
import datetime
import random
import SDL_Pi_SunControl

# Main Program

print ""
print "Test SDL_Pi_SunControl Version 1.0 - SwitchDoc Labs"
print ""
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""

# configuration

INA3221Address = 0x40

#Pin_USBControlControl = 21
#Pin_USBControlEnable = 26

critical_control = 21
critical_enable = 26

variable_control = 6
variable_enable = 12

Pin_WatchDog_Done = 13
Pin_WatchDog_Wake = 16

filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.datetime.utcnow()


critical = SDL_Pi_SunControl.SDL_Pi_SunControl(INA3221Address=INA3221Address, USBControlEnable=critical_enable, USBControlControl=critical_control, WatchDog_Done = Pin_WatchDog_Done, WatchDog_Wake=Pin_WatchDog_Wake)
variable = SDL_Pi_SunControl.SDL_Pi_SunControl(INA3221Address=INA3221Address, USBControlEnable=variable_enable, USBControlControl=variable_control, WatchDog_Done=Pin_WatchDog_Done, WatchDog_Wake=Pin_WatchDog_Wake)

while True:

	print "------------------------------"
	print "SunControl Voltages and Currents - New"
  	print "------------------------------"

	# set Label
	#myLabel = "LIPO_Battery"

  	#print "%s Load Voltage :\t  %3.2f V" % (myLabel, sunControl.readChannelVoltageV(SDL_Pi_SunControl.SunControl_LIPO_BATTERY_CHANNEL))
  	#print "%s Current :\t\t  %3.2f mA" % (myLabel, sunControl.readChannelCurrentmA(SDL_Pi_SunControl.SunControl_LIPO_BATTERY_CHANNEL))
  	#print

        # set Label
	#myLabel = "Solar Cell"

  	#print "%s Load Voltage :\t  %3.2f V" % (myLabel, sunControl.readChannelVoltageV(SDL_Pi_SunControl.SunControl_SOLAR_CELL_CHANNEL))
  	#print "%s Current :\t\t  %3.2f mA" % (myLabel, sunControl.readChannelCurrentmA(SDL_Pi_SunControl.SunControl_SOLAR_CELL_CHANNEL))
  	#print


	# set Label
	#myLabel = "Output"

  	#print "%s Load Voltage :\t\t  %3.2f V" % (myLabel, sunControl.readChannelVoltageV(SDL_Pi_SunControl.SunControl_OUTPUT_CHANNEL))
  	#print "%s Current :\t\t  %3.2f mA" % (myLabel, sunControl.readChannelCurrentmA(SDL_Pi_SunControl.SunControl_OUTPUT_CHANNEL))
  	#print


	#
	time.sleep(2.0)

	# Turn the USB Power Off
	critical.setUSBControl(True)
	critical.setUSBEnable(True)
	critical.setUSBControl(False)

	variable.setUSBControl(True)
	variable.setUSBEnable(True)
	variable.setUSBControl(False)

	print "------"
	print "USB Power turned OFF"
	print "------"

	time.sleep(10.0)

        #led.on()
	# set Label
  	print "------------------------------"
	print "SunControl Voltages and Currents"
  	print "------------------------------"

	myLabel = "LIPO_Battery"

  	#print "%s Load Voltage :\t  %3.2f V" % (myLabel, sunControl.readChannelVoltageV(SDL_Pi_SunControl.SunControl_LIPO_BATTERY_CHANNEL))
  	#print "%s Current :\t\t  %3.2f mA" % (myLabel, sunControl.readChannelCurrentmA(SDL_Pi_SunControl.SunControl_LIPO_BATTERY_CHANNEL))
  	#print

        # set Label
	myLabel = "Solar Cell"

  	#print "%s Load Voltage :\t  %3.2f V" % (myLabel, sunControl.readChannelVoltageV(SDL_Pi_SunControl.SunControl_SOLAR_CELL_CHANNEL))
  	#print "%s Current :\t\t  %3.2f mA" % (myLabel, sunControl.readChannelCurrentmA(SDL_Pi_SunControl.SunControl_SOLAR_CELL_CHANNEL))
  	#print


	# set Label
	myLabel = "Output"

  	#print "%s Load Voltage :\t\t  %3.2f V" % (myLabel, sunControl.readChannelVoltageV(SDL_Pi_SunControl.SunControl_OUTPUT_CHANNEL))
  	#print "%s Current :\t\t  %3.2f mA" % (myLabel, sunControl.readChannelCurrentmA(SDL_Pi_SunControl.SunControl_OUTPUT_CHANNEL))

	time.sleep(2.0)

	print "------"
	print "USB Power turned ON"
	print "------"

	critical.setUSBControl(True)
	critical.setUSBEnable(True)
	variable.setUSBControl(True)
	variable.setUSBEnable(True)

	time.sleep(10.0)
	#led.off()
