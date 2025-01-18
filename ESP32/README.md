## 概要

M5CoreS3を購入し、YOLOのカメラサンプル(ESP32/cpp/src/yolo11n.cpp)を動かしてみましたが、
試してみたところ、うまく動かせていません。(25/01/18)

以下を確認して、気づいたところあれば、アドバイス頂けませんか？
また、CoreS3とModule-LLMが故障してないかみたいので、そちらでコンパイルできた、CoreS3のバイナリファイルを頂けませんか？


## 実施①：VSCode+PlatformIOでのビルドの実行→M5ModuleLLMのバージョンが古いことでのコンパイルエラー発生。

https://github.com/Abandon-ht/ModuleLLM_Development_Guide/tree/dev
から、ファイルを一式ダウンロード

PlatformIOでビルドすると以下のエラーが発生する、M5ModuleLLMのバージョンが古い。

```
Processing M5CoreS3 (platform: espressif32@6.9.0; board: esp32-s3-devkitc-1; framework: arduino)
-------------------------------------------------------------------------------------------------------------------------------------
Verbose mode can be enabled via `-v, --verbose` option
CONFIGURATION: https://docs.platformio.org/page/boards/espressif32/esp32-s3-devkitc-1.html
PLATFORM: Espressif 32 (6.9.0) > Espressif ESP32-S3-DevKitC-1-N8 (8 MB QD, No PSRAM)
HARDWARE: ESP32S3 240MHz, 320KB RAM, 8MB Flash
DEBUG: Current (esp-builtin) On-board (esp-builtin) External (cmsis-dap, esp-bridge, esp-prog, iot-bus-jtag, jlink, minimodule, olimex-arm-usb-ocd, olimex-arm-usb-ocd-h, olimex-arm-usb-tiny-h, olimex-jtag-tiny, tumpa)
PACKAGES: 
 - framework-arduinoespressif32 @ 3.20017.241212+sha.dcc1105b 
 - tool-esptoolpy @ 1.40501.0 (4.5.1) 
 - toolchain-riscv32-esp @ 8.4.0+2021r2-patch5 
 - toolchain-xtensa-esp32s3 @ 8.4.0+2021r2-patch5
LDF: Library Dependency Finder -> https://bit.ly/configure-pio-ldf
LDF Modes: Finder ~ chain, Compatibility ~ soft
Found 39 compatible libraries
Scanning dependencies...
Dependency Graph
|-- TaskScheduler @ 3.8.5
|-- ArduinoJson @ 7.3.0
|-- M5Unified @ 0.2.2
|-- M5CoreS3 @ 1.0.0
|-- M5Module-LLM @ 1.3.0
Building in release mode
Compiling .pio\build\M5CoreS3\src\yolo11n.cpp.o
Building .pio\build\M5CoreS3\bootloader.bin
Generating partitions .pio\build\M5CoreS3\partitions.bin
esptool.py v4.5.1
Creating esp32s3 image...
Merged 1 ELF section
Successfully created esp32s3 image.
Compiling .pio\build\M5CoreS3\libbfa\SPI\SPI.cpp.o
Compiling .pio\build\M5CoreS3\libc5e\Wire\Wire.cpp.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\M5GFX.cpp.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\Fonts\IPA\lgfx_font_japan.c.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\Fonts\efont\lgfx_efont_cn.c.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\Fonts\efont\lgfx_efont_ja.c.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\Fonts\efont\lgfx_efont_kr.c.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\Fonts\efont\lgfx_efont_tw.c.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\utility\lgfx_miniz.c.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\utility\lgfx_pngle.c.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\utility\lgfx_qoi.c.o
Archiving .pio\build\M5CoreS3\libbfa\libSPI.a
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\utility\lgfx_qrcode.c.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\utility\lgfx_tjpgd.c.o
Archiving .pio\build\M5CoreS3\libc5e\libWire.a
src/yolo11n.cpp: In function 'void setup_vlm()':
src/yolo11n.cpp:275:20: error: 'ApiVlmSetupConfig_t' is not a member of 'm5_module_llm'
     m5_module_llm::ApiVlmSetupConfig_t vlm_config;
                    ^~~~~~~~~~~~~~~~~~~
src/yolo11n.cpp:275:20: note: suggested alternative: 'ApiLlmSetupConfig_t'
     m5_module_llm::ApiVlmSetupConfig_t vlm_config;
                    ^~~~~~~~~~~~~~~~~~~
                    ApiLlmSetupConfig_t
src/yolo11n.cpp:276:30: error: 'class M5ModuleLLM' has no member named 'vlm'; did you mean 'llm'?
     vlm_work_id = module_llm.vlm.setup(vlm_config, "vlm_setup");
                              ^~~
                              llm
src/yolo11n.cpp:276:40: error: 'vlm_config' was not declared in this scope
     vlm_work_id = module_llm.vlm.setup(vlm_config, "vlm_setup");
                                        ^~~~~~~~~~
src/yolo11n.cpp:276:40: note: suggested alternative: 'gpio_config'
     vlm_work_id = module_llm.vlm.setup(vlm_config, "vlm_setup");
                                        ^~~~~~~~~~
                                        gpio_config
src/yolo11n.cpp: In function 'void menuBackTask(void*)':
src/yolo11n.cpp:392:62: error: 'class m5_module_llm::ApiYolo' has no member named 'exit'; did you mean 'init'?
                 if (!yolo_work_id.isEmpty()) module_llm.yolo.exit(yolo_work_id);
                                                              ^~~~
                                                              init
src/yolo11n.cpp:393:56: error: 'class M5ModuleLLM' has no member named 'vlm'; did you mean 'llm'?
                 if (!vlm_work_id.isEmpty()) module_llm.vlm.exit(vlm_work_id);
                                                        ^~~
                                                        llm
src/yolo11n.cpp:394:68: error: 'class m5_module_llm::ApiMelotts' has no member named 'exit'; did you mean 'init'?
                 if (!melotts_work_id.isEmpty()) module_llm.melotts.exit(melotts_work_id);
                                                                    ^~~~
                                                                    init
src/yolo11n.cpp: In function 'void button_task(void*)':
src/yolo11n.cpp:541:58: error: 'class m5_module_llm::ApiYolo' has no member named 'exit'; did you mean 'init'?
             if (!yolo_work_id.isEmpty()) module_llm.yolo.exit(yolo_work_id);
                                                          ^~~~
                                                          init
src/yolo11n.cpp:542:52: error: 'class M5ModuleLLM' has no member named 'vlm'; did you mean 'llm'?
             if (!vlm_work_id.isEmpty()) module_llm.vlm.exit(vlm_work_id);
                                                    ^~~
                                                    llm
src/yolo11n.cpp:543:64: error: 'class m5_module_llm::ApiMelotts' has no member named 'exit'; did you mean 'init'?
             if (!melotts_work_id.isEmpty()) module_llm.melotts.exit(melotts_work_id);
                                                                ^~~~
                                                                init
src/yolo11n.cpp: In function 'void cameraTask(void*)':
src/yolo11n.cpp:623:36: error: 'class M5ModuleLLM' has no member named 'vlm'; did you mean 'llm'?
                         module_llm.vlm.inference(vlm_work_id, "请用幽默的方式描述这张图片，字数不超过60个。");
                                    ^~~
                                    llm
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\v1\LGFXBase.cpp.o
Compiling .pio\build\M5CoreS3\libce2\M5GFX\lgfx\v1\LGFX_Button.cpp.o
*** [.pio\build\M5CoreS3\src\yolo11n.cpp.o] Error 1
==================================================== [FAILED] Took 22.55 seconds ====================================================

Environment    Status    Duration
-------------  --------  ------------
M5CoreS3       FAILED    00:00:22.555
=============================================== 1 failed, 0 succeeded in 00:00:22.555 ===============================================

 *  ターミナル プロセス "C:\Users\nemo1\.platformio\penv\Scripts\platformio.exe 'run', '--environment', 'M5CoreS3'" が終了コード 1 で終了しました。 
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```


## 実施②：platformio.iniを編集して、M5ModuleLLMのバージョンをdevリポジトリに変更。以下のようにビルドは成功。


```platformio.ini
[env:M5CoreS3]
build_flags = 
	${env.build_flags}
	-DM5CORES3
lib_deps = 
	arkhipenko/TaskScheduler@^3.8.5
	bblanchon/ArduinoJson@^7.2.1
	m5stack/M5Unified@^0.2.2
	m5stack/M5CoreS3@^1.0.0
#	m5stack/M5Module-LLM@^1.1.0
	https://github.com/m5stack/M5Module-LLM#dev
# M5Module-LLMをdevリポジトリに変更
```

以下のようにビルドは成功。

```
Building .pio\build\M5CoreS3\firmware.bin
esptool.py v4.5.1
Creating esp32s3 image...
Merged 2 ELF sections
Successfully created esp32s3 image.
=================================================== [SUCCESS] Took 122.15 seconds ===================================================

Environment    Status    Duration
-------------  --------  ------------
M5CoreS3       SUCCESS   00:02:02.153
==================================================== 1 succeeded in 00:02:02.153 ====================================================
```

CoreS3に書き込んで起動すると、以下のようにリブートを繰り返す。

```

ELF file SHA256: d093e168be51cf37

E (383) esp_core_dump_flash: Core dump flash config is corrupted! CRC=0x7bd5c66f instead of 0x0
Rebooting...
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x28 (SPI_FAST_FLASH_BOOT)
Saved PC:0x40377b8c
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce3808,len:0x4bc
load:0x403c9700,len:0xbd8
load:0x403cc700,len:0x2a0c
entry 0x403c98d0
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.

Core  0 register dump:
PC      : 0x42010699  PS      : 0x00060f30  A0      : 0x820243e1  A1      : 0x3fceb2d0
A2      : 0x600080c8  A3      : 0x00000000  A4      : 0x00000001  A5      : 0x3fc9aed4
A6      : 0x3fc9e648  A7      : 0x3fceb2b0  A8      : 0x00000000  A9      : 0x3c181328
A10     : 0x00000200  A11     : 0x00000002  A12     : 0x3fc9aa18  A13     : 0x00000001
A14     : 0x00000018  A15     : 0x00000400  SAR     : 0x00000017  EXCCAUSE: 0x0000001c
EXCVADDR: 0x00000000  LBEG    : 0x403760f6  LEND    : 0x40376105  LCOUNT  : 0x00000000


Backtrace: 0x42010696:0x3fceb2d0 0x420243de:0x3fceb2f0 0x403778ef:0x3fceb320 0x403cd86b:0x3fceb350 0x403cdb2a:0x3fceb380 0x403c9925:0x3fceb4b0 0x40045c01:0x3fceb570 0x40043ab6:0x3fceb6f0 0x40034c45:0x3fceb710




ELF file SHA256: d093e168be51cf37

E (383) esp_core_dump_flash: Core dump flash config is corrupted! CRC=0x7bd5c66f instead of 0x0
Rebooting...
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x28 (SPI_FAST_FLASH_BOOT)
Saved PC:0x40377b8c
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce3808,len:0x4bc
load:0x403c9700,len:0xbd8
load:0x403cc700,len:0x2a0c
entry 0x403c98d0
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.

Core  0 register dump:
PC      : 0x42010699  PS      : 0x00060f30  A0      : 0x820243e1  A1      : 0x3fceb2d0
A2      : 0x600080c8  A3      : 0x00000000  A4      : 0x00000001  A5      : 0x3fc9aed4
A6      : 0x3fc9e648  A7      : 0x3fceb2b0  A8      : 0x00000000  A9      : 0x3c181328
A10     : 0x00000200  A11     : 0x00000002  A12     : 0x3fc9aa18  A13     : 0x00000001
A14     : 0x00000018  A15     : 0x00000400  SAR     : 0x00000017  EXCCAUSE: 0x0000001c
EXCVADDR: 0x00000000  LBEG    : 0x403760f6  LEND    : 0x40376105  LCOUNT  : 0x00000000


Backtrace: 0x42010696:0x3fceb2d0 0x420243de:0x3fceb2f0 0x403778ef:0x3fceb320 0x403cd86b:0x3fceb350 0x403cdb2a:0x3fceb380 0x403c9925:0x3fceb4b0 0x40045c01:0x3fceb570 0x40043ab6:0x3fceb6f0 0x40034c45:0x3fceb710




ELF file SHA256: d093e168be51cf37

E (383) esp_core_dump_flash: Core dump flash config is corrupted! CRC=0x7bd5c66f instead of 0x0
Rebooting...
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x28 (SPI_FAST_FLASH_BOOT)
Saved PC:0x40377b8c
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce3808,len:0x4bc
load:0x403c9700,len:0xbd8
load:0x403cc700,len:0x2a0c
entry 0x403c98d0
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.

Core  0 register dump:
PC      : 0x42010699  PS      : 0x00060f30  A0      : 0x820243e1  A1      : 0x3fceb2d0
A2      : 0x600080c8  A3      : 0x00000000  A4      : 0x00000001  A5      : 0x3fc9aed4
A6      : 0x3fc9e648  A7      : 0x3fceb2b0  A8      : 0x00000000  A9      : 0x3c181328
A10     : 0x00000200  A11     : 0x00000002  A12     : 0x3fc9aa18  A13     : 0x00000001
A14     : 0x00000018  A15     : 0x00000400  SAR     : 0x00000017  EXCCAUSE: 0x0000001c
EXCVADDR: 0x00000000  LBEG    : 0x403760f6  LEND    : 0x40376105  LCOUNT  : 0x00000000


Backtrace: 0x42010696:0x3fceb2d0 0x420243de:0x3fceb2f0 0x403778ef:0x3fceb320 0x403cd86b:0x3fceb350 0x403cdb2a:0x3fceb380 0x403c9925:0x3fceb4b0 0x40045c01:0x3fceb570 0x40043ab6:0x3fceb6f0 0x40034c45:0x3fceb710




ELF file SHA256: d093e168be51cf37

E (383) esp_core_dump_flash: Core dump flash config is corrupted! CRC=0x7bd5c66f instead of 0x0
Rebooting...
ESP-ROM:esp32s3-20210327
Build:Mar 27 2021
rst:0xc (RTC_SW_CPU_RST),boot:0x28 (SPI_FAST_FLASH_BOOT)
Saved PC:0x40377b8c
SPIWP:0xee
mode:DIO, clock div:1
load:0x3fce3808,len:0x4bc
load:0x403c9700,len:0xbd8
load:0x403cc700,len:0x2a0c
entry 0x403c98d0
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.

Core  0 register dump:
PC      : 0x42010699  PS      : 0x00060f30  A0      : 0x820243e1  A1      : 0x3fceb2d0
A2      : 0x600080c8  A3      : 0x00000000  A4      : 0x00000001  A5      : 0x3fc9aed4
A6      : 0x3fc9e648  A7      : 0x3fceb2b0  A8      : 0x00000000  A9      : 0x3c181328
A10     : 0x00000200  A11     : 0x00000002  A12     : 0x3fc9aa18  A13     : 0x00000001
A14     : 0x00000018  A15     : 0x00000400  SAR     : 0x00000017  EXCCAUSE: 0x0000001c
EXCVADDR: 0x00000000  LBEG    : 0x403760f6  LEND    : 0x40376105  LCOUNT  : 0x00000000


Backtrace: 0x42010696:0x3fceb2d0 0x420243de:0x3fceb2f0 0x403778ef:0x3fceb320 0x403cd86b:0x3fceb350 0x403cdb2a:0x3fceb380 0x403c9925:0x3fceb4b0 0x40045c01:0x3fceb570 0x40043ab6:0x3fceb6f0 0x40034c45:0x3fceb710


```

