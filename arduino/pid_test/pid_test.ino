#include <PID_v1.h>

#define motorLBA 4  // Control pin 1 for motor 1 sol geri
#define motorLFA 5  // Control pin 2 for motor 1 sol ileri
#define motorRFA 6  // Control pin 1 for motor 2 sag ileri
#define motorRBA 7  // Control pin 2 for motor 2 sag geri

volatile int hitsRight = 0;
volatile int hitsLeft = 0;
int var1, var2;
int raspMessage,roundDirection,var, zot, temp1, temp2; 
double SetPoint1, SetPoint2, SetPoint3, SetPoint4;
double Input1, Input2, Input3, Input4;
double  Output1, Output2, Output3, Output4;
int encoderDifference; 
PID myPIDStraight1(&Input1, &Output1, &SetPoint1, 5, 80, 40, DIRECT);
PID myPIDStraight2(&Input2, &Output2, &SetPoint2, 5, 80, 40, DIRECT);

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
  analogWrite(motorLFA, 125);
  analogWrite(motorRFA, 125);
  analogWrite(motorRBA, 0);
  myPIDStraight1.SetMode(AUTOMATIC); 
  myPIDStraight2.SetMode(AUTOMATIC); 
  Output1=125;
  Output2=125;
  }


void loop() {
 if (hitsLeft > hitsRight){
    myPIDStraight1.Compute();
    analogWrite(motorRBA, Output1);
    analogWrite(motorLFA, 125);
    Serial.print("LEFT:");
    Serial.print(hitsLeft);
    Serial.print(",");
    Serial.println("125");
    Serial.print("RIGHT::");
    Serial.print(hitsRight);
    Serial.print(",");
    Serial.println(Output1);
    Serial.println(" ");}
  else if (hitsRight > hitsLeft){
    myPIDStraight2.Compute();
    analogWrite(motorRBA, 125);
    analogWrite(motorLFA, Output2);
    Serial.print("LEFT:");
    Serial.print(hitsLeft);
    Serial.print(",");
    Serial.println(Output2);
    Serial.print("RIGHT::");
    Serial.print(hitsRight);
    Serial.print(",");
    Serial.println(125);
    Serial.println(" ");}
  else if (hitsLeft == hitsRight){
    analogWrite(motorRBA, Output1);
    analogWrite(motorLFA, Output2);
    Serial.print("LEFT:");
    Serial.print(hitsLeft);
    Serial.print(",");
    Serial.println(Output2);
    Serial.print("RIGHT::");
    Serial.print(hitsRight);
    Serial.print(",");
    Serial.println(Output1);
    Serial.println(" ");}
   delay(200);
  }

void countLeft()
{
 hitsLeft++;
}

void countRight()
{
 hitsRight++;
}

