from telegram.ext import Updater
from telegram.ext import CommandHandler
from datetime import datetime
import logging
import globalvar

updater = Updater(token = globalvar.tokenkey)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def onoff(var):
	return "On" if var == 1 else "Off"

def runstatus(bot, update):
	botReply = \
	"Status:" \
	+"\nMain Pump: "+onoff(globalvar.pumpStatus)\
	+"\nSeedling Pump: "+onoff(globalvar.seedlingStatus)\
	+"\nGrow Lights: "+onoff(globalvar.ledStatus)\
	+"\nUV Sanitizer: "+onoff(globalvar.uvStatus)\
	+"\nAir Pump: "+onoff(globalvar.airPumpStatus)\
	+"\n"\
	+"\nPump Timer: " +onoff(globalvar.pumpTimerStatus)\
	+"\nInterval: On "+str(globalvar.onTime)+"s - Off "+str(globalvar.offTime)+"s"\
	+"\nSeedling Timer: "+onoff(globalvar.seedlingTimerStatus)\
	+"\nInterval: On "+str(globalvar.seedlingOnTime)+"s - Off "+str(globalvar.seedlingOffTime)+"s"
	updater.bot.send_message(chat_id=update.message.chat_id, text=botReply)

def status(bot, update):
	botReply = \
	"Time (UTC): "+datetime.utcfromtimestamp(globalvar.dataTime[-1]).strftime('%Y-%m-%d %H:%M')\
	+"\nWater Temperature: "+"%.1f"%globalvar.dataTemp[-1]+u"\u00b0"+"C"\
	+"\nWater Level: "+"%.1f"%globalvar.dataWaterLevel[-1]+"cm"\
	+"\npH Level: "+"%.2f"%globalvar.dataPh[-1]\
	+"\nEC Voltage: "+"%.4f"%globalvar.dataEcV[-1]+"V"\
	+"\nEC Estimate: "+"%.2f"%globalvar.dataEc[-1]+"mS/cm"\
	+"\nLight Intensity: "+"%.1f"%(globalvar.dataLight[-1]*100)+"%"\
	+"\nAir Temperature: "+"%.1f"%globalvar.dataAirTemp[-1]+u"\u00b0"+"C"\
	+"\nAir Humidity: "+"%.2f"%globalvar.dataAirHumid[-1]+"%"
	updater.bot.send_message(chat_id=update.message.chat_id, text=botReply)

def pumptimer(bot, update):
	globalvar.botInput = 1
	globalvar.pumpTimerInput = 1
	globalvar.chat_id = update.message.chat_id

def seedlingtimer(bot, update):
	globalvar.botInput = 1
	globalvar.seedlingTimerInput = 1
	globalvar.chat_id = update.message.chat_id

def pump(bot, update):
	globalvar.botInput = 1
	globalvar.pumpInput = 1
	globalvar.chat_id = update.message.chat_id

def air(bot, update):
	globalvar.botInput = 1
	globalvar.airPumpInput = 1
	globalvar.chat_id = update.message.chat_id

def led(bot, update):
	globalvar.botInput = 1
	globalvar.ledInput = 1
	globalvar.chat_id = update.message.chat_id

def uv(bot, update):
	globalvar.botInput = 1
	globalvar.uvInput = 1
	globalvar.chat_id = update.message.chat_id

def seedling(bot, update):
	globalvar.botInput = 1
	globalvar.seedlingInput = 1
	globalvar.chat_id = update.message.chat_id

def image(bot, update):
	#bot send real time image
	globalvar.chat_id = update.message.chat_id

runstatus_handler = CommandHandler('runstatus', runstatus)
dispatcher.add_handler(runstatus_handler)

status_handler = CommandHandler('status', status)
dispatcher.add_handler(status_handler)

pumptimer_handler = CommandHandler('pumptimer', pumptimer)
dispatcher.add_handler(pumptimer_handler)

seedlingtimer_handler = CommandHandler('seedlingtimer', seedlingtimer)
dispatcher.add_handler(seedlingtimer_handler)

pump_handler = CommandHandler('pump', pump)
dispatcher.add_handler(pump_handler)

air_handler = CommandHandler('air', air)
dispatcher.add_handler(air_handler)

led_handler = CommandHandler('led', led)
dispatcher.add_handler(led_handler)

uv_handler = CommandHandler('uv', uv)
dispatcher.add_handler(uv_handler)

seedling_handler = CommandHandler('seedling', seedling)
dispatcher.add_handler(seedling_handler)

#image_handler = CommandHandler('image', image)
#dispatcher.add_handler(image)