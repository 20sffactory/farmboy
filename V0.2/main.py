#notes:
#waterlevel max = 5cm from top (pump off)
#waterlevel max = 10.8cm from top (pump on)


import systemupdate
import chatbot
import sensors
import datacontrol
import camera

if __name__ == "__main__":
	print("Initiate FarmboyOS")
	sensors.setupSensor()	
	chatbot.updater.start_polling()
	camera.startCamera()

	while True:
		sensors.readSensorData()
		systemupdate.botHandler()
		systemupdate.safetyCheck()
		datacontrol.writeData()

