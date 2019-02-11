#include <Servo.h>
#include <DueTimer.h>
float Kp=6.44;
float Ki=58.518;
float Ts=0.02;
int E1=0;
int E=0;
int Y1=0;
int y=0;
int lm35 = A1; 
int fanpin = 11;       // the pin where fan is
String sp1="";
String sp2="";
int tempMin = 20;   // the temperature to start the fan
int tempMax = 100;   // the maximum temperature when fan is at 100%
int ledPin =12;
int button_pin=11;
/////////////////// sensors and actuators
float temp=0; 
int led_status=0;
int button_status=0;
int light_buld=0;
int fan=0;
Servo Door;
int placer =0;
int Sp=0;
////////////////////////////
//the data frame of the esp1 goes like this: temp,light buld,place holder
//the data frame of the esp2 goes like this: fan,led status,door status 
////////////////////////////
void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial2.begin(115200);
  Door.attach(13);
  attachInterrupt(digitalPinToInterrupt(button_pin), StateButton, CHANGE);
  Timer1.attachInterrupt(controlpi).start(500000);
}


void loop() {
if(Serial1.available()>0)
 {
  char data = Serial1.read();
  Sp=heatData(data);
  }
 placerStatus();
 fan1(button_status);
 
}

void controlpi()
{ 
 if(button_status==1 && placer==1){
 temp=analogRead(lm35);
 temp =map(temp,0,1023,0,255);
 E = Sp - temp;
 y=255-((Ki*Ts*E1)-(Kp*E1)+(Kp*E)+Y1); // 0 turn on the mosfet 1 turn it off
 //Serial.println(y);
 if(y < 0) y = 0;
 if(y > 255) y =255;
 Y1 = y;
 E1=E;
 }else
 y=255; 
 }

int lmToAdc (int data)
{
  int adc=((data*0.01)*255)/5;
  return adc;
  }

void fan1(int on_off) {
  
  int temp = readTemp();     // get the temperature
  if(on_off==0)
  {
   if(temp  < tempMin) { // if temp is lower than minimum temp 
      fan = 0; // fan is not spinning 
      digitalWrite(fan, LOW); 
   } 
   if((temp  >= tempMin) && (temp <= tempMax)) { // if temperature is higher than minimum temp 
      fan = map(temp, tempMin, tempMax, 32, 255); // the actual speed of fan 
      analogWrite(fanpin, fan); // spin the fan at the fanSpeed speed 
   } 
   if(temp  <= tempMin) {        // if temp is higher than tempMax
     digitalWrite(ledPin, HIGH);  // turn on led 
     led_status=1;
   } else 
   {                    // else turn of led
     digitalWrite(ledPin, LOW); 
     led_status=0;
   }
}else
{
  fan=0;
  digitalWrite(fanpin,fan);
  }
       
}

int readTemp() {  // get the temperature and convert it to celsius
  temp = analogRead(lm35);
  return temp * 0.48828125;
}

void StateButton()
{
  if(button_status==0)
  button_status=1;
  else
  button_status=0;
  }

  int heatData(char data)
  {
    if(data=='0')
    return lmToAdc(40);
    if(data=='1')
    return lmToAdc(60);
    if(data=='2')
    return lmToAdc(80);
    if(data=='3')
    return lmToAdc(100);
    }

void placerStatus()
{
  placer = analogRead(A1);
  if(placer>300) // change this for the correct value
  placer=1;
  else
  placer =0;
  }
