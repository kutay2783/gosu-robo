 
#define I1 3  // Control pin 1 for motor 1
#define I2 4  // Control pin 2 for motor 1
#define I3 5  // Control pin 1 for motor 2
#define I4 6  // Control pin 2 for motor 2

volatile int hits1 = 0;
volatile int hits2 = 0;
int pin = 18;
int pin2 = 19;
int pin3 = 22;
int led = 13;

char x;

void setup() {
  Serial.begin(9600);
  pinMode(pin, INPUT);
   pinMode(pin2, INPUT);
  pinMode(pin3, OUTPUT);
  // put your setup code here, to run once:
  attachInterrupt(4, count1, CHANGE);
  attachInterrupt(5, count2, CHANGE); 
 
    pinMode(I1, OUTPUT);
    pinMode(I2, OUTPUT);
    pinMode(I3, OUTPUT);
    pinMode(I4, OUTPUT);
     pinMode(led, OUTPUT);
  analogWrite(I1, 150);
  analogWrite(I4, 150);
  analogWrite(I3, 0);
  analogWrite(I2, 0);
   digitalWrite(pin3, HIGH);
   
  }


void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("Hits1=");
  Serial.print(hits1);
  Serial.print(',');
  //Serial.print(", Hits2=");
  Serial.print(hits2);
  Serial.println(',');

//  int val = digitalRead(18);
//  int val2 = digitalRead(19);
//  Serial.println(val);
//Serial.println(val2);
  count2();
  if (Serial.available() > 0)
    {x = (char) Serial.read();
     // Serial.println('asd');
    if(x=='0')
      digitalWrite(pin3, LOW);
      digitalWrite(led, LOW); 
      
    if(x=='1')
      {  analogWrite(I1, 0);
         analogWrite(I4, 0);
         digitalWrite(led, HIGH);  
      }
    }
  delay(500);
}

void count1()
{
 hits1++;
}

void count2()
{
 hits2++;
}

