//#include <Wire.h>
//#include <SPI.h>
#include <LiquidCrystal_I2C.h>

#include "ikonki.h"

#define _DEBUG
#define _trans_ 9600
#define grczasurozgrz 120000

#define ktcSO 12   /// or ICSP-1
#define ktcCS 10
#define ktcSCK 13  /// or ICSP-3

#define enA 3
#define enB 2
#define enSW 4

#define przek1 5
#define przek2 6

unsigned long time = 0, termtime = 0, time1 = 0, time2 = 0, timerozgrz; 

double temp = 0, utemp = 60, tempi,tempmax;
byte rozgrz=0;

byte dtemp=2;
byte fan=0;
byte grzeje =0;
byte co_u=5;//, old_co_u=100;

const unsigned int mini_maksi[7][2]={{20,260},{2,20},{0,24},{0,59},{0,1},{0,1},{0,5}};
// temp<20;260> dttemp<2;20> godz<0;24> min<0;59> grz2<0;1> grz1<0;1> poz_enk<0;5>
// ale też                                                 yes/no<0;1> 

char sTemp[5], sCzas[3];

unsigned long czas = 0; 
byte ugodz = 0, umin = 30, usek = 15, dgodz = 0, dmin = 0;
byte rgodz , rmin , rsek;
unsigned int uczas, czass;
long rczas;

int en_Pos = 5;
//int old_en_Pos=1;
bool last_state, state_now;

int old_ival;
byte old_bval,oldg_bval=0, przywr = 0;
byte klik=0;
byte ustawia=0;

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 20 chars and 4 line display

void setup()  {
	
  pinMode(ktcCS, OUTPUT);
  pinMode(ktcSO, INPUT);
  pinMode(ktcSCK, OUTPUT);
  digitalWrite(ktcCS, HIGH);
  
    pinMode(przek1,OUTPUT);
    pinMode(przek2,OUTPUT);
    digitalWrite(przek1,HIGH);
    digitalWrite(przek2,HIGH);
  pinMode(enA, INPUT);
  pinMode(enB, INPUT);
  pinMode(enSW, INPUT);
  
	  attachInterrupt(digitalPinToInterrupt(enA), blinkA, LOW);  
	  attachInterrupt(digitalPinToInterrupt(enB), blinkB, LOW);  
 
  lcd.init();                      // initialize the lcd
  // Print a message to the LCD.
  lcd.backlight();
  lcd.createChar(0, plus_minus);
  lcd.createChar(1, zegare);
  lcd.createChar(2, termometr);
  lcd.createChar(3, celsiusSymbol);
//  lcd.createChar(4, fan1);
  lcd.createChar(4, grzalka);
  lcd.createChar(5, grzalka);
  lcd.createChar(6, vielebny);
    lcd.noBlink(); 
    lcd.noCursor();
	

  temp = (readThermocouple(temp));
  tempmax=temp;
    termtime = micros();
    time = millis(); 
    time1 = millis();
    time2 = millis();
  
    setMinMax(mini_maksi[6][0],mini_maksi[6][1]);
    uczas=gms_na_czas(ugodz,umin,usek);
    rczas=uczas;
    rczas_na_gms();
    uczas_na_gms();
    
 //	mn_wyswietl();
//   
#if defined(_DEBUG)
//    lcd.noBlink();
    Serial.begin(_trans_);
      Serial.println("----------TEST---------");
      Serial.println(temp);
      Serial.println("---- ---------------");

#endif    
//888888888888888888888  
}

void loop() {
  #if defined(_DEBUG)

  #endif    

if ((millis()-time)>500) { //112 za mało minimum 113
    time=millis();
    temp=readThermocouple(temp);	
    if (temp>tempmax) tempmax=temp;
  #if defined(_DEBUG)
	 // if (grzeje>0) {
	  {
		Serial.print(millis()); Serial.print("  ");
		Serial.print(" grz= ");       Serial.print(grzeje);
		Serial.print(" rozgrz= ");       Serial.print(rozgrz);
		Serial.print(" temp= "); Serial.print(temp);
    Serial.print(" temp max= "); Serial.print(tempmax); //Serial.print("    ");
    Serial.print(" tempi= "); Serial.print(tempi);
		Serial.print(" Troz+grczas= "); Serial.println(timerozgrz + grczasurozgrz);
	  }    
	#endif    
}
 

  mn_wyswietl();

//if (keyDown()|| keyUp()) {
  if (keyUp()) {
    klik=klik+1;
    if (klik>2) klik=0;
    switch (klik) {
      case 0:
        ustawia=0;
        if (en_Pos ==1) przywr=1;
        else przywr=0;
        en_Pos=co_u;
        break;
      case 1:
        ustawia=1;
          switch (co_u) {
            case 0:
              old_ival=utemp;
              en_Pos=old_ival;
              break;
            case 1:
              old_bval=dtemp;
              en_Pos=old_bval;
              break;
            case 2:
              old_bval=ugodz;
              en_Pos=old_bval;
              break;
            case 3:
              old_bval=umin;
              en_Pos=old_bval;
              break;
            case 4:
              old_bval=fan;
              en_Pos=old_bval;
              break;
            case 5:
              oldg_bval=grzeje;
              en_Pos=old_bval;
              break;
          }
        break;
      case 2:
        ustawia=2;
        setMinMax(mini_maksi[5][0],mini_maksi[5][1]);
        en_Pos=0;
        break;
    }
  }

 switch (ustawia) {
    case 0:
      setMinMax(mini_maksi[6][0],mini_maksi[6][1]);
 //     temp = (readThermocouple(temp)); ////////////////////////////////////////////////////////////
      //old_co_u=co_u;
      co_u=en_Pos;
      if (przywr==1) {
          switch (co_u) {
            case 0:
              utemp = old_ival;
              break;
            case 1:
              dtemp = old_bval;
              break;
            case 2:
              ugodz = old_bval;
              break;
            case 3:
              umin = old_bval;
              break;
            case 4:
              fan = old_bval;
              break;
            case 5:
//               grzeje = old_bval;
             break;
          }
      }
      else {
        grzeje=oldg_bval;
      }
      break;
    case 1:
      setMinMax(mini_maksi[co_u][0],mini_maksi[co_u][1]);
		switch (co_u) {
            case 0:
              utemp=en_Pos;        
              break;
            case 1:
              dtemp=en_Pos;
              break;
            case 2:
              ugodz=en_Pos;
              dgodz = ugodz - old_bval;
              break;
            case 3:
              umin=en_Pos;
              dmin = umin - old_bval;
              break;
            case 4:
              fan=en_Pos;
              if (fan==1) digitalWrite(przek2,LOW);
              else digitalWrite(przek2,HIGH);
              break;
            case 5:
              oldg_bval=en_Pos;
              break;
          }
      break;
    case 2:
      setMinMax(mini_maksi[5][0],mini_maksi[5][1]);
	    uczas=gms_na_czas(ugodz,umin,usek);
      rczas=uczas;
      rczas_na_gms();
      dgodz=0;
      dmin=0;
     mn_wyswietl();						//////////////////////---------------------------------
              if (oldg_bval==1) { 
                czass = millis();
                if (rczas<1) {
                  rczas=uczas;
                }
              }
      
      break;
  }
	
	if (grzeje==1) {
      rczas=uczas-((millis() -czass)/1000);
      rczas_na_gms();
// jeżeli różnica temp >=20 stC to jest rozgrzewanie
		if (rozgrz==0) {

		  if (temp>=(utemp-dtemp/2)) {
			digitalWrite(przek1,HIGH); // ===---> wyłącza grzałkę
		  }
		  else if (temp<utemp-dtemp) {
			digitalWrite(przek1,LOW);  // ===--->  włącza grzałkę
		  }

		  if ((utemp-temp)>19) {
			rozgrz=1;
			tempi=((utemp + temp)/2) -3; ////////////////////////==========================
			timerozgrz = millis();
		  }  
		}
		else {
			if (temp>tempi) {
	//          czas np. 2min zanim powtórnie włączy grzałkę
			  digitalWrite(przek1,HIGH);  // wyłącza grzałkę
			  if (millis() >(timerozgrz + grczasurozgrz)) {
				  rozgrz=0;
			  }  
	//          i timer na 2min
			}
		}
		
		if (rczas<0) {
			grzeje=0;
			oldg_bval=0;
			rczas=uczas;
			rczas_na_gms();
		}
	}
	else {
		digitalWrite(przek1,HIGH);  // ===---> wyłącza grzałkę
	}
/// if grzeje=0	

}
//==========================--------------------==================================

char * strTemp(int tempu) {
		sprintf(sTemp,"%4d",tempu);
	return sTemp;	
}	
char * strCzas( int czasunio) {
		sprintf(sCzas,"%2d",czasunio);
	return sCzas;	
}	

void mn_wyswietl() {
 lcd.setCursor(19,3);
  lcd.write(byte(6));

  lcd.setCursor(0,0);
  lcd.write(byte(2));
  lcd.print(strTemp(temp)); lcd.write(byte(3));lcd.print("/");
  
  lcd.print(kurs(co_u,0));
  lcd.print(strTemp(utemp)); lcd.write(byte(3));lcd.print(" ");

  lcd.write(byte(0));lcd.write(byte(2));//lcd.print(" ");
  lcd.print(kurs(co_u,1));
  lcd.print(strCzas(dtemp)); lcd.write(byte(3));

    lcd.setCursor(0,1);
    lcd.write(byte(1));
//wypisanie bieżącego czasu do czasu nastawionego 
    lcd.print(strCzas(rgodz)); lcd.print("h");
    lcd.print(strCzas(rmin));lcd.print("m");
    lcd.print(strCzas(rsek));lcd.print("s /");
    lcd.print(kurs(co_u,2));
	lcd.print(strCzas(ugodz));lcd.print("h");
    lcd.print(kurs(co_u,3));
    lcd.print(strCzas(umin));lcd.print("m");

  lcd.setCursor(0,2);
  lcd.write(byte(4));lcd.print("2");
  lcd.print(kurs(co_u,4));

  if (fan==0) lcd.print(" OFF  ");
  else lcd.print("  ON  ");

  lcd.write(byte(5));lcd.print(" ");
  lcd.print(kurs(co_u,5));

  if (oldg_bval==0) lcd.print(" OFF   ");
  else lcd.print("  ON   ");
  
  lcd.setCursor(0,3);
  if (ustawia==2) {
    lcd.print("Set?");
    if (en_Pos==0) {
        lcd.print(char(62)); lcd.print("Y N");
        przywr=0;
    }else {
        lcd.print(" Y");lcd.print(char(62)); lcd.print("N");
        przywr=1;
    }
  } else lcd.print("          "); 
} 

//-----------------------
char kurs(byte co_ust, byte poz) {
	if (co_ust==poz) {
		if (ustawia==1) return char(126); // '->'
		else return char(62);  //'>'
	} else return char(32);		// ' '
}

//=========================================================================
double readThermocouple(double tempu) {
  uint16_t v;
 
  digitalWrite(ktcCS, LOW);
  if ((micros()-termtime) >10) {
 	termtime = micros();
	  // Read in 16 bits,
	  //  15    = 0 always
	  //  14..2 = 0.25 degree counts MSB First
	  //  2     = 1 if thermocouple is open circuit  
	  //  1..0  = uninteresting status
	  
    	#if defined(_DEBUG)
    //    Serial.print("        jest w odcz temp"); Serial.println("");
      #endif 



	  v = shiftIn(ktcSO, ktcSCK, MSBFIRST);
	  v <<= 8;
	  v |= shiftIn(ktcSO, ktcSCK, MSBFIRST);
	  
    
	  digitalWrite(ktcCS, HIGH);
 	  if (v & 0x4)  {    
		// Bit 2 indicates if the thermocouple is disconnected
		//return NAN;     
		return -300;
	  }
    v >>= 3;      // The lower three bits (0,1,2) are discarded status bits
    	#if defined(_DEBUG)
  //      Serial.print("        jest w odcz temp "); Serial.println(v);
        #endif 
	 	  
  return v*0.25;     // The remaining bits are the number of 0.25 degree (C) counts

  }
  else return tempu;
}
//==================================================================

void blinkA() {
  if ((millis() - time) > 3) {
        en_Pos=en_Pos+1; 
  time = millis();
  }
}
void blinkB() {
  if ((millis() - time) > 3)  {
        en_Pos=en_Pos-1;
  time = millis();
  }
}
bool keyDown() {
  if ((millis()-time1) >3) {
     time1 = millis();
     state_now=!digitalRead(enSW);
      if(last_state == false && state_now == true){
          last_state = state_now;
          return true;
      }
      else{
          last_state = state_now;
          return false;
      }
  }
  else{
    return false;
  }
}
bool keyUp() {
  if ((millis()-time2) >3) {
      time2 = millis();
      state_now=!digitalRead(enSW);
      if(last_state == true && state_now == false){
          last_state = state_now;
          return true;
      }
      else{
          last_state = state_now;
          return false;
      }
  }
  else{
        return false;
  }
}

//==================================================================
void setMinMax(int Min, int Max) {
  if (en_Pos < Min) en_Pos = Max;
  if (en_Pos > Max) en_Pos = Min;
}
//==================================================================
void uczas_na_gms() {
unsigned int temp;
	ugodz = (uczas/3600);
	temp = uczas - (ugodz *3600);
	umin = (temp/60);
	usek = temp - (umin*60);
}
void rczas_na_gms() {
unsigned int temp;
	rgodz = (rczas/3600);
	temp = rczas - (rgodz *3600);
	rmin = (temp/60);
	rsek = temp - (rmin*60);
}
unsigned int gms_na_czas(byte g, byte m, byte s) {
	return (g*3600 + m*60 + s);
}
