#include <PID_v1.h>

#define motorRFA 7  // sag motor sari pin//sag ileri aktif
#define motorRBA 6  // sag motor siyah pin
#define motorLBA 5  // sol motor kirmizi pin
#define motorLFA 4  // sol motor siyah pin
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
long debouncing_time =100;
volatile unsigned long last_microsLeft, last_microsRight;
PID myPIDStraight1(&Input1, &Output1, &SetPoint1, 13 , 1, 0.5 , DIRECT);

void setup() {
  Serial.begin(9600);
  attachInterrupt(5, countLeft, CHANGE);
  attachInterrupt(4, countRight, CHANGE); 
  pinMode(0, INPUT);
  pinMode(1, INPUT);
  pinMode(motorLBA, OUTPUT);
  pinMode(motorLFA, OUTPUT);
  pinMode(motorRFA, OUTPUT);
  pinMode(motorRBA, OUTPUT);
  analogWrite(motorLBA, 0);
  analogWrite(motorLFA, 0);
  analogWrite(motorRFA, 0);
  analogWrite(motorRBA, 0);
  //delay(1000);
  SetPoint1=0;  
  Output1=0;

  myPIDStraight1.SetMode(AUTOMATIC);
  myPIDStraight1.SetOutputLimits(-90,90);

  }


void loop() { 
   while (true){
     if(raspRX()==7)
           break; }
  analogWrite(motorLFA, motorSpeed);
  analogWrite(motorRFA, motorSpeed);
  
  while(hitsLeft<100 || hitsRight<100) {
 //analogWrite(motorLFA, motorSpeed); 
 Input1=hitsLeft-hitsRight;
 myPIDStraight1.Compute();
 analogWrite(motorRFA, motorSpeed-Output1);
  Serial.println(int(hitsLeft));
  Serial.println(int(hitsRight));
  Serial.println(int(Output1));
  //Serial.print(motorSpeed-Output1);
  Serial.println(int(Input1));
  delay(500);
  }
  analogWrite(motorLFA, 0);
  analogWrite(motorRFA, 0); 
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
   
int raspRX() {
  while (true){
  if(Serial.available()>0){
       zot = (int) Serial.read();
       return(zot);
       } } }
