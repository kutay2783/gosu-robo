

#include <PID_v1.h>
///////define parts/////////
#define enablePin  52
#define encoderRight  0
#define encoderLeft 1
#define controlLed 13
#define echoPin 30
#define trigPin 31

#define motorRFA 7 // sag motor sari pin//sag ileri aktif
#define motorRBA 6  // sag motor siyah pin
#define motorLBA 5  // sol motor kirmizi pin
#define motorLFA 4  // sol motor siyah pin
#define encRight 9
#define encLeft  8
#define motorSpeed 125
volatile int hitsRight = 0;
volatile int hitsLeft = 0;
long distance;
int raspMessage,roundDirection,var, zot, temp1, temp2,condition;
double SetPointStraight=0, SetPointRound=0;
double InputStraight, InputRound;
double  OutputStraight, OutputRound;
int encLeftValue,encRightValue;
int encoderDifference,motorSpeedLast=motorSpeed;
volatile unsigned long last_microsRight, last_microsLeft;
long debouncing_time =100;
PID myPIDStraight(&InputStraight, &OutputStraight, &SetPointStraight, 13,
1, 0.5, DIRECT);
PID myPIDRound(&InputRound, &OutputRound, &SetPointRound, 13, 1, 0.5,
DIRECT);

void setup() {
  Serial.begin(9600);
  /*pinMode(encoderRight, INPUT);        // analog read icin simdilik dursun!!
  pinMode(encoderLeft, INPUT);*/        // sistem basladiginda test edebilmekicin encoderleri
  pinMode(controlLed, OUTPUT);
  attachInterrupt(5, countLeft, CHANGE);
  attachInterrupt(4, countRight, CHANGE);
  pinMode(motorRFA, OUTPUT);
  pinMode(motorRBA, OUTPUT);
  pinMode(motorLBA, OUTPUT);
  pinMode(motorLFA, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  /*analogWrite(motorRFA, 0);
  analogWrite(motorRBA, 0);
  analogWrite(motorLBA, 0);
  analogWrite(motorLFA, 0);*/
  digitalWrite(controlLed, LOW);
  digitalWrite (trigPin,LOW);
  myPIDStraight.SetMode(AUTOMATIC);
  myPIDStraight.SetOutputLimits(-90,90);
  myPIDRound.SetOutputLimits(-90,90);
  }

void loop() {

   while (true){
     if(raspRX()==1)
           break; }
  raspTX(1);

    while (true){
      condition=raspRX();
      if      (condition==5 )  roundAroundCW();
      else if (condition==6 )  roundAroundCCW();
      else if (condition==7 )  goStraight();
      else if (condition==8 )  incRightRasp();
      else if (condition==9 )  incLeftRasp();
      else if (condition==10)  returnHits();        
     }
}
////////////Round CW///////////
void roundAroundCW (){
 myPIDRound.SetMode(AUTOMATIC);
  raspTX(20);
  temp1=raspRX();
  raspTX(21);
  temp2=raspRX();
  var=temp1*250+temp2;
  hitsLeft=0;
  hitsRight=0;
  encRightValue = analogRead(encRight);
  encLeftValue = analogRead(encLeft);
  if (encRightValue>300||encRightValue<700)
    hitsRight--;
  if (encLeftValue>300||encLeftValue<700)
    hitsLeft--;
  InputRound = hitsLeft - hitsRight ;
  analogWrite(motorRBA, 125);
  analogWrite(motorLFA, 125);
  digitalWrite(controlLed,HIGH);
  while((hitsLeft<var) &&  (hitsRight<var)){
    InputRound = hitsLeft - hitsRight ;
    myPIDRound.Compute();
    analogWrite(motorRBA, motorSpeed-OutputRound);
  }
  analogWrite(motorRBA, 0);
  raspTX(3);
  digitalWrite(controlLed,LOW);
  analogWrite(motorLFA, 0);
}


  /////////round CCW/////////////////
  void roundAroundCCW (){
   myPIDRound.SetMode(AUTOMATIC);
  raspTX(40);
  temp1=raspRX();
  raspTX(41);
  temp2=raspRX();
  var=temp1*250+temp2;
  hitsLeft=0;
  hitsRight=0;
  InputRound = hitsLeft - hitsRight ;
  encRightValue =analogRead(encRight);
  encLeftValue =analogRead(encLeft);
  if (encRightValue>300||encRightValue<700)
    hitsRight--;
  if (encLeftValue>300||encLeftValue<700)
    hitsLeft--;
  analogWrite(motorRFA, 125);
  analogWrite(motorLBA, 125);
  digitalWrite(controlLed,HIGH);
    while((hitsLeft<var) &&  (hitsRight<var)){
      InputRound = hitsLeft - hitsRight ;
      myPIDRound.Compute();
      analogWrite(motorRFA, motorSpeed-OutputRound);
  }
  analogWrite(motorRFA, 0);
  raspTX(43);
  digitalWrite(controlLed,LOW);
  analogWrite(motorLBA, 0);
 }

 ////////////Go Straight////////////
void goStraight(){

  
  raspTX(30);
  temp1=raspRX();
  raspTX(31);
  temp2=raspRX();
  var=temp1*250+temp2;
  raspTX(33);
  hitsLeft=0;
  hitsRight=0;
   InputStraight = hitsLeft - hitsRight ;
  analogWrite(motorRFA, 125);
  analogWrite(motorLFA, 125);
  digitalWrite(controlLed,HIGH);
  while((hitsLeft<var)&&( hitsRight<var)){
    if(Serial.available()>0){
         zot = (int) Serial.read();
       if (zot==8)
         incRightRasp();
       else if (zot==9)
         incLeftRasp();
       else if (zot==10)
         returnHits();
       else if (zot==4)
         break;
}
    InputStraight = hitsLeft - hitsRight ;
    myPIDStraight.Compute();
    analogWrite(motorRFA, motorSpeed-OutputStraight);
      }


      analogWrite(motorRFA, 0);
      digitalWrite(controlLed,LOW);      
      analogWrite(motorLFA, 0);
      if (zot==4)
        raspTX(4);
  }
///////////////Return Hits/////////

void returnHits() {
  raspTX(102);
  delay(2);
  //raspTX((hitsLeft+hitsRight)/500);
  raspTX(hitsLeft);
  delay(2);
  //raspTX((hitsLeft+hitsRight)%250);
  raspTX(hitsRight);

}
//////////incRightRasp//////////////
void incLeftRasp(){
  raspTX(92);
  temp1=raspRX();
  for (temp2=0;temp2<temp1;temp2++)
    InterruptLeft();
  //hitsLeft=hitsLeft+temp1;
  raspTX(93);
}
void incRightRasp(){
  raspTX(82);
  temp1=raspRX();
  for (temp2=0;temp2<temp1;temp2++)
      InterruptRight();
  //hitsRight=hitsRight+temp1;
  raspTX(83);
}

////////arduino message protocol//////////

int raspRX() {
  while (true){
  if(Serial.available()>0){
       zot = (int) Serial.read();
       return(zot);
       } } }

void raspTX(int z) {
  Serial.println (z); }

////////encoder interruppt part//////////

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


