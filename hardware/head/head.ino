const int dummy = 0;
const int eyesLimit = 30;
const int eyebrowLimit = 35;
#include <ArduinoJson.h>
#include <ServoEasing.hpp> // Usa startEaseTo para movimiento no bloqueante con ServoEasing

ServoEasing servoEyesX;
ServoEasing servoEyesY;
ServoEasing servoEyebrowL;
ServoEasing servoEyebrowR;
ServoEasing servoJaws;
ServoEasing servoEarL;
ServoEasing servoEarR;
ServoEasing servoNeckZ;

void setup() {
    // Asigna el pin y la posición inicial para cada servo y define la velocidad
    servoEyesX.attach(12, 90);
    servoEyesY.attach(11, 90);
    servoEyebrowL.attach(10);
    servoEyebrowR.attach(9);
    servoJaws.attach(8);
    servoEarL.attach(7);
    servoEarR.attach(6);
    servoNeckZ.attach(5);
    // Ajusta la velocidad según sea necesario
    servoEyesX.setSpeed(5);
    servoEyesY.setSpeed(5);
    servoEyebrowL.setSpeed(5);
    servoEyebrowR.setSpeed(5);
    servoJaws.setSpeed(5);
    servoEarL.setSpeed(10);
    servoEarR.setSpeed(10);
    servoNeckZ.setSpeed(5);
    // Define el tipo de movimiento
    servoEyesX.setEasingType(EASE_CUBIC_IN_OUT);
    servoEyesY.setEasingType(EASE_CUBIC_IN_OUT);
    servoEyebrowL.setEasingType(EASE_CUBIC_IN_OUT);
    servoEyebrowR.setEasingType(EASE_CUBIC_IN_OUT);
    servoJaws.setEasingType(EASE_CUBIC_IN_OUT);
    servoEarL.setEasingType(EASE_CUBIC_IN_OUT);
    servoEarR.setEasingType(EASE_CUBIC_IN_OUT);
    servoNeckZ.setEasingType(EASE_CUBIC_IN_OUT);

    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);
    eyePositions(servoEyesX, 0);
    eyePositions(servoEyesY, 0);
    servoNeckZ.startEaseTo(0+90, 40, START_UPDATE_BY_INTERRUPT);
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
        servoEarL.startEaseTo(ear_l, 100, START_UPDATE_BY_INTERRUPT);
        servoEarR.startEaseTo(180 - ear_r, 100, START_UPDATE_BY_INTERRUPT);
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

    if (doc.containsKey("neck_z")) {
      int neck_z = doc["neck_z"];
      servoNeckZ.startEaseTo(neck_z + 90, 40, START_UPDATE_BY_INTERRUPT);
      digitalWrite(13, HIGH);
    }
}

void eyePositions(ServoEasing &servoEyes, int pos) {
    int eyesLimit = 30;
    if (pos > eyesLimit) {
        pos = eyesLimit;
    }
    if (pos < -eyesLimit) {
        pos = -eyesLimit;
    }
    servoEyes.startEaseTo(pos + 90, 100, START_UPDATE_BY_INTERRUPT);
}

void eyebrowPositions(ServoEasing &servoEyebrow, int pos) {
    int eyebrowLimit = 35;
    if (pos > eyebrowLimit) {
        pos = eyebrowLimit;
    }
    if (pos < -eyebrowLimit) {
        pos = -eyebrowLimit;
    }
    servoEyebrow.startEaseTo(pos + 90, 100, START_UPDATE_BY_INTERRUPT);
}

void jawsPosition(int pos) {
    int jawsLimit = 45;
    int jawsTare = 8;
    if (pos > jawsLimit) {
        pos = jawsLimit;
    }
    servoJaws.startEaseTo(pos + jawsTare, 80, START_UPDATE_BY_INTERRUPT);
}

void neckPosition(ServoEasing servoNeck, int pos) {
    servoNeck.startEaseTo(pos + 90, 40, START_UPDATE_BY_INTERRUPT);
}