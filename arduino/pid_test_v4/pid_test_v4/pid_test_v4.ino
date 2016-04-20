#include <PID_v1.h>

#define motorRFA 4  // Control pin 1 for motor 1 sol geri
#define motorRBA 5  // Control pin 2 for motor 1 sol ileri
#define motorLFA 6  // Control pin 1 for motor 2 sag ileri
#define motorLBA 7  // Control pin 2 for motor 2 sag geri
#define motorSpeed 125

volatile int hitsRight = 0;
volatile int hitsLeft = 0;
int var1, var2;
int raspMessage,roundDirection,var, zot, temp1, temp2; 
double SetPoint1, SetPoint2, SetPoint3, SetPoint4;
double Input1, Input2, Input3, Input4;
double  Output1, Output2, Output3, Output4;
int encoderDifference; 
int motorSpeedLast;
long debouncing_time =10;
volatile unsigned long last_microsLeft, last_microsRight;
PID myPIDStraight1(&Input1, &Output1, &SetPoint1, 13 , 0.2, 0.5 , DIRECT);

void setup() {
  Serial.begin(9600);
  attachInterrupt(4, countLeft, CHANGE);
  attachInterrupt(5, countRight, CHANGE); 
  pinMode(0, INPUT);
  pinMode(1, INPUT);
  pinMode(motorLBA, OUTPUT);
  pinMode(motorLFA, OUTPUT);
  pinMode(motorRFA, OUTPUT);
  pinMode(motorRBA, OUTPUT);
  analogWrite(motorLBA, 0);
  analogWrite(motorLFA, motorSpeed);
  analogWrite(motorRFA, motorSpeed);
  analogWrite(motorRBA, 0);
  //delay(1000);
  SetPoint1=0;  
  Output1=0;

  myPIDStraight1.SetMode(AUTOMATIC);
  myPIDStraight1.SetOutputLimits(-90,90);

  }


void loop() { 
 //analogWrite(motorLFA, motorSpeed); 
 Input1=hitsLeft-hitsRight;
 myPIDStraight1.Compute();
 analogWrite(motorRFA, motorSpeed-Output1);
 
 

  Serial.print(hitsLeft);
  Serial.print(",");
  Serial.print(hitsRight);
  Serial.print(",");
  Serial.print(Output1);
  Serial.print(",");
  Serial.println(Input1);
  delay(500);
  }

void countLeft()
{
  if((long)(micros()-last_microsLeft)>=debouncing_time*1000) {
  InterruptLeft();
  last_microsLeft=micros(); }
}
void InterruptLeft() {
   hitsLeft++; }

void countRight()
{
  if((long)(micros()-last_microsRight)>=debouncing_time*1000) {
  InterruptRight();
  last_microsRight=micros(); }
}
void InterruptRight() {
   hitsRight++; }

