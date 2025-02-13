## 概要

M5CoreS3を購入し、YOLOのカメラサンプル(ESP32/cpp/src/yolo11n.cpp)を動かしてみましたが、
試してみたところ、不具合あり。(25/01/18)
以下を対処して動いた。

 * NG：VSCode+PlatformIOでのビルドの実行→M5ModuleLLMのバージョンが古いことでのコンパイルエラー発生。

 * https://github.com/Abandon-ht/ModuleLLM_Development_Guide/tree/dev　から、ファイルを一式ダウンロード
 * ライブラリ M5ModuleLLMのバージョンが古い -> M5Stack のdevバージョンを参照する (https://github.com/m5stack/M5Module-LLM/tree/dev)
 * PlatformIOでビルドするとCoreS3がクラッシュし続ける
   、パーティションテーブルの問題。.cppファイルを.inoファイルに修正し、Arduinoを使ってコンパイルすることで回避。

 * シリアルポートのボーレートを修正する（1500000がある->115200)
 * https://github.com/Abandon-ht/ModuleLLM_Development_Guide/blob/dev/ESP32/cpp/src/yolo11n.cpp#L184
 
 * #define Serial USBSerial  を消す。 ArduinoIDEでは不要。
 * https://github.com/Abandon-ht/ModuleLLM_Development_Guide/blob/dev/ESP32/cpp/src/yolo11n.cpp#L32
   
 * VLMを動かすには、DualButtonを買ってPortBにさす。
 * YOLOを動かすにはCoreS3を使う。カメラが必要。
https://x.com/nnn112358/status/1885479805417906567
https://x.com/nnn112358/status/1880573851526107537


