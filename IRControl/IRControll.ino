
#include <IRremote.h>
IRsend irsend;
 
void setup() {
    Serial.begin(115200);
    //IR
    IrSender.begin(3, ENABLE_LED_FEEDBACK);
    IrSender.enableIROut(38);

    //Joy
    pinMode(8, INPUT_PULLUP); 
}

uint16_t sAddress1 = 0x0102;
uint8_t sRepeats = 0;
void loop() {
  //JOY DEBUG
  
  Serial.print(analogRead(A1)/400); Serial.print("  ");         
  Serial.print(analogRead(A0)/400); Serial.print("  ");          
  Serial.println((analogRead(A2) / 110));

//  IrSender.sendNEC(sAddress1, 0, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 1, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 2, sRepeats);
//  delay(1000);
  
//  IrSender.sendNEC(sAddress1, 0x10, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x11, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x12, sRepeats);
//  delay(1000);
//  
//  IrSender.sendNEC(sAddress1, 0x20, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x21, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x22, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x23, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x24, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x25, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x26, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x27, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x28, sRepeats);
//  delay(1000);
//  IrSender.sendNEC(sAddress1, 0x29, sRepeats);
//  delay(100000);

  IrSender.sendNEC(sAddress1, (analogRead(A1) / 400), sRepeats);
  delay(100);
  IrSender.sendNEC(sAddress1, (analogRead(A0) / 400) + 0x10, sRepeats);
  delay(100);
  IrSender.sendNEC(sAddress1, (analogRead(A2) / 110) + 0x20, sRepeats);
  delay(100);
  
}
