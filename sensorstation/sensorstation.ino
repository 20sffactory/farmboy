//#include <string>
#include <ArduinoSort.h>
#include <ArduinoJson.h>
#include <TimeLib.h>
#include <DHT.h>

#include <OneWire.h>
#include <DallasTemperature.h>

bool running = false;

//pins declaration
int airTempPin = 26;
int resTempPin = 25;//pin num //dont use D0
int resLevTrigPin = 22;//digital pin num
int resLevEchoPin = 23;//digital pin num
int resPhPin = A6;//////;//analog pin num
int resEcPin = A4;//analog pin number
int leakPin = A0;//analog pin number
int lightPin = A3; //analog pin number

//global variables
int sampleSize = 10;

//resTemp variables
OneWire oneWire(resTempPin);
DallasTemperature sensors(&oneWire);

//extTemp variables
#define DHTTYPE DHT11
DHT dht(airTempPin, DHTTYPE);

//resEc variables
//kValue is TDS calibration value/ TDS sensor reading
float kValue = 1.4;
float voltRef = 5.0;
float temperature = 0.0;

//resPh variables
//float phOffset = 0.0;

void setup() {
  //setup serial baud rate
  Serial.begin(115200);
  //sr04 init
  pinMode(resLevTrigPin, OUTPUT);
  pinMode(resLevEchoPin, INPUT);
  //tds init
  //  pinMode(resTdsPin, INPUT);
  //ds18b20 init
  sensors.begin();
  //dht11 init  
  dht.begin();
}

float getTemp() {
  sensors.setWaitForConversion(false);
  sensors.requestTemperatures();
  delay(750);
  float celcius = sensors.getTempCByIndex(0);
  temperature = celcius;
  return celcius;
}

float getAirHumidity() {
  float airHumidity = dht.readHumidity();
  return airHumidity;
}

float getAirTemperature() {
  float airTemperature = dht.readTemperature();
  return airTemperature;
}

float getWaterLevel() {
  //output distance in cm
  float waterLevelArray[sampleSize];
  for (byte i = 0; i < sampleSize; i++) {
    digitalWrite(resLevTrigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(resLevTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(resLevTrigPin, LOW);
    long duration = pulseIn(resLevEchoPin, HIGH);
    float distance = duration * 0.0343 / 2;
    waterLevelArray[i] = distance;
    delayMicroseconds(5000);
  }
  float waterLevelMedian = findMedian(waterLevelArray, sampleSize);
  return waterLevelMedian;
}

float getEC() {

//read into sample array
  float ecArray[sampleSize];
  for (byte i = 0; i<sampleSize; i++) {
    ecArray[i] = analogRead(resEcPin);
    delayMicroseconds(5000);
  }
  float ecMedian = findMedian(ecArray, sampleSize);
// read the analog value more stable by the median filtering algorithm, and convert to voltage value
  float averageVoltage = ecMedian * voltRef / 1024.0;
//  temperature compensation formula:
  float compensationCoefficient = 1.0+0.02*(temperature-25.0);
//temperature compensation
  float compensationVoltage = averageVoltage/compensationCoefficient;
//convert voltage value to ec value
//  float ecValue = (133.42*compensationVoltage*compensationVoltage*compensationVoltage - 255.86*compensationVoltage*compensationVoltage + 857.39*compensationVoltage)*kValue;
  return compensationVoltage;
  }

float getPhVal() {
  float phArray[sampleSize];
  for (byte i = 0; i<sampleSize; i++) {
    phArray[i] = analogRead(resPhPin);
    delayMicroseconds(500);
  }
  float phMedian = findMedian(phArray, sampleSize);
  float phValue=phMedian*5.0/1024/6;
  phValue = 3.5*phValue;//+phOffset;
  //return phValue;
  
}

int getLeakValue() {
  //output binary check leak
  float leakArray[sampleSize];
  for (byte i = 0; i < sampleSize; i++) {
    leakArray[i] = analogRead(leakPin);
    delayMicroseconds(100);
  }
  float leakMedian = findMedian(leakArray, sampleSize);
  int leakValue;
  //1 means leak, 0 means no leak
  if (leakMedian > 600.0) {
    leakValue = 0;
  } else {
    leakValue = 1;
  }
  return leakValue;
}

float getLightValue() {
  float lightArray[sampleSize];
  for (byte i = 0; i < sampleSize; i++) {
    int light = analogRead(lightPin);
    lightArray[i] = (float) light;
    delayMicroseconds(100);
  }
  int lightMedian = findMedian(lightArray, sampleSize);
  return lightMedian;
}

float findMedian(float dataList[], int count) {
  sortArray(dataList, count);
  //check even and return median
  if (count % 2 != 0) {
    return (float)dataList[count / 2];
  }
  return (float)(dataList[(count - 1) / 2] + dataList[count / 2]) / 2.0;
}

void writeJsonSensor() {
  StaticJsonDocument<512> doc;
  JsonObject object = doc.to<JsonObject>();
  object["idtime"] = now();
  object["temp"] = getTemp();
  object["airhumid"] = getAirHumidity();
  object["airtemp"] = getAirTemperature();
  object["level"] = getWaterLevel();
  object["ph"] = getPhVal();
  object["ecv"] = getEC();
  object["leak"] = getLeakValue();
  object["light"] = getLightValue();
  serializeJson(doc, Serial);
  Serial.print("\n");
}

void loop() {
  if (Serial.available() > 0) {
    switch(Serial.read()) {
      case '1':
        running = true;
        break;
    }
  }
  if (running) {
      writeJsonSensor();
  }
}
