# farmboy
A modularised computer to monitor, control and automate hydroponics systems

This project is a work in progress. New functions are being added everyday. 
Discussions and updates are available here:
https://www.facebook.com/groups/1916953951765449/

Understanding of how a hydroponics system work in theory is highly recommended for anyone intending to enter this project.
This project also involves wiring of multiple AC devices, which can cause harm and kill without proper knowledge, please make precautions and know the risk.

Key Functions (as of 22Apr19):
SQLite Database to store sensor data median value per defined interval
Telegram Chatbot for remote control via mobile
  - status of real time data
  - status of run state of all equipments
  - pause/continue pump timer
  - manual on/off for LEDs, Water Pump, Air Pump, UV sanitizer
  - warning texts if leakage is detected

Computer Hardware List:
Mega2560
Mega2560 Sensor Shield
Raspberry Pi 3B+
8 Channel Relay Module
12V3A PSU
PSU Fused Switch
4 Channel Screw Terminal
TFT LCD Touch Screen for Raspberry Pi

Arduino Sensors involved:
DS18B20 - water temperature
SR04 - water level readings
CHT11 - air temperature and humidity
SEN0244 - tds/ec readings
SEN0161 - pH readings
GL5528 - light dependent resistor
RainSensor - leakage detection
