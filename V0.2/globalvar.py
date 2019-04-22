#Reservoir Dimension
resHeight = 35 #from tank bottom up to ultrasonic sensor in cm
#resLength = 
#resWidth = 

#EC/TDS Calibration Formula
def ecReading(ecV):
	ec = (133.42*ecV*ecV*ecV - 255.86*ecV*ecV + 857.39*ecV)*1.55/1000
	return ec

#Serial Config
serialPort = '/dev/ttyUSB0'
serialBaud = 115200
bytesize = 8
timeout = 1

#GPIO io Pins
ioPump0 = 21 #AC
ioUv = 20 #AC
ioAirPump = 16 #AC
#io5 = 12 #AC
ioLed = 26 #12V1A (4 Channel Total < 1.5A)
ioSeedling = 19 #12V
#io2 = 13 #12V
#io1 = 6 #12V

#Telegram Chatbot Key
tokenkey = '000000000:XXXXXXXXXXXXXXXXXXXXXXXXXX'

#Main Pump Schedule Config in seconds
onTime = 600
offTime = 1200

#Seedling Pump Schedule Config in seconds
seedlingOnTime = 200
seedlingOffTime = 1600

#Input Indicator
botInput, pumpTimerInput, pumpInput, \
airPumpInput, ledInput, uvInput, \
seedlingInput, seedlingTimerInput\
=\
0, 0, 0, \
0, 0, 0, \
0, 0

#Pump0 Status
pumpTimerInit, pumpTimerStatus, pumpStatus =\
0, 0, 0

seedlingTimerInit, seedlingTimerStatus, seedlingStatus =\
0, 0, 0

#AirPump Status
airPumpStatus = 0

#LED Status
ledStatus = 0

#UV Status
uvStatus = 0

#chat_id
chat_id = ""

#Sensor Data 
dataTime, dataTemp, dataWaterLevel, \
dataPh, dataEcV, dataEc, \
dataLight, dataAirTemp, dataAirHumid \
= \
[], [], [], \
[], [], [], \
[], [], []
dataLeak = 0
dataLeakTime = 0

#Data Saving Frequency (data count per save)
dataSavingCount = 60
