import json
import globalvar
import math
from statistics import median
import sqlite3

conn = sqlite3.connect('data.db')
curs = conn.cursor()

curs.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sensors' ''')

if curs.fetchone()[0] == 0:
	curs.execute("""CREATE TABLE sensors (
			idtime integer,
			temp real,
			waterlevel real,
			ph real,
			ecv real,
			ec real,
			light real,
			airtemp real,
			airhumid real
		)""")
	conn.commit()

def writeData():
	if len(globalvar.dataTime) >= globalvar.dataSavingCount:
		medTime, medTemp, medWaterLevel, medPh, medEcV, medEc, medLight, medAirTemp, medAirHumid = \
		int(median(globalvar.dataTime)), median(globalvar.dataTemp), median(globalvar.dataWaterLevel), \
		median(globalvar.dataPh), median(globalvar.dataEcV), median(globalvar.dataEc), \
		median(globalvar.dataLight), median(globalvar.dataAirTemp), median(globalvar.dataAirHumid)

		globalvar.dataTime, globalvar.dataTemp, globalvar.dataWaterLevel, \
		globalvar.dataPh, globalvar.dataEcV, globalvar.dataEc, \
		globalvar.dataLight, globalvar.dataAirTemp, globalvar.dataAirHumid = \
		[], [], [], \
		[], [], [], \
		[], [], []

		medDict = {
			"idtime": medTime,
			"temp": medTemp,
			"level": medWaterLevel,
			"ph": medPh, 
			"ecv": medEcV,
			"ec": medEc,
			"light": medLight,
			"airtemp": medAirTemp,
			"airhumid": medAirHumid
		}
		curs.execute("INSERT INTO sensors VALUES (:idtime, :temp, :level, :ph, :ecv, :ec, :light, :airtemp, :airhumid)", medDict)
		print("Memory saved to Database:")
		print(medDict)
		conn.commit()

def shutdown():
	conn.close()
