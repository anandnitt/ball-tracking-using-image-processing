 #include <avr/io.h>
 #include <avr/interrupt.h>
 int milli=0;

 void usart_int(void)
{
  UCSR0A=0x00;
  UCSR0B=(1<< RXEN0)|(1<< TXEN0);//TRANSMIT AND RECEIVE ENABLE
  UCSR0C=(1<<UCSZ01)|(1<<UCSZ00);//ASYNCHRONOUS, 8 BIT TRANSFER
  UBRR0L= 0x67 ; //BAUD RATE 9600
  
}


void usart_send(int ch )
{
  while(UCSR0A!=(UCSR0A|(1<<UDRE0)));//waiting for UDRE to become high
  UDR0= ch;
}
int main()
 {
  sei();
  OCR1A=250;
 usart_int();
   TCCR1B=(1<<WGM12)|(1<<CS11)|(1<<CS10);
    TIMSK1|=(1<<OCIE1A);
while(1)
{}
 
 }
 
 ISR(TIMER1_COMPA_vect)
{
  milli++;
  if(milli==2000)
  {
    usart_send('a');
    usart_send('a');
    milli=0;
    }
  }

    
