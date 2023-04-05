
// deklaracja pinów dla czujników odbiciowych
const int leftSensorPin = A0; int LSP = 0;
const int centerLeftSensorPin = A1; int CLSP = 0;
const int centerRightSensorPin = A2; int CRSP = 0;
const int rightSensorPin = A3; int RSP = 0;

const int motorDirection1 = 7; int MD1 = 0;
const int motorDirection2 = 8; int MD2 = 0;
const int motorSpeed1 = 9; int MS1 = 0;
const int motorSpeed2 = 10; int MS2 = 0;

//const int buttonPin = 4;
//int buttonState = 0;
//int velOnOff = 0;

int deviationFromCenter() {
  int leftSensorValue = analogRead(A0); // odczyt wartości z lewego czujnika
  int rightSensorValue = analogRead(A3); // odczyt wartości z prawego czujnika
  int centerValue = (leftSensorValue + rightSensorValue) / 2; // środkowa wartość

  int deviation = (centerValue - leftSensorValue); // obliczenie odchylenia od lewego czujnika

  return deviation; // zwrócenie wartości odchylenia
}

void setup() {
  // konfiguracja pinów dla czujników odbiciowych jako wejścia analogowe
  pinMode(leftSensorPin, INPUT);
  pinMode(centerLeftSensorPin, INPUT);
  pinMode(centerRightSensorPin, INPUT);
  pinMode(rightSensorPin, INPUT);

  pinMode(motorDirection1, OUTPUT);
  pinMode(motorDirection2, OUTPUT);
  pinMode(motorSpeed1, OUTPUT);
  pinMode(motorSpeed2, OUTPUT);

//  pinMode(buttonPin, INPUT_PULLUP);
  // włączenie monitora portu szeregowego
  Serial.begin(9600);
}

void loop() {
  // odczyt wartości z czujników odbiciowych
  int LSP = analogRead(leftSensorPin);
  int CLSP = analogRead(centerLeftSensorPin);
  int CRSP = analogRead(centerRightSensorPin);
  int RSP = analogRead(rightSensorPin);

//  buttonState = digitalRead(buttonPin);
//  if (buttonState == HIGH){
//    velOnOff = 1;
//  }
//  else{
//    velOnOff = 0;
//  }
  
  int deviation = deviationFromCenter();
  Serial.print("Deviation: ");
  Serial.println(deviation);

  // wywołanie funkcji sterującej silnikami z regulatorem P
  int error = deviation/17;
  int Kp = 1; // wzmocnienie regulatora P
  int speed = 45; // prędkość obrotowa silników
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

  // wypisanie wartości na monitorze szeregowym
  Serial.print("Left sensor value: ");
  Serial.print(LSP);
  Serial.print(" | Center sensor value: ");
  Serial.print(CLSP);
  Serial.print(" | Right sensor value: ");
  Serial.print(CRSP);
  Serial.print(" | Fourth sensor value: ");
  Serial.print(RSP);
  Serial.println();

  // opóźnienie pomiędzy odczytami
  delay(10);
}
