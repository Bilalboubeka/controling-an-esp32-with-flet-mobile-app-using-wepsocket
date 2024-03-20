#include <WiFi.h>
#include <WebSocketsServer.h>
#include <FS.h>

#define LED1 15
#define LED2 16
#define LED3 2
int toggling = 1 ;
int progres = 0 ;

// Set these to your desired credentials.
const char *ssid = "ssid";
const char *password = "password";

WebSocketsServer webSocket = WebSocketsServer(81);



void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  if (type ==  WStype_CONNECTED)
  {
    digitalWrite(LED3, HIGH);
  }
  
  if (type == WStype_TEXT) {
      Serial.printf("[%u] Text: %s\n", num, payload);
      // Echo text message back to client
      //webSocket.sendTXT(num, payload);
    // Convert payload to a String for easier manipulation
    String message = String((char *)payload);

    // Check the content of the message and perform tasks based on it
    if (message == "Task1") {
      toggling = 0 ;
    } else if (message == "Task2") {
      toggling=1;
    } else if (message == "stop") {
      // Perform Task 3
      toggling=2;
    }
    // Add more conditions as needed for additional tasks
  }
  if (type == WStype_DISCONNECTED)
  {
    digitalWrite(LED3, LOW);
  }
  
}



void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi. IP address: ");
  Serial.println(WiFi.localIP());

  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
}

void loop() {
  webSocket.loop();
  if (toggling == 0)
  {
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, LOW);
    
      
  }else if (toggling==1)
  {
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, HIGH);
  }else if (toggling==2)
  {
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
  }

  // I didn't have a sensor on me I will replace this when I bay one
   static unsigned long lastTime = 0;
  static int counter = 1;

  if (millis() - lastTime > 3000) { // Check if 3 seconds have passed
    lastTime = millis();
    
    // Create a String object to hold the counter value
    String counterStr = String(counter);
    
    // Send the current counter value to all connected clients
    webSocket.broadcastTXT(counterStr);
    
    counter++;
    if (counter > 100) {
      counter = 1; // Reset the counter after reaching 100
    }
  }
  
}

