/*
 * MIT License
 *
 * Copyright (c) 2024 LittleMouse
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * - The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
#include "image.h"
#include "M5CoreS3.h"
#include <M5ModuleLLM.h>

#include <ArduinoJson.h>
#include <FreeRTOS.h>

#define Serial USBSerial  // PlatformIO

SemaphoreHandle_t mutex;

extern const uint16_t rgb565[];

struct box_t {
    int x;
    int y;
    int w;
    int h;
    std::uint16_t color;
    int touch_id = -1;

    void clear(void)
    {
        M5.Display.setColor(M5.Display.getBaseColor());
        for (int i = 0; i < 8; ++i) {
            M5.Display.drawRoundRect(x + i, y + i, w - i * 2, h - i * 2, 20);
        }
    }
    void draw(void)
    {
        M5.Display.setColor(color);
        int ie = touch_id < 0 ? 4 : 8;
        for (int i = 0; i < ie; ++i) {
            M5.Display.drawRoundRect(x + i, y + i, w - i * 2, h - i * 2, 20);
        }
    }
    bool contain(int x, int y)
    {
        return this->x <= x && x < (this->x + this->w) && this->y <= y && y < (this->y + this->h);
    }
};

struct yolo_box_t {
    String class_name;
    float confidence;
    int x1;
    int y1;
    int x2;
    int y2;
    int frame;
};

static constexpr std::size_t box_count = 5;
static box_t box_list[box_count];
static yolo_box_t yolo_box;
static bool state;
static M5ModuleLLM module_llm;
// static String camera_work_id;
static String yolo_work_id;

const size_t JSON_BUFFER_SIZE = 2048;
char jsonBuffer[JSON_BUFFER_SIZE];
size_t bufferIndex = 0;

void setup_menu(void)
{
    M5.Display.pushImage(0, 0, CoreS3.Display.width(), CoreS3.Display.height(), rgb565);

    M5.Display.setTextDatum(middle_center);
    M5.Display.setFont(&fonts::Orbitron_Light_24);

    for (std::size_t i = 0; i < box_count - 1; ++i) {
        box_list[i].w = 100;
        box_list[i].h = 100;
    }
    box_list[0].x = 35;
    box_list[0].y = 12;
    box_list[1].x = 187;
    box_list[1].y = 12;
    box_list[2].x = 35;
    box_list[2].y = 130;
    box_list[3].x = 187;
    box_list[3].y = 130;
}

void setup_camera(void)
{
    CoreS3.Display.setTextColor(ORANGE);
    CoreS3.Display.setTextDatum(middle_center);
    CoreS3.Display.setFont(&fonts::Orbitron_Light_24);

    if (!CoreS3.Camera.begin()) {
        CoreS3.Display.drawString("Camera Init Fail", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    }
    CoreS3.Display.drawString("Camera Init Success", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    CoreS3.Camera.sensor->set_framesize(CoreS3.Camera.sensor, FRAMESIZE_QVGA);
}

void setup_comm(void)
{
    Serial.begin(115200);
    Serial2.begin(1500000, SERIAL_8N1, 18, 17);
    Serial2.setRxBufferSize(2048);
}

void setup_llm(void)
{
    M5.Display.setTextColor(ORANGE);
    M5.Display.setTextSize(1);
    M5.Display.setTextDatum(middle_center);
    module_llm.begin(&Serial2);
    M5.Display.drawString("Check ModuleLLM connection..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    while (1) {
        if (module_llm.checkConnection()) {
            break;
        }
    }

    M5.Display.drawString("Reset ModuleLLM..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    module_llm.sys.reset();
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("Setup ok..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
}

void setup_yolo_detect(void)
{
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("setup_yolo_detect..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    m5_module_llm::ApiYoloSetupConfig_t yolo_config;
    yolo_config.input = {"yolo.jpeg.base64"};
    yolo_config.model = "yolo11n";
    yolo_work_id      = module_llm.yolo.setup(yolo_config, "yolo_setup");
    while (yolo_work_id == nullptr) vTaskDelay(100);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("yolo setup done..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    vTaskDelay(200);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
}

void setup_yolo_pose(void)
{
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("setup_yolo_pose..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    m5_module_llm::ApiYoloSetupConfig_t yolo_config;
    yolo_config.input = {"yolo.jpeg.base64"};
    yolo_config.model = "yolo11n-pose";
    yolo_work_id      = module_llm.yolo.setup(yolo_config, "yolo_setup");
    while (yolo_work_id == nullptr) vTaskDelay(100);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("yolo setup done..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    vTaskDelay(200);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
}

void setup_yolo_seg(void)
{
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("setup_yolo_seg..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    m5_module_llm::ApiYoloSetupConfig_t yolo_config;
    yolo_config.input = {"yolo.jpeg.base64"};
    yolo_config.model = "yolo11n-seg";
    yolo_work_id      = module_llm.yolo.setup(yolo_config, "yolo_setup");
    while (yolo_work_id == nullptr) vTaskDelay(100);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("yolo setup done..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    vTaskDelay(200);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
}

void setup_yolo_hand(void)
{
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("setup_yolo_hand..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    m5_module_llm::ApiYoloSetupConfig_t yolo_config;
    yolo_config.input = {"yolo.jpeg.base64"};
    yolo_config.model = "yolo11n-hand";
    yolo_work_id      = module_llm.yolo.setup(yolo_config, "yolo_setup");
    while (yolo_work_id == nullptr) vTaskDelay(100);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
    M5.Display.drawString("yolo setup done..", CoreS3.Display.width() / 2, CoreS3.Display.height() / 2);
    vTaskDelay(200);
    M5.Display.fillRect(0, (CoreS3.Display.height() / 2) - 10, 320, 25, WHITE);
}

void setup_yolo(int j)
{
    void (*setupFunctions[4])() = {setup_yolo_detect, setup_yolo_pose, setup_yolo_seg, setup_yolo_hand};

    if (j >= 0 && j < 4) {
        setupFunctions[j]();
        state = true;
    }
}

void menuTask(void* pvParameters)
{
    while (true) {
        if (state) {
            vTaskDelay(100);
            continue;
        }

        M5.delay(1);
        M5.update();

        auto count = M5.Touch.getCount();
        if (!count) {
            vTaskDelay(10);
            continue;
        }

        static m5::touch_state_t prev_state;
        auto t = M5.Touch.getDetail();
        if (prev_state != t.state) {
            prev_state                                  = t.state;
            static constexpr const char* state_name[16] = {
                "none", "touch", "touch_end", "touch_begin", "___", "hold", "hold_end", "hold_begin",
                "___",  "flick", "flick_end", "flick_begin", "___", "drag", "drag_end", "drag_begin"};
            M5_LOGI("%s", state_name[t.state]);
        }

        for (std::size_t i = 0; i < count; ++i) {
            auto t = M5.Touch.getDetail(i);

            for (std::size_t j = 0; j < box_count - 1; ++j) {
                if (t.wasClicked() && box_list[j].contain(t.x, t.y)) {
                    box_list[j].touch_id = t.id;
                    setup_yolo(j);
                }

                M5.Display.waitDisplay();
                if (box_list[j].touch_id == t.id) {
                    if (t.wasReleased()) {
                        box_list[j].touch_id = -1;
                        box_list[j].clear();
                    } else {
                        auto dx = t.deltaX();
                        auto dy = t.deltaY();
                        if (dx || dy) {
                            box_list[j].clear();
                            box_list[j].x += dx;
                            box_list[j].y += dy;
                        }
                    }
                }
            }
        }
        vTaskDelay(10);
    }
}

void menuBackTask(void* pvParameters)
{
    while (true) {
        if (!state) {
            vTaskDelay(100);
            continue;
        }

        M5.update();

        box_list[4].x     = 0;
        box_list[4].y     = 0;
        box_list[4].w     = 100;
        box_list[4].h     = 70;
        box_list[4].color = TFT_CYAN;
        box_list[4].draw();

        CoreS3.Display.setTextColor(CYAN);
        M5.Display.setTextSize(1);
        M5.Display.drawString("Back", 50, 30);

        auto count = M5.Touch.getCount();

        for (std::size_t i = 0; i < count; ++i) {
            auto t = M5.Touch.getDetail(i);
            if (t.wasClicked() && box_list[4].contain(t.x, t.y)) {
                box_list[4].touch_id = t.id;
                state                = false;
                esp_restart();
            }
        }

        vTaskDelay(100);
    }
}

void send_camera_data(uint8_t* out_jpg, size_t out_jpg_len)
{
    JsonDocument jsonDoc;
    jsonDoc["RAW"]        = out_jpg_len;
    jsonDoc["request_id"] = "yolo_inference";
    jsonDoc["work_id"]    = yolo_work_id;
    jsonDoc["action"]     = "inference";
    jsonDoc["object"]     = "cv.jpeg.base64";

    char jsonString[256];
    serializeJson(jsonDoc, jsonString);

    Serial2.write((const uint8_t*)jsonString, strlen(jsonString));
    Serial2.write(out_jpg, out_jpg_len);
}

void parseJson(const char* jsonString)
{
    JsonDocument jsonDoc;
    // Serial.println(jsonString);
    DeserializationError error = deserializeJson(jsonDoc, jsonString);
    if (error) return;

    if (jsonDoc["request_id"].isNull()) return;
    const char* request_id = jsonDoc["request_id"];

    if (strcmp(request_id, "yolo_inference") == 0) {
        JsonArray delta = jsonDoc["data"]["delta"].as<JsonArray>();

        if (delta.size() > 0) {
            JsonObject result   = delta[0].as<JsonObject>();
            yolo_box.class_name = result["class"].as<String>();
            yolo_box.confidence = result["confidence"].as<float>();
            JsonArray bboxArray = result["bbox"].as<JsonArray>();

            if (bboxArray.size() == 4) {
                yolo_box.frame = 2;
                yolo_box.x1    = bboxArray[0].as<int>();
                yolo_box.y1    = bboxArray[1].as<int>();
                yolo_box.x2    = bboxArray[2].as<int>();
                yolo_box.y2    = bboxArray[3].as<int>();
            }
        }
    }
}

void recv_llm_data(void)
{
    static int bufferIndex = 0;

    while (Serial2.available() > 0) {
        char c = Serial2.read();

        if (c == '\n') {
            if (bufferIndex > 0) {
                jsonBuffer[bufferIndex] = '\0';
                parseJson(jsonBuffer);
                bufferIndex = 0;
            }
        } else if (bufferIndex < JSON_BUFFER_SIZE - 1) {
            jsonBuffer[bufferIndex++] = c;
        } else {
            bufferIndex = 0;
        }
    }
}

void recvTask(void* pvParameters)
{
    while (true) {
        if (state) {
            recv_llm_data();
        } else {
            vTaskDelay(100);
        }
    }
}

void cameraTask(void* pvParameters)
{
    while (true) {
        if (state) {
            if (CoreS3.Camera.get()) {
                uint8_t* out_jpg   = NULL;
                size_t out_jpg_len = 0;
                frame2jpg(CoreS3.Camera.fb, 50, &out_jpg, &out_jpg_len);
                send_camera_data(out_jpg, out_jpg_len);
                free(out_jpg);
                CoreS3.Display.pushImage(0, 0, CoreS3.Display.width(), CoreS3.Display.height(),
                                         (uint16_t*)CoreS3.Camera.fb->buf);
                if (yolo_box.frame) {
                    yolo_box.frame--;
                    M5.Display.setTextDatum(bottom_left);
                    M5.Display.drawString(yolo_box.class_name.c_str(), yolo_box.x1, yolo_box.y1);
                    M5.Display.setTextDatum(bottom_left);
                    M5.Display.drawFloat(yolo_box.confidence, 2, yolo_box.x2, yolo_box.y1);
                    M5.Display.drawRect(yolo_box.x1, yolo_box.y1, yolo_box.x2, yolo_box.y2, ORANGE);
                }
                CoreS3.Camera.free();
            }
        } else {
            vTaskDelay(100);
        }
    }
}

void setup_task(void)
{
    mutex = xSemaphoreCreateMutex();
    xTaskCreatePinnedToCore(recvTask, "Receive Task", 4096, NULL, 3, NULL, 1);
    xTaskCreatePinnedToCore(cameraTask, "Camera Task", 8192, NULL, 2, NULL, 0);
    xTaskCreatePinnedToCore(menuTask, "Menu Task", 2048, NULL, 1, NULL, 1);
    // xTaskCreatePinnedToCore(menuBackTask, "Menu Back Task", 2048, NULL, 0, NULL, 1);
}

void setup()
{
    CoreS3.begin();
    setup_camera();
    setup_menu();
    setup_comm();
    setup_llm();
    setup_task();
}

void loop()
{
}
