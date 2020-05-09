#include <SPI.h>
#include <MFRC522.h>

const byte numReaders = 2;
// Each reader has a unique Slave Select pin
const byte ssPins[] = {2, 4};
// They'll share the same reset pin
const byte resetPin = 5;

MFRC522 mfrc522[numReaders];

void setup() {
  // Initialise serial communications channel with the PC
  Serial.begin(9600);
  Serial.println(F("Serial communication started"));

  // Initialise the SPI bus
  SPI.begin();

  for (uint8_t i = 0; i < numReaders; i++) {
    // The Slave Select (SS) pin and reset pin can be assigned to any pin
    mfrc522[i].PCD_Init(ssPins[i], resetPin);
    // Set the gain to max - not sure this makes any difference...
     mfrc522[i].PCD_SetAntennaGain(MFRC522::PCD_RxGain::RxGain_max);

    // Dump some debug information to the serial monitor
    Serial.print(F("Reader #"));
    Serial.print(i);
    Serial.print(F(" initialised on pin "));
    Serial.print(String(ssPins[i]));
    Serial.print(F(". Antenna strength: "));
    Serial.print(mfrc522[i].PCD_GetAntennaGain());
    Serial.print(F(". Version : "));
    mfrc522[i].PCD_DumpVersionToSerial();

    // Slight delay before activating next reader
    delay(100);
  }

  Serial.println(F("--- END SETUP ---"));

}
/**
   Main loop
*/
void loop() {
  // Assume that the tags have not changed since last reading
  boolean changedValue = false;
  // Loop through each reader
  for (uint8_t i = 0; i < numReaders; i++) {
    // Initialise the sensor
    mfrc522[i].PCD_Init();
    // String to hold the ID detected by each sensor
    String readRFID = "";
    // If the sensor detects a tag and is able to read it
    if (mfrc522[i].PICC_IsNewCardPresent() && mfrc522[i].PICC_ReadCardSerial()) {
      // Extract the ID from the tag
      readRFID = dump_byte_array(mfrc522[i].uid.uidByte, mfrc522[i].uid.size);

      Serial.print(F("Reader #"));
      Serial.print(String(i));
      Serial.print(F(" on Pin #"));
      Serial.print(String((ssPins[i])));
      Serial.print(F(" detected tag: "));
      Serial.println(readRFID);
      
    }
    // Halt PICC
//    mfrc522[i].PICC_HaltA();
    // Stop encryption on PCD
//    mfrc522[i].PCD_StopCrypto1();
  }

}
/**
   Helper function to return a string ID from byte array
*/
String dump_byte_array(byte *buffer, byte bufferSize) {
  String read_rfid = "";
  for (byte i = 0; i < bufferSize; i++) {
    read_rfid = read_rfid + String(buffer[i], HEX);
  }
  return read_rfid;
}