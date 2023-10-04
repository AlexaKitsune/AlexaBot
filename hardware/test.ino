#include <Servo.h>

Servo myservo; // Crea un objeto de tipo Servo

void setup()
{
    myservo.attach(9); // Asigna el pin 9 al servo
                       // myservo.write(90);  // Lleva el servo a 90 grados
}

void loop()
{
    // El código dentro de loop() se ejecutará una sola vez y luego se detendrá

    eyePositions(0);
}

void eyePositions(int posY)
{
    int eyesYlimit = 25;
    if (posY > eyesYlimit) {
        posY = eyesYlimit;
    }
    if (posY < -eyesYlimit) {
        posY = -eyesYlimit;
    }
    myservo.write(posY + 90);
}

void jawsPosition(int pos)
{
    int adjust = 10;
    myservo.write(pos + adjust);
}

/*
#include <Servo.h>

Servo myservo;  // Crear un objeto de servo

void setup() {
  myservo.attach(9);  // Adjuntar el servo al pin 9
}

void loop() {
  // Girar en una dirección (sentido horario)
  myservo.write(90);  // Velocidad de giro 0 (detenido)
  delay(1000);

  // Girar en la dirección opuesta (antihorario)
  myservo.write(180);  // Velocidad de giro máxima en una dirección
  delay(1000);

  // Detener el giro
  myservo.write(90);
  delay(1000);
}*/
