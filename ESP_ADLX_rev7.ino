#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <HTTPClient.h>

const char *mqtt_user = "TP-Link_C936";
const char *mqtt_password = "65413357";
//const char *mqtt_user = "Piramide";
//const char *mqtt_password = "Bolsonaro26";
const char *mqtt_client_id = "";


float acceleration_x = 0;
float acceleration_y = 0;
float acceleration_z = 0;

// REPLACE with your Domain name and URL path or IP address with path
const char* serverName = "http://192.168.0.103/post-esp-data.php";
//const char* serverName = "http://192.168.0.105/post-esp-data.php";

// Keep this API Key value to be compatible with the PHP code provided in the project page. 
// If you change the apiKeyValue value, the PHP file /post-esp-data.php also needs to have the same key 
String apiKeyValue = "tPmAT5Ab3j7F9";

String sensorName = "none";          //-------------------------------------------------------------------colocar dados da maquina
String sensorLocation = "none";

int httpResponseCode;
bool start_python = 0;

// Replace the next variables with your SSID/Password combination
//const char* ssid = "Piramide";
//const char* password = "Bolsonaro26";
const char* ssid = "TP-Link_C936";
const char* password = "65413357";


// Add your MQTT Broker IP address, example:
const char* mqtt_server = "192.168.0.103";
//const char* mqtt_server = "192.168.0.105";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

bool start = 0;

const int ledPin = 4;

bool read_sensor = 0;

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

void displaySensorDetails(void)
{
  sensor_t sensor;
  accel.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" m/s^2");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" m/s^2");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" m/s^2"); 
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

void displayDataRate(void)
{
  Serial.print  ("Data Rate:    "); 
 
  switch(accel.getDataRate())
  {
    case ADXL345_DATARATE_3200_HZ:
      Serial.print  ("3200 "); 
      break;
    case ADXL345_DATARATE_1600_HZ:
      Serial.print  ("1600 "); 
      break;
    case ADXL345_DATARATE_800_HZ:
      Serial.print  ("800 "); 
      break;
    case ADXL345_DATARATE_400_HZ:
      Serial.print  ("400 "); 
      break;
    case ADXL345_DATARATE_200_HZ:
      Serial.print  ("200 "); 
      break;
    case ADXL345_DATARATE_100_HZ:
      Serial.print  ("100 "); 
      break;
    case ADXL345_DATARATE_50_HZ:
      Serial.print  ("50 "); 
      break;
    case ADXL345_DATARATE_25_HZ:
      Serial.print  ("25 "); 
      break;
    case ADXL345_DATARATE_12_5_HZ:
      Serial.print  ("12.5 "); 
      break;
    case ADXL345_DATARATE_6_25HZ:
      Serial.print  ("6.25 "); 
      break;
    case ADXL345_DATARATE_3_13_HZ:
      Serial.print  ("3.13 "); 
      break;
    case ADXL345_DATARATE_1_56_HZ:
      Serial.print  ("1.56 "); 
      break;
    case ADXL345_DATARATE_0_78_HZ:
      Serial.print  ("0.78 "); 
      break;
    case ADXL345_DATARATE_0_39_HZ:
      Serial.print  ("0.39 "); 
      break;
    case ADXL345_DATARATE_0_20_HZ:
      Serial.print  ("0.20 "); 
      break;
    case ADXL345_DATARATE_0_10_HZ:
      Serial.print  ("0.10 "); 
      break;
    default:
      Serial.print  ("???? "); 
      break;
  } 
  Serial.println(" Hz"); 
}

void displayRange(void)
{
  Serial.print ("Range:         +/- ");
 
  switch(accel.getRange())
  {
    case ADXL345_RANGE_16_G:
      Serial.print  ("16 "); 
      break;
    case ADXL345_RANGE_8_G:
      Serial.print  ("8 "); 
      break;
    case ADXL345_RANGE_4_G:
      Serial.print  ("4 "); 
      break;
    case ADXL345_RANGE_2_G:
      Serial.print  ("2 "); 
      break;
    default:
      Serial.print  ("?? "); 
      break;
  } 
  Serial.println(" g"); 
}

void setup(void) 
{

  Serial.begin(9600);
  Serial.println("Accelerometer Test"); Serial.println("");
 
  /* Initialise the sensor */
  if(!accel.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }

  /* Set the range to whatever is appropriate for your project */
  //accel.setRange(ADXL345_RANGE_16_G);
  accel.setDataRate(ADXL345_DATARATE_25_HZ);
  //accel.setRange(ADXL345_RANGE_8_G);
  // accel.setRange(ADXL345_RANGE_4_G);
  accel.setRange(ADXL345_RANGE_2_G);

  //accel.writeRegister(ADXL345_REG_FIFO_CTL, 0x40); // Modo FIFO
  //accel.writeRegister(ADXL345_REG_FIFO_CTL, 0x80 | 32); // Habilita o FIFO e define a profundidade (32 entradas)
  //accel.setOffsetX(1);
 
  delay(1000);


  /* Display some basic information on this sensor */
  displaySensorDetails();
 
  /* Display additional settings (outside the scope of sensor_t) */
  displayDataRate();
  displayRange();
  Serial.println("");

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(ledPin, OUTPUT);
}



void setup_wifi() 
{
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) //----------------------- TRATA OS DADOS QUE VEM VIA MQTT --------------------
{
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
  if (String(topic) == "esp32/output") {
    Serial.print("Changing output to ");
    
    if(messageTemp == "on"){
      Serial.println("on");
      //digitalWrite(ledPin, HIGH);
      client.publish("esp32/status", "trabalhando");
      start= 1 ;
    

    }

    
    else if(messageTemp == "off"){
      Serial.println("off");
      //digitalWrite(ledPin, LOW);
    }
    else if(messageTemp == "1"){
      sensorName = "Rotative";
      sensorLocation = "MT27";
      Serial.println("Ligando leitura MT28");
      //digitalWrite(ledPin, LOW);
    }
    else if(messageTemp == "2"){
      sensorName = "Rotative";
      sensorLocation = "MT28";
      Serial.println("Ligando leitura MT29");
      //digitalWrite(ledPin, LOW);
    }
    
    else if(messageTemp == "3"){
      sensorName = "Rotative";
      sensorLocation = "MT29";
      Serial.println("Ligando leitura MT29");
      //digitalWrite(ledPin, LOW);
    }
    else if(messageTemp == "4"){
      sensorName = "Rotative";
      sensorLocation = "MT30";
      Serial.println("Ligando leitura MT31");
      //digitalWrite(ledPin, LOW);
    }
    else if(messageTemp == "5"){
      sensorName = "Rotative";
      sensorLocation = "MT31";
      Serial.println("Ligando leitura MT32");
      //digitalWrite(ledPin, LOW);
    }
    else if(messageTemp == "6"){
      sensorName = "Rotative";
      sensorLocation = "MT32";
      Serial.println("Ligando leitura MT33");
      //digitalWrite(ledPin, LOW);
    }
    else if(messageTemp == "7"){
      sensorName = "Rotative";
      sensorLocation = "MT33";
      Serial.println("Ligando leitura MT34");
      //digitalWrite(ledPin, LOW);
    }
    else if(messageTemp == "8"){
      sensorName = "Rotative";
      sensorLocation = "MT35";
      Serial.println("Ligando leitura MT35");
      //digitalWrite(ledPin, LOW);
    }

    
    }
}

void reconnect() 
{
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(mqtt_client_id, mqtt_user, mqtt_password)) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop(void) 

{

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  /* Get a new sensor event */ 
  sensors_event_t event;  
  accel.getEvent(&event);
  
  if(WiFi.status()== WL_CONNECTED){

    WiFiClient client;

  }
  
  delay(100);

    if (start ==1){
      for (int i = 0; i < 300; i++){
        sensors_event_t event;  
        accel.getEvent(&event);

        acceleration_x = (event.acceleration.x);
        char xString[8];

        acceleration_y = (event.acceleration.y) ;
        char yString[8];

        acceleration_z = (event.acceleration.z) ;
        char zString[8];

        // Converter os valores de aceleração para strings
        dtostrf(acceleration_x, 1, 2, xString);
        dtostrf(acceleration_y, 1, 2, yString);
        dtostrf(acceleration_z, 1, 2, zString);

        // Criar uma string contendo os valores de aceleração concatenados
        char accelString[50]; // Tamanho total é suficiente para armazenar os três valores e delimitadores
        snprintf(accelString, sizeof(accelString), "%s,%s,%s,%s,%s", sensorName,sensorLocation,xString, yString, zString);

        // Publicar a string de aceleração no tópico "python/accel"
        client.publish("python/accel", accelString);

      }
      start = 0;
      
    }

//----------------------------------------------------------------------------------------------------------------------------------------------------

  long now = millis();
  if (now - lastMsg > 10000) {
    lastMsg = now;

    client.publish("esp32/status", "ligado oscioso");
    

    
    
    acceleration_x = (event.acceleration.x);
    char xString[8];
    dtostrf(acceleration_x, 1, 2, xString);
    //Serial.print("eixo_x: ");
    //Serial.println(xString);
    client.publish("esp32/eixo_x", xString);

    acceleration_y = (event.acceleration.y) ;
    char yString[8];
    dtostrf(acceleration_y, 1, 2, yString);
    //Serial.print("eixo_y: ");
    //Serial.println(yString);
    client.publish("esp32/eixo_y", yString);

    acceleration_z = (event.acceleration.z) ;
    char zString[8];
    dtostrf(acceleration_z, 1, 2, zString);
    //Serial.print("eixo_z: ");
    //Serial.println(zString);
    client.publish("esp32/eixo_z", zString);
  
  }

}

