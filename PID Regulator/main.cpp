#include <avr/io.h>
#include <inttypes.h>

// Stałe regulatora PID wstawic 1.0 0.5 0.2
#define Kp 0.6
#define Ki 0.3
#define Kd 0.01

float i1, d1;

float error = 0;
float proportional = 0;
float integral = 0;
float max_integral = 100; // Maksymalna wartość całki do ograniczenia windupu
float min_integral = -100; // Minimalna wartość całki
float derivative = 0;
float max_derivative = 60; // ograniczenie na uchyb
float min_derivative = -60;
float dt = 0.1;
float last_error = 0;

int main(void)
{
	
	// port zadawanej prędkości obrotowej
	uint8_t predkosc_zadana = 242;
	PORTA = predkosc_zadana;
	
	// port do włączania i wyłączania I oraz D ustawiamy na włączone
	DDRA = _BV(0) | _BV(1);
	
	while (1){
		predkosc_zadana = PORTA;
		int predkosc_aktualna = PORTB;
		//predkosc_aktualna = predkosc_aktualna * 200 / 255;
		
		// obliczenia PID'a
		error = predkosc_zadana - predkosc_aktualna;
		proportional = Kp * error;
		
		// integral
		i1 = DDRA & _BV(0);
		if (i1 != 0){
			integral += Ki * error * dt;
			
			// ograniczenie windup'u
			if (integral > max_integral){
				integral = max_integral;
			}
			else if (integral < min_integral){
				integral = min_integral;
			}
		}
		else{
			integral = 0;
		}
		
		
		// derivative
		d1 = DDRA & _BV(1) ;
		if (d1 != 0){
			derivative = Kd * (error - last_error) / dt;
			
			// ograniczenie uchybu
			if (derivative > max_derivative){
				derivative = max_derivative;
			}
			else if (derivative < min_derivative){
				derivative = min_derivative;
			}
		}
		else {
			derivative = 0;
		}
		
		// predkosc aktualna po iteracji z PID'em
		predkosc_aktualna = predkosc_aktualna + proportional + integral + derivative;
		
		// sygnalizacji przesterowania DDRB
		// czyli wartość poza zakresem 0-255
		
		if (predkosc_aktualna > 255 || predkosc_aktualna < 0){
			PORTC=0b11111111;
		}
		else{
			PORTC=0x00;
		}
		
		PORTB = predkosc_aktualna;
		last_error = error;
		
	}
}
