#include "esp_camera.h"
#include <WiFi.h>
#include <Arduino.h>


// these are from example code
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// pin to whats on the board mapping for motor controls

#define P_104 4
#define P_102 2
#define P_1014 14
#define P_1015 15
#define P_1013 13
#define P_1012 12


const char* ssid = "Trochilidae";
const char* password = "humm!ngb!rd31";

void startCameraServer();

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
//     config.fb_count = 1;

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_XGA);

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");


    // register
  pinMode(P_104, OUTPUT); // purple pwm
  pinMode(P_102, OUTPUT); // red
  pinMode(P_1014, OUTPUT); // yellow

  pinMode(P_1015, OUTPUT); // purple pwm
  pinMode(P_1013, OUTPUT); // red
  pinMode(P_1012, OUTPUT); // yellow

    // setup all of
  analogWrite(P_104, 0); // purple pwm
  digitalWrite(P_102, LOW); // red
  digitalWrite(P_1014, LOW); // yellow

  analogWrite(P_1015, 0); // purple pwm
  digitalWrite(P_1013, LOW); // red
  digitalWrite(P_1012, LOW); // yellow

    // run
  analogWrite(P_104, 0); // purple pwm
  digitalWrite(P_102, HIGH); // red
  digitalWrite(P_1014, LOW); // yellow

  analogWrite(P_1015, 0); // purple pwm
  digitalWrite(P_1013, HIGH); // red
  digitalWrite(P_1012, LOW); // yellow
          delay(2000);

    // setup all of
  analogWrite(P_104, 0); // purple pwm
  digitalWrite(P_102, LOW); // red
  digitalWrite(P_1014, LOW); // yellow

  analogWrite(P_1015, 0); // purple pwm
  digitalWrite(P_1013, LOW); // red
  digitalWrite(P_1012, LOW); // yellow
          delay(2000);
    // run
  analogWrite(P_104, 0); // purple pwm
  digitalWrite(P_102, HIGH); // red
  digitalWrite(P_1014, LOW); // yellow

  analogWrite(P_1015, 0); // purple pwm
  digitalWrite(P_1013, HIGH); // red
  digitalWrite(P_1012, LOW); // yellow
          delay(4000);

    // setup all of
  analogWrite(P_104, 0); // purple pwm
  digitalWrite(P_102, LOW); // red
  digitalWrite(P_1014, LOW); // yellow

  analogWrite(P_1015, 0); // purple pwm
  digitalWrite(P_1013, LOW); // red
  digitalWrite(P_1012, LOW); // yellow





}

void loop() {
  // put your main code here, to run repeatedly:
  delay(10000);
}
