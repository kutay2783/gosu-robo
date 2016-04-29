#include <TimerThree.h>
#include <TimerOne.h>
#include <PID_v1.h>

 

#define enablePin  52 
#define encoderRight  18
#define encoderLeft 19
#define controlLed 13
#define echoPin 30
#define trigPin 31
#define led1 52
#define led2 53
#define led3 54
#define led4 55
#define motorLBA 4  // sag motor sari pin//sag ileri aktif
#define motorLFA 5  // sag motor siyah pin
#define motorRFA 6  // sol motor kirmizi pin
#define motorA 7  // sol motor siyah pin

volatile int hitsRight = 0;
volatile int hitsLeft = 0;
long distance;
int raspMessage,roundDirection,var, zot, temp1, temp2; 
double SetPoint1, SetPoint2, SetPoint3, SetPoint4;
double Input1, Input2, Input3, Input4;
double  Output1, Output2, Output3, Output4;
int encoderDifference; 

PID myPIDStraight1(&Input1, &Output1, &SetPoint1, 15, 80, 40, DIRECT);
PID myPIDStraight2(&Input2, &Output2, &SetPoint2, 15, 80, 40, DIRECT);
PID myPIDround1(&Input3, &Output3, &SetPoint3, 15, 80, 40, DIRECT);
PID myPIDround2(&Input2, &Output2, &SetPoint4, 15, 80, 40, DIRECT);
void setup() {
  Serial.begin(9600);
  Timer1.initialize();
  Timer3.initialize();
  Timer1.attachInterrupt(enabLeft,  75000);
  Timer3.attachInterrupt(enabRight, 75000);
  pinMode(encoderRight, INPUT);
  pinMode(encoderLeft, INPUT);
  pinMode(controlLed, OUTPUT);
  attachInterrupt(4, incLeft, CHANGE);
  attachInterrupt(5, incRight, CHANGE); 
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  digitalWrite(controlLed, LOW);
  digitalWrite (trigPin,LOW);
  
  SetPoint1=1;  SetPoint2=1;  SetPoint3=1;  SetPoint4=1;
  myPIDStraight1.SetMode(AUTOMATIC); 
  myPIDStraight2.SetMode(AUTOMATIC); 
  myPIDround1.SetMode(AUTOMATIC); 
  myPIDround2.SetMode(AUTOMATIC);   
 
  }

void loop() {

   while (true){
     if(raspRX()==1)
           break;     
  }
   raspTX(2);
   //while (true){
   //if(Serial.available ()>0){
    //  raspMessage = (int) Serial.read();
     // switch (raspMessage){
        switch (raspRX()){
        case 5:  roundAroundCW();
        case 6:  roundAroundCCW();
        case 7:  goStraight();
        case 8:  incRightRasp();
        case 9:  incLeftRasp();
        case 10: returnHits();
        //}
    //} 
  }
}
void roundAroundCW (){
  //digitalWrite(controlLed, HIGH);
  raspTX(20);
  temp1=raspRX();
  if(temp1==0)
    digitalWrite(controlLed, LOW);
  delay(2);
  raspTX(21);
  delay(200);
 
  temp2=raspRX();
/*    if(temp2==9) {
    analogWrite(motorRBA, 150);
    analogWrite(motorLFA, 150);
    digitalWrite(controlLed, HIGH);
    analogWrite(motorRBA, 150); }
    delay(1000);
    digitalWrite(controlLed, LOW);
    delay(1000);
    digitalWrite(controlLed, HIGH);
    delay(1000);
    digitalWrite(controlLed, LOW);
    delay(1000);
    digitalWrite(controlLed, HIGH);
  analogWrite(motorRBA, 125);
  analogWrite(motorLFA, 125);
  delay(5000);
  digitalWrite(controlLed, LOW);*/
  var=temp1*250+temp2;
  
  hitsLeft=0;
  hitsRight=0;
 
  Input1 = hitsLeft - hitsRight ;
  Input2 = hitsRight - hitsLeft ;  
  analogWrite(motorRBA, 175);//sag kirmizi
  analogWrite(motorLBA, 175);//sol siyah
  while(hitsLeft<var || hitsRight<var){  /*  
  if (hitsLeft > hitsRight){
    myPIDround1.Compute();
    analogWrite(motorRBA, Output3);
    analogWrite(motorLFA, 125);}
  if (hitsRight > hitsLeft){
    myPIDround2.Compute();
    analogWrite(motorRBA, 125);
    analogWrite(motorLFA, Output4);}
  if (hitsLeft == hitsRight){
    analogWrite(motorRBA, Output3);
    analogWrite(motorLFA, Output4);} */
  //Serial.print('(');
  //Serial.print(hitsRight);
  //Serial.print(',');
  //Serial.print(hitsLeft);
  //Serial.println(')');
    }
  analogWrite(motorRBA, 0);
  raspTX(3);
  analogWrite(motorLFA, 0);
  }
  
  void roundAroundCCW (){
  raspTX(2);
  temp1=raspRX();
  raspTX(2);
  temp2=raspRX();
  var=temp1*250+temp2;
  
  hitsLeft=0;
  hitsRight=0;
  Input1 = hitsLeft  -  hitsRight ;
  Input2 = hitsRight - hitsLeft ;  
  analogWrite(motorRBA, 125);//sag kirmizi
  analogWrite(motorLFA, 125);//sol siyah
  delay(2000);
  while(hitsLeft<var || hitsRight<var){    
    if (hitsLeft > hitsRight){
        myPIDround1.Compute();
        analogWrite(motorRFA, Output3);
        analogWrite(motorLBA, 125);}
    if (hitsRight > hitsLeft){
        myPIDround2.Compute();
        analogWrite(motorRFA, 125);
        analogWrite(motorLBA, Output4);}
    if (hitsLeft == hitsRight){
        analogWrite(motorRFA, Output3);
        analogWrite(motorLBA, Output4);}
    }
  raspTX(3);
  }
  
void goStraight(){
  raspTX(3);
  delay(2000);
  analogWrite(motorRFA, 125);
  temp1=raspRX();
  analogWrite(motorLFA, 125);
  delay(2000);
  raspTX(4);
  //temp2=raspRX();
  //var=temp1*250+temp2;
  
  //hitsLeft=0;
  //hitsRight=0;
  //Input3 = hitsLeft - hitsRight ;
  //Input4 = hitsRight - hitsLeft ; 
  analogWrite(motorRFA, 125);
  analogWrite(motorLFA, 125);
  while(hitsLeft<1000 || hitsRight<1000){    
     if (hitsLeft > hitsRight){
        myPIDStraight1.Compute();
        analogWrite(motorRFA, Output3);
        analogWrite(motorLFA, 125);}
    if (hitsRight > hitsLeft){
        myPIDStraight2.Compute();
        analogWrite(motorRFA, 125);
        analogWrite(motorLFA, Output4);}
    if (hitsLeft == hitsRight){
        analogWrite(motorRFA, Output3);
        analogWrite(motorLFA, Output4);}
    digitalWrite (trigPin,HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    distance=pulseIn(echoPin,HIGH);
    distance=distance/58.2;
    if(distance>0 && distance<3){
        raspTX(4);
        break;
      }
    }
  if(!(distance>0 && distance<3))  
     raspTX(3);
  }
  
  
void returnHits() {
  raspTX(2);
  delay(2);
  raspTX((hitsLeft+hitsRight)/500);
  delay(2);
  raspTX((hitsLeft+hitsRight)%250);

}
void incLeftRasp(){
  raspTX(2);
  temp1=raspRX();
  hitsLeft=hitsLeft+temp1;
  raspTX(3);
}
void incRightRasp(){
  raspTX(2);
  temp1=raspRX();
  hitsRight=hitsRight+temp1;
  raspTX(3);
}

void incLeft()
{
 hitsLeft++;
 EIMSK &= ~(bit (INT2));
 TIMSK1 = _BV(TOIE1);
 
}

void incRight()
{
 hitsRight++;
 EIMSK &= ~(bit (INT3));
 TIMSK3 = _BV(TOIE1);
}

void enabLeft() {
  EIMSK |= (bit (INT2));
  Timer1.detachInterrupt();
  }
  
void enabRight() {
  EIMSK |= (bit (INT3));
  Timer3.detachInterrupt();
  }
  
int raspRX() {
  while (true){
  if(Serial.available()>0){
       zot = (int) Serial.read();
       return(zot);
       } } }
       
void raspTX(int z) {  
  Serial.println (z); }



