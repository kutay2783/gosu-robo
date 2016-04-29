 
#define motorLBA 4  // Control pin 1 for motor 1 sol geri
#define motorLFA 5  // Control pin 2 for motor 1 sol ileri
#define motorRFA 6  // Control pin 1 for motor 2 sag ileri
#define motorRBA 7  // Control pin 2 for motor 2 sag geri

volatile int hitsLeft = 0;
volatile int hitsRight = 0;
int analogLeft, analogRight;
void setup() {
  Serial.begin(9600);
  attachInterrupt(0, countLeft, CHANGE);
  attachInterrupt(1, countRight, CHANGE); 
  pinMode(0, INPUT);
  pinMode(1, INPUT);
  pinMode(motorLBA, OUTPUT);
  pinMode(motorLFA, OUTPUT);
  pinMode(motorRFA, OUTPUT);
  pinMode(motorRBA, OUTPUT);
  analogWrite(motorLBA, 0);
  analogWrite(motorLFA, 100);
  analogWrite(motorRFA, 100);
  analogWrite(motorRBA, 0);
  }


void loop() {
  Serial.print('(');
  Serial.print(hitsLeft);
  Serial.print(',');
  Serial.print(hitsRight);
  Serial.println(')');
  
  analogLeft=analogRead(0);
  analogRight=analogRead(1);
  Serial.print("analog readings are:");
  Serial.print(analogLeft);
  Serial.print(',');
  Serial.println(analogRight);
  delay(1000);
}

void countLeft()
{
 hitsLeft++;
}

void countRight()
{
 hitsRight++;
}

