// Copyright (c) 2023, Kacper Wieleba
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for private, non-commercial purposes only, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

const int leftSensorPin = A0; int LSP = 0;
const int centerLeftSensorPin = A1; int CLSP = 0;
const int centerRightSensorPin = A2; int CRSP = 0;
const int rightSensorPin = A3; int RSP = 0;

const int motorDirection1 = 7; int MD1 = 0;
const int motorDirection2 = 8; int MD2 = 0;
const int motorSpeed1 = 9; int MS1 = 0;
const int motorSpeed2 = 10; int MS2 = 0;

int deviationFromCenter() {
  int leftSensorValue = analogRead(A0);
  int rightSensorValue = analogRead(A3);
  int centerValue = (leftSensorValue + rightSensorValue) / 2;

  int deviation = (centerValue - leftSensorValue);

  return deviation; // feedback - deviation
}

void setup() {
  // pin configuration
  pinMode(leftSensorPin, INPUT);
  pinMode(centerLeftSensorPin, INPUT);
  pinMode(centerRightSensorPin, INPUT);
  pinMode(rightSensorPin, INPUT);

  pinMode(motorDirection1, OUTPUT);
  pinMode(motorDirection2, OUTPUT);
  pinMode(motorSpeed1, OUTPUT);
  pinMode(motorSpeed2, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // reacding values from sensors
  int LSP = analogRead(leftSensorPin);
  int CLSP = analogRead(centerLeftSensorPin);
  int CRSP = analogRead(centerRightSensorPin);
  int RSP = analogRead(rightSensorPin);
  
  int deviation = deviationFromCenter();
  Serial.print("Deviation: ");
  Serial.println(deviation);

  // P regulator
  int error = deviation/17;
  int Kp = 1;
  int speed = 45;
  int rightSpeed = (-speed + (error * Kp));
  int leftSpeed = (-speed - (error * Kp));

  if (leftSpeed < 0) {
    digitalWrite(motorDirection1, LOW);
    leftSpeed = abs(leftSpeed);
  } 
  else {
    digitalWrite(motorDirection1, HIGH);
  }

  if (rightSpeed < 0) {
    digitalWrite(motorDirection2, LOW);
    rightSpeed = abs(rightSpeed);
  } 
  else {
    digitalWrite(motorDirection2, HIGH);
  }

  analogWrite(motorSpeed1, leftSpeed);
  analogWrite(motorSpeed2, rightSpeed);

  // feedback in serial monitor
  Serial.print("Left sensor value: ");
  Serial.print(LSP);
  Serial.print(" | Center sensor value: ");
  Serial.print(CLSP);
  Serial.print(" | Right sensor value: ");
  Serial.print(CRSP);
  Serial.print(" | Fourth sensor value: ");
  Serial.print(RSP);
  Serial.println();
  
  delay(50);
}
