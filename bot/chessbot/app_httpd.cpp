#include "esp_http_server.h"
#include "esp_timer.h"
#include "esp_camera.h"
#include "img_converters.h"
#include "Arduino.h"

#define P_SPEED 15
#define P_M1_A 13
#define P_M1_B 12
#define P_M2_A 2
#define P_M2_B 14

const int freq = 5000;
const int motorChannel = 3;

typedef struct {
        httpd_req_t *req;
        size_t len;
} jpg_chunking_t;

httpd_handle_t camera_httpd = NULL;

static void motor_control(int pinA, int pinB, int dir){
    Serial.println("Motor control");
    Serial.printf("pa: %d pb: %d dir: %d", pinA, pinB, dir);

    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);

    if (dir == 1) {
      digitalWrite(pinB, HIGH);
    } else if (dir == 2) {
      digitalWrite(pinA, HIGH);
    }
}

static void motor_setup(){
    ledcSetup(motorChannel, freq, 8);
    ledcAttachPin(P_SPEED, motorChannel);
    ledcWrite(motorChannel, 0);
    pinMode(P_M1_A, OUTPUT);
    pinMode(P_M1_B, OUTPUT);
    pinMode(P_M2_A, OUTPUT);
    pinMode(P_M2_B, OUTPUT);
    digitalWrite(P_M1_A, LOW);
    digitalWrite(P_M1_B, LOW);
    digitalWrite(P_M2_A, LOW);
    digitalWrite(P_M2_B, LOW);
    Serial.println("Setup finished, start test pattern");

    ledcWrite(motorChannel, 255);
    motor_control(P_M1_A, P_M1_B, 1);
    motor_control(P_M2_A, P_M2_B, 1);
    delay(3000);
    Serial.println("Step 01");

    //ledcWrite(motorChannel, 255);
    motor_control(P_M1_A, P_M1_B, 2);
    motor_control(P_M2_A, P_M2_B, 2);
    delay(3000);
    Serial.println("Step 02");

    //ledcWrite(motorChannel, 255);
    motor_control(P_M1_A, P_M1_B, 0);
    motor_control(P_M2_A, P_M2_B, 0);
    delay(3000);
    Serial.println("Step 03");

    //ledcWrite(motorChannel, 255);
    motor_control(P_M1_A, P_M1_B, 2);
    motor_control(P_M2_A, P_M2_B, 1);
    delay(2000);
    Serial.println("Step 04");

    //ledcWrite(motorChannel, 255);
    motor_control(P_M1_A, P_M1_B, 1);
    motor_control(P_M2_A, P_M2_B, 2);
    delay(2000);
    Serial.println("Step 05");

    //ledcWrite(motorChannel, 255);
    motor_control(P_M1_A, P_M1_B, 0);
    motor_control(P_M2_A, P_M2_B, 1);
    delay(2000);
    Serial.println("Step 06");
    motor_control(P_M1_A, P_M1_B, 0);
    motor_control(P_M2_A, P_M2_B, 2);
    delay(2000);
    Serial.println("Step 07");
    //ledcWrite(motorChannel, 255);
    motor_control(P_M1_A, P_M1_B, 1);
    motor_control(P_M2_A, P_M2_B, 0);
    delay(2000);
    Serial.println("Step 08");
    motor_control(P_M1_A, P_M1_B, 2);
    motor_control(P_M2_A, P_M2_B, 0);
    delay(2000);
    Serial.println("Step 09");

    Serial.println("Testpattern finished");
    ledcWrite(motorChannel, 0);
    motor_control(P_M1_A, P_M1_B, 0);
    motor_control(P_M2_A, P_M2_B, 0);
    Serial.println("Setup finished");
}

static void motors_run(int dir1, int dir2, int speed, int duration){
    Serial.printf("Motor control: d1: %d d2: %d s: %d d %s", dir1, dir2, speed, duration);
    if (duration < 0) {
        duration = 0;
    }
    if (duration > 30) {
        duration = 30;
    }
    if (speed > 255) {
        speed = 255;
    }

    ledcWrite(motorChannel, speed);

    motor_control(P_M1_A, P_M1_B, dir1);
    motor_control(P_M2_A, P_M2_B, dir2);
    delay(duration);

    motor_control(P_M1_A, P_M1_B, 0);
    motor_control(P_M2_A, P_M2_B, 0);
}

static esp_err_t cmd_handler(httpd_req_t *req){
    Serial.println("move");
    char*  buf;
    size_t buf_len;
    char motor1_dir[2] = {0,};
    char motor2_dir[2] = {0,};
    char speed[3] = {0,};
    char duration[2] = {0,};

    buf_len = httpd_req_get_url_query_len(req) + 1;
    if (buf_len > 1) {
        buf = (char*)malloc(buf_len);
        if(!buf){
            Serial.println("error with no buffer");
            httpd_resp_send_500(req);
            return ESP_FAIL;
        }
        if (httpd_req_get_url_query_str(req, buf, buf_len) == ESP_OK) {
            if (httpd_query_key_value(buf, "m1", motor1_dir, sizeof(motor1_dir)) == ESP_OK &&
                httpd_query_key_value(buf, "m2", motor2_dir, sizeof(motor2_dir)) == ESP_OK &&
                httpd_query_key_value(buf, "d", duration, sizeof(duration)) == ESP_OK &&
                httpd_query_key_value(buf, "s", speed, sizeof(speed)) == ESP_OK) {
            } else {
                free(buf);
                Serial.println("error with query args");

                httpd_resp_send_404(req);
                return ESP_FAIL;
            }
        } else {
            free(buf);
            Serial.println("error with getting query string");
            httpd_resp_send_404(req);
            return ESP_FAIL;
        }
        free(buf);
    } else {
        httpd_resp_send_404(req);
        Serial.println("error with buffer length");
        return ESP_FAIL;
    }

    int m1 = atoi(motor1_dir);
    int m2 = atoi(motor2_dir);
    int d = atoi(duration);
    int s = atoi(speed);

    motors_run(
        atoi(motor1_dir),
        atoi(motor2_dir),
        atoi(speed),
        atoi(duration)
    );
}

static size_t jpg_encode_stream(void * arg, size_t index, const void* data, size_t len){
    jpg_chunking_t *j = (jpg_chunking_t *)arg;
    if(!index){
        j->len = 0;
    }
    if(httpd_resp_send_chunk(j->req, (const char *)data, len) != ESP_OK){
        return 0;
    }
    j->len += len;
    return len;
}

static esp_err_t capture_handler(httpd_req_t *req){
    digitalWrite(4, HIGH);
    camera_fb_t * fb = NULL;
    esp_err_t res = ESP_OK;
    int64_t fr_start = esp_timer_get_time();

    fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("Camera capture failed");
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }

    httpd_resp_set_type(req, "image/jpeg");
    httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=capture.jpg");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");

    size_t out_len, out_width, out_height;
    uint8_t * out_buf;
    bool s;
    bool detected = false;


    size_t fb_len = 0;
    if(fb->format == PIXFORMAT_JPEG){
        fb_len = fb->len;
        res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
    } else {
        jpg_chunking_t jchunk = {req, 0};
        res = frame2jpg_cb(fb, 80, jpg_encode_stream, &jchunk)?ESP_OK:ESP_FAIL;
        httpd_resp_send_chunk(req, NULL, 0);
        fb_len = jchunk.len;
    }
    esp_camera_fb_return(fb);
    int64_t fr_end = esp_timer_get_time();
    Serial.printf("JPG: %uB %ums\n", (uint32_t)(fb_len), (uint32_t)((fr_end - fr_start)/1000));
    digitalWrite(4, LOW);
    return res;

}


static esp_err_t index_handler(httpd_req_t *req){
    static char json_response[1024];
    char * p = json_response;
    *p++ = '{';
    p+=sprintf(p, "\"name\":%s,", "\"chessbot\"");
    p+=sprintf(p, "\"piece\":%s,", "\"wq\"");
    p+=sprintf(p, "\"poc_pic\":%s,", "\"http://192.168.178.200/position.jpeg\"");
    *p++ = '}';
    *p++ = 0;
    httpd_resp_set_type(req, "application/json");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
    return httpd_resp_send(req, json_response, strlen(json_response));
}

void startCameraServer(){
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();

    httpd_uri_t index_uri = {
        .uri       = "/",
        .method    = HTTP_GET,
        .handler   = index_handler,
        .user_ctx  = NULL
    };

    httpd_uri_t cmd_uri = {
        .uri       = "/move",
        .method    = HTTP_GET,
        .handler   = cmd_handler,
        .user_ctx  = NULL
    };

        httpd_uri_t capture_uri = {
        .uri       = "/position.jpeg",
        .method    = HTTP_GET,
        .handler   = capture_handler,
        .user_ctx  = NULL
    };

    Serial.printf("Setup motor with pins: m1a: %d m1b: %d m2a: %d m2b: %d ms: %d\n", P_M1_A, P_M1_B, P_M2_A, P_M2_B, P_SPEED);
    motor_setup();


    Serial.printf("Starting web server on port: '%d'\n", config.server_port);
    if (httpd_start(&camera_httpd, &config) == ESP_OK) {
        httpd_register_uri_handler(camera_httpd, &index_uri);
        httpd_register_uri_handler(camera_httpd, &capture_uri);
    }
}
