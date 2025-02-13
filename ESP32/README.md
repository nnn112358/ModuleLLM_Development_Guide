## 概要

M5CoreS3を購入し、YOLOのカメラサンプル(ESP32/cpp/src/yolo11n.cpp)を動かしてみましたが、
試してみたところ、不具合あり。(25/01/18)<br>
以下を対処して動いた。(2/1)

### 最初
NG：VSCode+PlatformIOでのビルドの実行→M5ModuleLLMのバージョンが古いことでのコンパイルエラー発生。

### 対処:
 * (https://github.com/Abandon-ht/ModuleLLM_Development_Guide/tree/dev) から、ファイルを一式ダウンロード
 * ライブラリ M5ModuleLLMのバージョンが古い -> M5Stack のdevバージョンを参照する (https://github.com/m5stack/M5Module-LLM/tree/dev)
 * PlatformIOでビルドするとCoreS3がクラッシュし続ける
   おそらく、パーティションテーブルの問題。.cppファイルを.inoファイルに修正し、Arduinoを使ってコンパイルすることで回避。

 * シリアルポートのボーレートを修正する（1500000がある->115200)
 * https://github.com/Abandon-ht/ModuleLLM_Development_Guide/blob/dev/ESP32/cpp/src/yolo11n.cpp#L184
 
 * #define Serial USBSerial  を消す。 ArduinoIDEでは不要。
 * https://github.com/Abandon-ht/ModuleLLM_Development_Guide/blob/dev/ESP32/cpp/src/yolo11n.cpp#L32
 
 *char jsonBuffer[JSON_BUFFER_SIZE]; がライブラリで名前が干渉しているとエラー。　jsonBuffer->_jsonBuffer　に変更。
 
 * VLMを動かすには、DualButtonを買ってPortBにさす。
 * YOLOを動かすにはCoreS3を使う。カメラが必要。
 * 
### 動作の様子:
https://x.com/nnn112358/status/1885479805417906567<br>
https://x.com/nnn112358/status/1880573851526107537<br>


