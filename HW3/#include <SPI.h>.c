#include <SPI.h>
#include <MFRC522.h>

//전역변수
int count = 0;

//arduino 설정
int blue = 2;
int green = 3;
int red = 4;
int RST_PIN = 9;
int SS_PIN = 10;

MFRC522 mfrc(SS_PIN,RST_PIN);

void setup(){
  Serial.begin(9600);
  SPI.begin();
  mfrc.PCD_Init();
}

void loop(){
  //인식 못하면 계속 return 당하기
  if(!mfrc.PICC_IsNewCardPresent() || !mfrc.PICC_ReadCardSerial()){
    delay(500);
    return;
  }
  count = count + 1;
  if(count%3 == 0){
    analogWrite(blue,0);
    analogWrite(green,0);
    analogWrite(red,255);
  }
  else if(count%3 == 1){
    analogWrite(blue,0);
    analogWrite(red,0);
    analogWrite(green,255);
  }
  else if(count%3 == 2){
    analogWrite(green,0);
    analogWrite(red,0);
    analogWrite(blue,255);
  }
  
}