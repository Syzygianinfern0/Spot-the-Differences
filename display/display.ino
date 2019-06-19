/*
Author Name : S P Sharan
Domain: Tronix
Sub-Domain: Signal Processing & ML

Functions: 
      dlay()    - Create a small delay
      disp()    - Displays the corresponding matrix leds
      init()    - Init registers for data and timer
      
Global Variables: 
      pos[6][6] - Placeholder for the matrix LEDs
      d         - Done Status
      k         - For the timer
*/
 
#include <avr/io.h>
#include <avr/interrupt.h>

volatile int k = 0;
int pos[6][6] = {1, 1, 0, 0, 0, 0,
                 0, 1, 0, 0, 0, 0,
                 0, 0, 1, 0, 0, 0,
                 0, 0, 0, 1, 0, 0,
                 0, 0, 0, 0, 1, 0,
                 0, 0, 0, 0, 0, 1};

ISR(TIMER0_OVF_vect)    //Triggered When Overflow Occours
{
  ++k;
}

/*
 * Delay for 1 overflow of the timer 0
 * without prescaling
 * Example Call : dlay();
 */
void dlay()
{
  k = 0;
  TCCR0B = 1 << CS00;   // No Prescaler
  while (k <= 1);       // Wait for 1 Overflow from ISR
  TCCR0B = 0;           // Reset the counter
}

/*
 * Turns on the each required LED for 1 overflow and Turns off again
 * Example Call : disp();
 */
void disp()
{
  for (int i = 0; i < 6; i++)
  {
    for (int j = 0; j < 6; j++)
    {
      if (pos[i][j] == 1)
      {
        PORTD = 1 << (2 + j);
        PORTB = 0xFF ^ (1 << i);
        dlay();
        PORTD = 0;
        PORTB = 0xFF;
        dlay();
      }
    }
  }
}


void init()
{
  Serial.begin(9600);   // Start the Serial Communication
  TIMSK0 = 1 << TOIE0;  // Enable Overflow Interrupt
  DDRD = 0b11111100;    // + terminal of LEDs to be connected to D2-D7 
  DDRB = 0xFF;          // - terminal of LEDs to be connected to B0-B5
  PORTB = 0xFF;         // Keeps the LEDs off
  PORTD = 0;
  sei();                // Enable Interrupts
}

int d = 0;              // Done 

int main(void)
{
  init();
  while (1) 
  {
    if(d)                                 // If signal was recieved, display forever
      while(1)
        disp();
    if (Serial.available())               // If buffer present/communication attempt
    {
      for ( int i = 0 ; i < 6 ; ++i )
        for ( int j = 0 ; j < 6 ; ++j )
          pos[i][j] = Serial.read();      // Fill in the matrix with the recieved info
      d = 1;
    }
    Serial.println("############");       // Display the current status of the done
    Serial.println(d);
    Serial.println("############");       // Display the current status of the matrix
    for ( int i = 0 ; i < 6 ; ++i )
      for ( int j = 0 ; j < 6 ; ++j )
        Serial.println(pos[i][j]);

  }
}
