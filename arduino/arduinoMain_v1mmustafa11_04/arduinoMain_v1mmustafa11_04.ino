
#include <PID_v1.h> 
///////define parts/////////
#define enablePin  52 
#define encoderRight  0
#define encoderLeft 1
#define controlLed 13
#define echoPin 30
#define trigPin 31

#define motorRFA 4  // sag motor sari pin//sag ileri aktif
#define motorRBA 5  // sag motor siyah pin
#define motorLBA 6  // sol motor kirmizi pin
#define motorLFA 7  // sol motor siyah pin
#define motorSpeed 125
volatile int hitsRight = 0;
volatile int hitsLeft = 0;
long distance;
int raspMessage,roundDirection,var, zot, temp1, temp2; 
double SetPointStraight=0, SetPointRound=0;
double InputStraight, InputRound;
double  OutputStraight, OutputRound;
int encoderDifference; 
volatile unsigned long last_microsRight, last_microsLeft;
long debouncing_time =25;
PID myPIDStraight(&InputStraight, &OutputStraight, &SetPointStraight, 1, 4, 2, DIRECT);
PID myPIDRound(&InputRound, &OutputRound, &SetPointRound, 5, 4, 2, DIRECT);

void setup() {
  Serial.begin(9600);  
  /*pinMode(encoderRight, INPUT);	// analog read icin simdilik dursun!!
  pinMode(encoderLeft, INPUT);*/	// sistem basladiginda test edebilmek icin encoderleri	
  pinMode(controlLed, OUTPUT);
  attachInterrupt(4, countLeft, CHANGE);
  attachInterrupt(5, countRight, CHANGE); 
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
  myPIDRound.SetMode(AUTOMATIC); 
   
 
  }

void loop() {

   while (true){
     if(raspRX()==1)
           break;     
  }
   raspTX(2);
   
     
        switch (raspRX()){
        case 5:  roundAroundCW();
        case 6:  roundAroundCCW();
        case 7:  goStraight();
        case 8:  incRightRasp();
        case 9:  incLeftRasp();
        case 10: returnHits();
        }
    
  
}
////////////Round CW///////////
void roundAroundCW (){  
  raspTX(20);
  temp1=raspRX();   
  raspTX(21);  
  temp2=raspRX();
  var=temp1*250+temp2;
  hitsLeft=0;
  hitsRight=0;
  InputRound = hitsLeft - hitsRight ;  
  analogWrite(motorRBA, 125);
  analogWrite(motorLFA, 125);
  digitalWrite(controlLed,HIGH);
  while((hitsLeft<var) &&  (hitsRight<var)){ 
    InputRound = hitsLeft - hitsRight ;   
    if (InputRound > SetPointRound ){
	myPIDRound.SetControllerDirection(REVERSE);
        myPIDRound.Compute();
	analogWrite(motorRBA, motorSpeed-OutputRound);
    	analogWrite(motorLFA, 125); }
    else if (InputRound < SetPointRound){
	myPIDRound.SetControllerDirection(DIRECT);
        myPIDRound.Compute();
        analogWrite(motorRBA, motorSpeed-OutputRound);
    	analogWrite(motorLFA, 125); }
    else if (hitsLeft == hitsRight){
        analogWrite(motorRBA, 125);
        analogWrite(motorLFA, 125);}
  
  }
  analogWrite(motorRBA, 0);
  raspTX(3);
  digitalWrite(controlLed,LOW);
  analogWrite(motorLFA, 0);
}


  /////////round CCW/////////////////
  void roundAroundCCW (){
  raspTX(40);
  temp1=raspRX();   
  raspTX(41);  
  temp2=raspRX();
  var=temp1*250+temp2;
  hitsLeft=0;
  hitsRight=0;
  InputRound = hitsLeft - hitsRight ;  
  analogWrite(motorRFA, 125);
  analogWrite(motorLBA, 125);
  digitalWrite(controlLed,HIGH);
  while((hitsLeft<var) &&( hitsRight<var)){  
    InputRound = hitsLeft - hitsRight ;   
    if (InputRound > SetPointRound ){
	myPIDRound.SetControllerDirection(REVERSE);
        myPIDRound.Compute();
	analogWrite(motorRFA, motorSpeed-OutputRound);
    	analogWrite(motorLBA, 125); }
    else if (InputRound < SetPointRound){
	myPIDRound.SetControllerDirection(DIRECT);
        myPIDRound.Compute();
        analogWrite(motorRFA, motorSpeed-OutputRound);
    	analogWrite(motorLBA, 125); }
    else if (hitsLeft == hitsRight){
        analogWrite(motorRFA, 125);
        analogWrite(motorLBA, 125);}
 
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
  hitsLeft=0;
  hitsRight=0;
    
  analogWrite(motorRFA, 125);
  analogWrite(motorLFA, 125);
  digitalWrite(controlLed,HIGH);
  while((hitsLeft<var)&&( hitsRight<var)){
     InputStraight = hitsLeft - hitsRight ;    
     if (InputStraight > SetPointStraight ){
	myPIDStraight.SetControllerDirection(REVERSE);
        myPIDStraight.Compute();
	analogWrite(motorRFA, motorSpeed-OutputStraight);
    	analogWrite(motorLFA, 125); }
    else if (InputStraight < SetPointStraight){
	myPIDStraight.SetControllerDirection(DIRECT);
        myPIDStraight.Compute();
        analogWrite(motorRFA, motorSpeed-OutputStraight);
    	analogWrite(motorLFA, 125); }
    else if (hitsLeft == hitsRight){
        analogWrite(motorRFA, 125);
        analogWrite(motorLFA, 125);}
    
      }
    
    
      analogWrite(motorRFA, 0);
      digitalWrite(controlLed,LOW);
      raspTX(33);
      analogWrite(motorLFA, 0);
  }
///////////////Return Hits/////////  
  
void returnHits() {
  raspTX(2);
  delay(2);
  raspTX((hitsLeft+hitsRight)/500);
  delay(2);
  raspTX((hitsLeft+hitsRight)%250);

}
//////////incRightRasp//////////////
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


