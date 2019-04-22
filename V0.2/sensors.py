import serial
import time
import json
import globalvar
import math
import datacontrol

ser = serial.Serial(globalvar.serialPort, baudrate=globalvar.serialBaud, bytesize=globalvar.bytesize, timeout= globalvar.timeout)
time.sleep(1)
startTime = int(time.time())
currentTime = startTime

def readSensorData():
	global currentTime
	while ser.in_waiting > 0:
		dataJson = ser.readline()
		dataDict = json.loads(dataJson.decode('utf-8'))
		currentTime = int(time.time())
		dataDict['idtime'] = currentTime
		processSensors(dataDict)

def processSensors(dataDict):
	#if dataDict['idtime'] != globalvar.dataTime[-1]:
	globalvar.dataTime.append(currentTime)
	globalvar.dataTemp.append(dataDict['temp'])
	globalvar.dataWaterLevel.append(globalvar.resHeight - dataDict['level'])
	globalvar.dataPh.append(dataDict['ph'])
	ecvComp = dataDict['ecv'] / (1+0.02*(dataDict['temp']-25))
	globalvar.dataEcV.append(ecvComp)
	globalvar.dataEc.append(globalvar.ecReading(ecvComp))
	globalvar.dataLight.append((1024-dataDict['light'])/1024)
	globalvar.dataAirTemp.append(dataDict['airtemp'])
	globalvar.dataAirHumid.append(dataDict['airhumid'])
	globalvar.dataLeak = dataDict['leak']
	#print(dataDict)
	#print(globalvar.dataEc[-1])

def setupSensor():
	ser.write("1".encode())
	print("Initiate Sensor Inputs.")