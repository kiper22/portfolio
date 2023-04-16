#include <Wire.h>
#include <SoftwareSerial.h>
#include <LiquidCrystal_I2C.h>
#include "Ultrasonic.h"
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> 
#endif

LiquidCrystal_I2C lcd(0x27,16,2);
Ultrasonic ultrasonic(7);
Adafruit_NeoPixel pixels(8, 6, NEO_GRB + NEO_KHZ800);


/*
int LedCZERWONY(k){     pixels.setPixelColor(k, pixels.Color(255, 0, 0))     ;}
int LedZOLTY(k){        pixels.setPixelColor(k, pixels.Color(128, 128, 0))   ;}
int LedZIELONY(k){      pixels.setPixelColor(k, pixels.Color(0,255, 0))      ;}
int LedPUSTY(k){        pixels.setPixelColor(k, pixels.Color(0,0, 0))        ;}
*/
void setup()
{
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  pinMode(4,OUTPUT);
  pinMode(2,OUTPUT);
  digitalWrite(2,HIGH);
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  pixels.begin();
}
void loop()
{

  int RangeInCentimeters;
  RangeInCentimeters = ultrasonic.MeasureInCentimeters();
 
  lcd.setCursor(0,0);
  lcd.print("The distance:");
  lcd.setCursor(0,1) ;
  
  if(RangeInCentimeters<151){
    lcd.print(RangeInCentimeters,DEC);
    lcd.setCursor(5,1) ;
    lcd.print("cm");
    }
    else{
     lcd.print("more than 150cm");
     }
     
  delay(150);
  
  Buzzer(RangeInCentimeters);
    LEDY(RangeInCentimeters);
  lcd.clear();
  pixels.clear();
}
int Buzzer(int k){
  if(k<20){
    digitalWrite(4,HIGH);
    }
    else{
     digitalWrite(4,LOW);
      }
}

int LedPUSTY(int k){        pixels.setPixelColor(k, pixels.Color(0,0, 0))        ;}
int LEDY(int c1){

    for (int c2=0;c2<8;c2++){
      LedPUSTY(c2);
    }
    
  if(c1<=90){pixels.setPixelColor(7, pixels.Color(0,255, 0));}
  if(c1<=80){pixels.setPixelColor(6, pixels.Color(0,255, 0));}
  if(c1<=70){pixels.setPixelColor(5, pixels.Color(0,255, 0));}
  if(c1<=60){pixels.setPixelColor(4, pixels.Color(128, 128, 0));}  
  if(c1<=50){pixels.setPixelColor(3, pixels.Color(128, 128, 0));}
  if(c1<=40){pixels.setPixelColor(2, pixels.Color(255, 0, 0));}
  if(c1<=30){pixels.setPixelColor(1, pixels.Color(255, 0, 0));}
  if(c1<=20){pixels.setPixelColor(0, pixels.Color(255, 0, 0));}
  
  pixels.show();  
}
