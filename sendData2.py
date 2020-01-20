#!/usr/bin/env python
# imports
import requests
import sys
import time
import datetime
import random 
import SDL_Pi_INA3221

# Main Program

filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.datetime.utcnow()

ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)

# the three channels of the INA3221 named for SunAirPlus Solar Power Controller channels (www.switchdoc.com)
LIPO_BATTERY_CHANNEL = 1
SOLAR_CELL_CHANNEL   = 2
OUTPUT_CHANNEL       = 3

AUTHORIZATION_TOKEN  = "87988823bf25d0288adf21b477b8c51c"
DEVICE_ID            = "7013d728-13a5-4a54-b5ed-95e077543525"


data_header = '{"mode":"async", "messageType":"607fadbd8beb6110e1df", "messages":[{'
data_trailer = '}]}'

MULTI_CHAIN_URL = "https://maas-proxy.cfapps.eu10.hana.ondemand.com/6119818b-436a-4c19-9a40-1ef81cb3b6a8/rpc"
ADDRESS = "1ETfghCegSKZCjTSiZyZ7EoYrhoxTGbTfb2bnZ"
ASSET = "DEnergyCoin"
	
mc_data_header = "{\"method\": \"issuemore\", \"params\": ["
mc_data_trailer =  "]}"
	
	
mc_headers = {'apikey': "HjxqWENuFCMzsAK9DgYfmShosFrH4Umpj3MxVFCjncA2M8mcVAnyxAZ5F6gUgwhY"}

loopcount = 0

duration = 10.0


totalEnergy = 0.0
 
while True:

  	print "------------------------------"
  	shuntvoltage1 = 0
  	busvoltage1   = 0
  	current_mA1   = 0
  	loadvoltage1  = 0


  	busvoltage1 = ina3221.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
  	shuntvoltage1 = ina3221.getShuntVoltage_mV(LIPO_BATTERY_CHANNEL)
  	# minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
  	current_mA1 = ina3221.getCurrent_mA(LIPO_BATTERY_CHANNEL)  

  	loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)
  
  	#print "LIPO_Battery Bus Voltage: %3.2f V " % busvoltage1
  	#print "LIPO_Battery Shunt Voltage: %3.2f mV " % shuntvoltage1
  	#print "LIPO_Battery Load Voltage:  %3.2f V" % loadvoltage1
  	#print "LIPO_Battery Current 1:  %3.2f mA" % current_mA1
  	
    	batteryVoltage = '"batteryVoltage":"' + str(loadvoltage1) + '",'
	batteryCurrent = '"batteryCurrent":"' + str(current_mA1) + '",'

  	#print

  	shuntvoltage2 = 0
  	busvoltage2 = 0
  	current_mA2 = 0
  	loadvoltage2 = 0

  	busvoltage2 = ina3221.getBusVoltage_V(SOLAR_CELL_CHANNEL)
  	shuntvoltage2 = ina3221.getShuntVoltage_mV(SOLAR_CELL_CHANNEL)
  	current_mA2 = -ina3221.getCurrent_mA(SOLAR_CELL_CHANNEL)
  	loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000)
  
  	#print "Solar Cell Bus Voltage 2:  %3.2f V " % busvoltage2
  	#print "Solar Cell Shunt Voltage 2: %3.2f mV " % shuntvoltage2
  	#print "Solar Cell Load Voltage 2:  %3.2f V" % loadvoltage2
  	#print "Solar Cell Current 2:  %3.2f mA" % current_mA2
  	#print 

  	shuntvoltage3 = 0
  	busvoltage3 = 0
  	current_mA3 = 0
  	loadvoltage3 = 0

  	busvoltage3 = ina3221.getBusVoltage_V(OUTPUT_CHANNEL)
  	shuntvoltage3 = ina3221.getShuntVoltage_mV(OUTPUT_CHANNEL)
  	current_mA3 = ina3221.getCurrent_mA(OUTPUT_CHANNEL)
  	loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000)
  	
	loadVoltage = '"loadVoltage":"' + str(loadvoltage3) + '",'
	loadCurrent = '"loadCurrent":"' + str(current_mA3) + '",'
	
  	
  
  	#print "Output Bus Voltage 3:  %3.2f V " % busvoltage3
  	#print "Output Shunt Voltage 3: %3.2f mV " % shuntvoltage3
  	#print "Output Load Voltage 3:  %3.2f V" % loadvoltage3
  	#print "Output Current 3:  %3.2f mA" % current_mA3
  	#print
		
	panelVoltage = '"panelVoltage":"' + str(loadvoltage2) + '",'
	panelCurrent = '"panelCurrent":"' + str(current_mA2) + '",'

	# send to IoT service
	URL = "https://iotmmsb400fd1ce1.us3.hana.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/" + DEVICE_ID
	
	
	current_milli_time = lambda: int(round(time.time()))

	timestamp = '"timestamp":"' + str(current_milli_time()) + '"'
	
	payload = data_header + panelVoltage  + panelCurrent + batteryVoltage + batteryCurrent + loadVoltage + loadCurrent + timestamp + data_trailer
		
		 
	#data = '{"mode":"async","messageType":"607fadbd8beb6110e1df","messages":[{"panelVoltage":"2.22","panelCurrent":"1.24","batteryVoltage":"2.44","batteryCurrent":"0.55","loadVoltage":"5.22","loadCurrent":"2.0","timestamp":1413191650}]}'

	

	headers={'Content-Type':'application/json;charset=utf-8', 'Authorization': 'Bearer ' + AUTHORIZATION_TOKEN}


	r = requests.post(url = URL, data = payload, headers = headers)

	print("Response is %s", r.text)
	
	mwatts = loadvoltage2*current_mA2;
        print("mWatts %s", str(mwatts))
	mwattHour = mwatts*(duration/360)
        print("mWatt Hour %s", str(mwattHour))
	

        totalEnergy = totalEnergy + mwattHour;
 	
	loopcount = loopcount + 1
	
	if loopcount > 5:
		
                print("Total Energy %s", str(totalEnergy))
 
		mc_headers = {'apikey': "HjxqWENuFCMzsAK9DgYfmShosFrH4Umpj3MxVFCjncA2M8mcVAnyxAZ5F6gUgwhY"}
	
		#mc_payload = "{\"method": \"issuemore\", \"params\": [\"1ETfghCegSKZCjTSiZyZ7EoYrhoxTGbTfb2bnZ\",\"SAPEnergyCoin\",2]}"
	
	
		mc_payload = mc_data_header + "\"" +  ADDRESS + "\",\"" + ASSET + "\"," + str(totalEnergy) + mc_data_trailer

		print("Request is %s", mc_payload)
			

		r1 = requests.post(url = MULTI_CHAIN_URL, data = mc_payload, headers = mc_headers, verify = False)

		print("Response is %s", r1.text)
		
		totalEnergy = 0.0
		
		loopcount = 0
		
		

	time.sleep(duration)



