 
#define I1 4  // Control pin 1 for motor 1 sol geri
#define I2 5  // Control pin 2 for motor 1 sol ileri
#define I3 6  // Control pin 1 for motor 2 sag ileri
#define I4 7  // Control pin 2 for motor 2 sag geri

volatile int hits1 = 0;
volatile int hits2 = 0;
int var1, var2;
void setup() {
  Serial.begin(9600);
  attachInterrupt(4, count1, CHANGE);
  attachInterrupt(5, count2, CHANGE); 
  pinMode(0, INPUT);
  pinMode(1, INPUT);
  pinMode(I1, OUTPUT);
  pinMode(I2, OUTPUT);
  pinMode(I3, OUTPUT);
  pinMode(I4, OUTPUT);
  analogWrite(I1, 0);
  analogWrite(I2, 0);
  analogWrite(I3, 0);
  analogWrite(I4, 100);
  }


void loop() {
  Serial.print('(');
  Serial.print(hits1);
  Serial.print(',');
  Serial.print(hits2);
  Serial.println(')');
  
  var1=analogRead(0);
  var2=analogRead(1);
  Serial.print("analog readings are:");
  Serial.print(var1);
  Serial.print(',');
  Serial.println(var2);
  delay(1000);
}

void count1()
{
 hits1++;
}

void count2()
{
 hits2++;
}

