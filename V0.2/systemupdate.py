import time
import chatbot
import globalvar
import RPi.GPIO as GPIO
import cameracontrol
from apscheduler.schedulers.background import BackgroundScheduler

def IOHIGH(io):
	GPIO.output(io, GPIO.HIGH)
def IOLOW(io):
	GPIO.output(io, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setup(globalvar.ioPump0, GPIO.OUT, initial = 1)
GPIO.setup(globalvar.ioAirPump, GPIO.OUT, initial = 1)
GPIO.setup(globalvar.ioLed, GPIO.OUT, initial = 1)
GPIO.setup(globalvar.ioUv, GPIO.OUT, initial = 1)
GPIO.setup(globalvar.ioSeedling, GPIO.OUT, initial = 1)

def pumpTimer():
	IOLOW(globalvar.ioPump0)
	globalvar.pumpStatus = 1
	print('Pump On.')
	time.sleep(globalvar.onTime)
	IOHIGH(globalvar.ioPump0)
	globalvar.pumpStatus = 0
	print('Pump Off.')
	chatbot.updater.bot.send_message(chat_id=globalvar.chat_id, text="Pump cycle done & restarted.")

def seedlingTimer():
	IOLOW(globalvar.ioSeedling)
	globalvar.seedlingStatus = 1
	print('Seedling Pump On.')
	time.sleep(globalvar.seedlingOnTime)
	IOHIGH(globalvar.ioSeedling)
	globalvar.seedlingStatus = 0
	print('Seedling Pump Off.')
	chatbot.updater.bot.send_message(chat_id=globalvar.chat_id, text="Seedling pump cycle done & restarted.")

pumpSched = BackgroundScheduler()
pumpJob = pumpSched.add_job(pumpTimer, 'interval', seconds = globalvar.onTime + globalvar.offTime)
seedlingSched = BackgroundScheduler()
seedlingJob = seedlingSched.add_job(seedlingTimer, 'interval', seconds = globalvar.seedlingOnTime + globalvar.seedlingOffTime)

def botHandler():
	if 	globalvar.botInput == 1:
		
		#Pump Timer Handler
		if globalvar.pumpTimerInput == 1:
			if globalvar.pumpTimerInit == 0:
				botReply = "Pump timer begins in: " + str(globalvar.onTime + globalvar.offTime) + "s."
				#pumpTimer()
				pumpSched.start()
				globalvar.pumpTimerInit = 1
				globalvar.pumpTimerStatus = 1
			elif globalvar.pumpTimerInit == 1:
				if globalvar.pumpTimerStatus == 1:
					pumpSched.pause()
					botReply = "Pump timer paused."
					globalvar.pumpTimerStatus = 0
				elif globalvar.pumpTimerStatus == 0:
					pumpSched.resume()
					botReply = "Pump timer resumed."
					globalvar.pumpTimerStatus = 1
			globalvar.pumpTimerInput = 0

		#Seedling Timer Handler
		if globalvar.seedlingTimerInput == 1:
			if globalvar.seedlingTimerInit == 0:
				botReply = "Seedling timer begins in: " + str(globalvar.seedlingOnTime + globalvar.seedlingOffTime) + "s."
				#seedlingTimer()
				seedlingSched.start()
				globalvar.seedlingTimerInit = 1
				globalvar.seedlingTimerStatus = 1
			elif globalvar.seedlingTimerInit == 1:
				if globalvar.seedlingTimerStatus == 1:
					seedlingSched.pause()
					botReply = "Seedling timer paused."
					globalvar.seedlingTimerStatus = 0
				elif globalvar.seedlingTimerStatus == 0:
					seedlingSched.resume()
					botReply = "Seedling timer resumed."
					globalvar.seedlingTimerStatus = 1
			globalvar.seedlingTimerInput = 0

		#Pump On/Off Handler
		if globalvar.pumpInput == 1:
			if globalvar.pumpStatus == 0:
				IOLOW(globalvar.ioPump0)
				globalvar.pumpStatus = 1
				botReply = "Pump on."
			elif globalvar.pumpStatus == 1:
				IOHIGH(globalvar.ioPump0)
				globalvar.pumpStatus = 0
				botReply = "Pump off."
			globalvar.pumpInput = 0

		#Air Pump On/Off Handler
		if globalvar.airPumpInput == 1:
			if globalvar.airPumpStatus == 0:
				IOLOW(globalvar.ioAirPump)
				globalvar.airPumpStatus = 1
				botReply = "Air on."
			elif globalvar.airPumpStatus == 1:
				IOHIGH(globalvar.ioAirPump)
				globalvar.airPumpStatus = 0
				botReply = "Air off."
			globalvar.airPumpInput = 0

		#LED On/Off Handler
		if globalvar.ledInput == 1:
			if globalvar.ledStatus == 0:
				IOLOW(globalvar.ioLed)
				globalvar.ledStatus = 1
				botReply = "LED on."
			elif globalvar.ledStatus == 1:
				IOHIGH(globalvar.ioLed)
				globalvar.ledStatus = 0
				botReply = "LED off."
			globalvar.ledInput = 0

		#UV On/Off Handler
		if globalvar.uvInput == 1:
			if globalvar.uvStatus == 0:
				IOLOW(globalvar.ioUv)
				globalvar.uvStatus = 1
				botReply = "UV on."
			elif globalvar.uvStatus == 1:
				IOHIGH(globalvar.ioUv)
				globalvar.uvStatus = 0
				botReply = "UV off."
			globalvar.uvInput = 0

		#Seedling On/Off Handler
		if globalvar.seedlingInput == 1:
			if globalvar.seedlingStatus == 0:
				IOLOW(globalvar.ioSeedling)
				globalvar.seedlingStatus = 1
				botReply = "Seedling Pump on."
			elif globalvar.seedlingStatus == 1:
				IOHIGH(globalvar.ioSeedling)
				globalvar.seedlingStatus = 0
				botReply = "Seedling Pump off."
			globalvar.seedlingInput = 0
		
		globalvar.botInput = 0
		chatbot.updater.bot.send_message(chat_id=globalvar.chat_id, text=botReply)

def safetyCheck():
	#Leakage Check
	if globalvar.dataLeak == 1:
		globalvar.dataLeakTime = globalvar.dataTime
		chatbot.updater.bot.send_message(chat_id=globalvar.chat_id, text="!!LEAKAGE DETECTED!!")
