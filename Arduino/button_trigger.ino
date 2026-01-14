/*
 * Project: IoT Contactless Attendance System
 * Module: Sensor Node (Arduino Uno R4 WiFi)
 * Description: Reads digital button input and transmits serial trigger event.
 */

const int BUTTON_PIN = 2;   // Connected to D2
const int BAUD_RATE = 9600; // Serial communication speed

void setup() {
  // Initialize UART Serial Communication
  Serial.begin(BAUD_RATE);
  
  // Configure pin as Input with Internal Pull-Up Resistor
  // LOW = Pressed, HIGH = Not Pressed
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int buttonState = digitalRead(BUTTON_PIN);

  // Check if button is pressed (Active LOW)
  if (buttonState == LOW) {
    // Send M2M trigger signal to Edge Gateway (Raspberry Pi)
    Serial.println("CHECKIN");
    
    // Debounce delay to prevent multiple triggers
    delay(1000); 
  }
}