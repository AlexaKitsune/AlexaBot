const int dummy = 0;
#include <ArduinoJson.h>
#include <Servo.h>

Servo servoEyesX; // Crea un objeto de tipo Servo
Servo servoEyesY;
Servo servoEyebrowL;
Servo servoEyebrowR;
Servo servoJaws;
Servo servoEarL;
Servo servoEarR;
Servo servoNeckZ;

void setup() {
  servoEyesX.attach(12); // Asigna el pin 8 al servo
  servoEyesY.attach(11);
  servoEyebrowL.attach(10);
  servoEyebrowR.attach(9);
  servoJaws.attach(8);
  servoEarL.attach(7);
  servoEarR.attach(6);
  servoNeckZ.attach(5);
  
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  eyePositions(servoEyesX, 0);
  eyePositions(servoEyesY, 0);
  neckPosition(0);
  jawsPosition(0);
  Serial.begin(9600);
  Serial.setTimeout(250);
}

void loop() {
  while (Serial.available() == 0);
  String strJson = Serial.readStringUntil('\n');
  Serial.println(strJson);
  processJson(strJson);
}

// FUNCTIONS:

void processJson(String jsonStr) {
  DynamicJsonDocument doc(512);  // Tamaño del documento JSON (ajustar según sea necesario)
  DeserializationError error = deserializeJson(doc, jsonStr);

  if (error) {
    Serial.println("Error al analizar JSON");
    return;
  }

  if (doc.containsKey("READY")) {
    int isReady = doc["READY"];
    if(isReady == 1){
      digitalWrite(13, HIGH);
      delay(10);
    }
  }

  // Verificar si los campos "difference_x" y "difference_y" existen en el JSON
  if (doc.containsKey("difference_x") && doc.containsKey("difference_y")) {
    int difference_x = doc["difference_x"];
    int difference_y = doc["difference_y"];

    eyePositions(servoEyesX, difference_x);
    eyePositions(servoEyesY, difference_y);
    digitalWrite(13, HIGH);
  }

  if (doc.containsKey("eyebrow_l") && doc.containsKey("eyebrow_r")) {
    int eyebrow_l = doc["eyebrow_l"];
    int eyebrow_r = doc["eyebrow_r"];

    eyebrowPositions(servoEyebrowL, eyebrow_l);
    eyebrowPositions(servoEyebrowR, eyebrow_r);
    digitalWrite(13, HIGH);
  }

  if (doc.containsKey("ear_l") && doc.containsKey("ear_r")) {
    int ear_l = doc["ear_l"];
    int ear_r = doc["ear_r"];

    servoEarL.write(ear_l);
    servoEarR.write(180 - ear_r);
    digitalWrite(13, HIGH);
  }

  if (doc.containsKey("tts_tokens")) {
    String text = doc["tts_tokens"];
    int length = text.length();
    for (int i = 0; i < length; i++) {
      char letter = text.charAt(i);
      int val;
      if (letter == 'L') {
        val = 10;
      } else if (letter == 'M') {
        val = 25;
      } else if (letter == 'H') {
        val = 40;
      }
      Serial.println(val);
      jawsPosition(val);
      delay(225);
    }
    jawsPosition(0);
  }
}

bool isNumber(String str) {
  // Función para verificar si una cadena es un número válido
  for (int i = 0; i < str.length(); i++) {
    if (!isDigit(str.charAt(i))) {
      return false;
    }
  }
  return true;
}

void eyePositions(Servo servoEyes, int pos) {
  int eyesLimit = 30;
  if (pos > eyesLimit) {
    pos = eyesLimit;
  }
  if (pos < -eyesLimit) {
    pos = -eyesLimit;
  }
  servoEyes.write(pos + 90);
}

void eyebrowPositions(Servo servoEyebrow, int pos) {
  int eyebrowLimit = 35;
  if (pos > eyebrowLimit) {
    pos = eyebrowLimit;
  }
  if (pos < -eyebrowLimit) {
    pos = -eyebrowLimit;
  }
  servoEyebrow.write(pos + 90);
}

void jawsPosition(int pos) {
  int jawsLimit = 45;
  int jawsTare = 8;

  if (pos > jawsLimit) {
    pos = jawsLimit;
  }

  servoJaws.write(pos + jawsTare);
}

void neckPosition(int pos){
  servoNeckZ.write(pos + 90);
}
