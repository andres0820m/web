
int data=0;
void setup () {
   
   Serial.begin(9600); //Inicializo el puerto serial a 9600 baudios
}

void loop () {
   if(Serial.available())
   {
    delay(100);
    char a=Serial.read();
    if (a=='a')
    
    Serial.println(pot());
    
    
    }
     
   }
int pot()
{
  int data = analogRead(A0);
  return data;
  }

 int readTemp() {  // get the temperature and convert it to celsius
  int temp;
  temp = analogRead(A0);
  return temp * 0.48828125;
}
