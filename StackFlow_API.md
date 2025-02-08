# 概要

LLMモジュールは、KWS（キーワード検出）、ASR（音声認識）、LLM（大規模言語モデル）、TTS（音声合成）などの機能ユニットを統合しています。各ユニットは独立したモジュールとして動作することも、データワークフローの統合のための設定をサポートすることもでき、よりインテリジェントなインタラクティブアプリケーションを実現できます。このモジュールはUART通信を介してホストデバイスと対話し、JSONフォーマットのデータパケットを使用するため、非常に使いやすい設計となっています。

## 内蔵機能ユニット

| ユニット | ユニット名 | 機能 |
|----------|------------|------|
| sys | システム | モジュールパラメータの設定、モジュールステータスの取得 |
| kws | キーワード検出 | 音声内のキーワードの検出 |
| asr | 音声認識 | 音声をテキストに変換 |
| llm | 生成モデル | 入力テキストに基づいて新しいテキストを生成 |
| tts | 音声合成 | テキストを音声に変換 |
| audio | システム音声インターフェース | マイク音声へのアクセスと音声再生 |

## 使用手順

1. モジュールをM5Stackメインコントローラ（Basic/M5Core2/M5Core3など）とスタックするか、USB-TTLコンバータを使用してTX/RXと電源に直接接続します。正常に起動すると、モジュールは緑色に点灯します。

2. プログラムでUARTインターフェースを初期化します（ピン設定は実際に接続されているデバイスに基づき、インターフェース設定は115200bps 8N1）。

3. 以下の使用例を参照し、初期化フレームを送信して目的のユニットサービスを有効化します。

## 通信インターフェース

LLMモジュールのUARTインターフェースは、デフォルトで115200bps 8N1に設定されています。

## データパケットフォーマット

### 送信フレームの基本構造
```json
{
    "request_id": "001", 
    "work_id": "llm.1001",
    "action": "taskinfo",
    "object": "None",
    "data": "None"
}
```

- request_id: コンテキストを区別するためのセッションID
- work_id: サービス呼び出し時はキーワード+ID（例：llm.xxxx）、セットアップ時はユニット名のみ
- action: 呼び出すメソッド
- object: dataで渡すパラメータの構造を設定
- data: 送信するパラメータ

[以下、各ユニット（SYS、AUDIO、KWS、ASR、LLM、TTS）の詳細な仕様と設定方法、アプリケーション例が続きます...]

# エラーコード

| コード | 説明 | メッセージ |
|--------|------|------------|
| 0 | 操作成功 | Operation Successful! |
| -1 | 通信チャネル受信状態マシンリセット警告 | reace reset |
| -2 | JSON解析エラー | JSON format error |
| -3 | sysアクションマッチエラー | action match false |
| -4 | 推論データプッシュエラー | inference data push false |
| -5 | モデルの読み込み失敗 | Model loading failed |
| -6 | ユニットが存在しない | Unit Does Not Exist |
| -7 | 不明な操作 | Unknown Operation |
| -8 | ユニットリソース割り当て失敗 | Unit Resource Allocation Failed |
| -9 | ユニット呼び出し失敗 | unit call false |
| -10 | モデル初期化失敗 | Model init failed |
| -11 | モデル実行エラー | Model run failed |
| -12 | モジュール未初期化 | Module has not been initialised |
| -13 | モジュールが既に動作中 | Module already working |
| -14 | モジュールが動作していない | Module is not working |
| -19 | ユニットリソース解放失敗 | Unit Resource Free Failed |

# アプリケーション例

## テキスト音声変換
TTSユニットを使用してテキストを音声に変換します。

## テキストアシスタント
テキストをLLMモデルに入力し、推論を処理し、音声として再生します（LLM+TTS）。

## 音声アシスタント
KWSで起動 → ASRで音声をテキストに変換 → 変換したコンテンツをLLMの入力として推論 → 最後に推論結果をTTSで音声出力します（KWS+ASR+LLM+TTS）。



# SYSユニット

SYSユニットは、モジュールの動作パラメータの設定とモジュールの動作情報の取得に使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| lsmode | 利用可能なモデルの取得 | なし | sys.lsmode |
| hwinfo | CPU負荷、メモリ負荷、チップ温度の取得 | なし | sys.hwinfo |
| reset | ユニットのリセット | なし | リセット完了JSON |
| reboot | システムの再起動 | なし | なし |
| ping | システムの応答確認 | なし | なし |

### lsmode
利用可能なモデルを取得するコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "lsmode"
}
```

応答例：
```json
{
    "created": 1692652687,
    "data": [
        {
            "capabilities": [
                "Automatic_Speech_Recognition"
            ],
            "input_type": [
                "sys.pcm"
            ],
            "model": "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23",
            "output_type": [
                "asr.utf-8"
            ],
            "type": "asr"
        },
        ... [その他のモデル情報]
    ],
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "sys.lsmode",
    "request_id": "001",
    "work_id": "sys"
}
```

### hwinfo
CPU負荷、メモリ負荷、チップ温度を取得するコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "hwinfo"
}
```

応答例（CPU負荷0%、メモリ18%、温度46°C）：
```json
{
    "created": 1692652642,
    "data": {
        "cpu_loadavg": 0,
        "mem": 18,
        "temperature": 46350
    },
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "sys.hwinfo",
    "request_id": "001",
    "work_id": "sys"
}
```

### reset
システムリセットコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "reset"
}
```

リセット開始応答：
```json
{
    "created": 1692652712,
    "error": {
        "code": 0,
        "message": "llm server restarting ..."
    },
    "request_id": "001",
    "work_id": "sys"
}
```

リセット完了応答：
```json
{
    "request_id": "0",
    "work_id": "sys",
    "created": 1692652723,
    "error": {
        "code": 0,
        "message": "reset over"
    }
}
```

### reboot
システム完全再起動コマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "reboot"
}
```

再起動コマンド応答：
```json
{
    "created": 1692652822,
    "error": {
        "code": 0,
        "message": "rebooting ..."
    },
    "request_id": "001",
    "work_id": "sys"
}
```

注意：応答メッセージの後、システムは再起動します。再起動中にV0EUEURSという文字列が送信されますが、これはシステム起動文字列であり、無視して構いません。

### ping
システムサービスの通信テスト。モジュール電源投入後の通信状態確認に有用です：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "ping"
}
```

応答例：
```json
{
    "created": 1692652310,
    "error": {
        "code": 0,
        "message": ""
    },
    "request_id": "001",
    "work_id": "sys"
}
```

# AUDIOユニット

AUDIOユニットは、システムのサウンドカードを制御し、マイク音声へのアクセスと音声再生を行います。キーワード検出（KWS）と自動音声認識（ASR）ユニットの音声入力、および音声合成（TTS）モジュールの音声出力を提供します。KWSとASRユニットを使用する前に、AUDIOユニットを初期化する必要があります。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | 音声ユニットの設定 | audio.setup | なし（成功したwork_idを含む応答を返す） |
| exit | work_idの作業終了 | なし | なし |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | audio.taskinfo |

### setup
Audioユニットを初期化し、再生音量とサウンドカードスロット番号を設定します。

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| capcard | マイクサウンドカードインデックス | デフォルトシステムサウンドカード：0 |
| capdevice | マイクデバイスインデックス | オンボードシリコンマイク：0 |
| capVolume | 入力音量 | 0.0～10.0（1以上で増幅、デフォルト0.5） |
| playcard | スピーカーサウンドカードインデックス | デフォルトシステムサウンドカード：0 |
| playdevice | スピーカーデバイスインデックス | オンボードスピーカー：1 |
| playVolume | 出力音量 | 0.0～10.0（1以上で増幅、デフォルト0.5） |

設定コマンド例：
```json
{
    "request_id": "1",
    "work_id": "audio",
    "action": "setup",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.5
    }
}
```

初期化応答：
```json
{
    "created": 1692659008,
    "error": {
        "code": 0,
        "message": "audio setup successful"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### pause
Audioユニット一時停止コマンド：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692659049,
    "error": {
        "code": 0,
        "message": "audio pause"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### work
Audioユニット開始コマンド：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "work",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.25
    }
}
```

開始応答：
```json
{
    "created": 1692659297,
    "error": {
        "code": 0,
        "message": "audio work start"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### exit
Audioユニットの終了と解放：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692659370,
    "error": {
        "code": 0,
        "message": "audio exit"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### taskinfo
Audioユニットの状態照会：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692659454,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

停止中の応答：
```json
{
    "created": 1692659499,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

解放済みの応答：
```json
{
    "created": 1692659403,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```
# KWSユニット

KWSユニットはキーワード検出に使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | KWSユニットの設定 | kws.setup | なし（成功したwork_idを含む応答を返す） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | kws.taskinfo |

### setup
KWSユニットを初期化し、中国語/英語認識モデルを設定します。
（注意：KWSキーワードフィールドでは中国語/英語の混在は許可されません）

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | 英語モデル: "sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01"<br>中国語モデル: "sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01" |
| kws | KWSキーワードテキスト | 中国語/英語の混在不可、英語は大文字のみ |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

英語認識モデルでのKWS設定例：
```json
{
    "request_id": "2",
    "work_id": "kws",
    "action": "setup",
    "object": "kws.setup",
    "data": {
        "model": "sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01",
        "response_format": "kws.bool",
        "input": "sys.pcm",
        "enoutput": true,
        "kws": "HELLO"
    }
}
```

初期化応答（注：セットアップ処理には約9秒かかります）：
```json
{
    "created": 1692660576,
    "error": {
        "code": 0,
        "message": "kws setup successful"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

キーワード検出時の応答：
```json
{
    "created": 1692660576,
    "error": {
        "code": 0,
        "message": "kws setup successful"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### pause
KWSユニット一時停止コマンド：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692660626,
    "error": {
        "code": 0,
        "message": "kws pause"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### work
KWSユニット開始コマンド：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692660651,
    "error": {
        "code": 0,
        "message": "kws work"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### exit
KWSユニットの終了と解放：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692654383,
    "error": {
        "code": 0,
        "message": "kws exit"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### taskinfo
KWSユニットの状態照会：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692654305,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.1001"
}
```

停止中の応答：
```json
{
    "created": 1692654535,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.1001"
}
```

解放済みの応答：
```json
{
    "created": 1692654452,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.0"
}
```

# ASRユニット

ASRユニットは音声をテキストに変換するために使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | ASRユニットの設定 | asr.setup | なし（成功したwork_idを含む応答を返す） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | asr.taskinfo |

### setup

ASRユニットを初期化し、中国語/英語モデルを設定します。

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | 英語モデル: "sherpa-ncnn-streaming-zipformer-20M-2023-02-17"<br>中国語モデル: "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23" |
| response_format | 出力フォーマット | 標準出力: "asr.utf-8"<br>ストリーミング出力: "asr.utf-8.stream" |
| input | 入力 | LLM入力: "llm.xxx"（llmユニットのwork_id）<br>UART入力: "tts.utf-8"<br>UARTストリーミング入力: "tts.utf-8.stream" |
| enkws | KWSによる起動の有効化 | KWSで起動後ASR実行: true<br>KWS起動なし、ASRは継続的に動作: false |
| rule1 | 起動から未認識コンテンツまでのタイムアウト | 単位：秒 |
| rule2 | 認識の最大間隔時間 | 単位：秒 |
| rule3 | 認識の最大タイムアウト | 単位：秒 |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

英語モデルでのASR設定例：
```json
{
    "request_id": "3",
    "work_id": "asr",
    "action": "setup",
    "object": "asr.setup",
    "data": {
        "model": "sherpa-ncnn-streaming-zipformer-20M-2023-02-17",
        "response_format": "asr.utf-8",
        "input": "sys.pcm",
        "enoutput": true,
        "enkws": true,
        "rule1": 2.4,
        "rule2": 1.2,
        "rule3": 30
    }
}
```

ASRユニット初期化応答：
```json
{
    "created": 1692667736,
    "error": {
        "code": 0,
        "message": "asr setup successful"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

ASR認識応答：
```json
{
    "created": 1692655176,
    "data": {
        "delta": " hello",
        "index": "0"
    },
    "object": "asr.stream",
    "request_id": "004",
    "work_id": "asr.1003"
}
```

### pause
ASRユニット一時停止コマンド：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692670174,
    "error": {
        "code": 0,
        "message": "asr pause"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### work
ASRユニット開始コマンド：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692670213,
    "error": {
        "code": 0,
        "message": "asr work"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### exit
ASRユニットの終了と解放：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692670254,
    "error": {
        "code": 0,
        "message": "asr exit"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### taskinfo
ASRユニットの状態照会：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692669923,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.1002"
}
```

停止中の応答：
```json
{
    "created": 1692653792,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.1002"
}
```

解放済みの応答：
```json
{
    "created": 1692669874,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.0"
}
```# 概要

LLMモジュールは、KWS（キーワード検出）、ASR（音声認識）、LLM（大規模言語モデル）、TTS（音声合成）などの機能ユニットを統合しています。各ユニットは独立したモジュールとして動作することも、データワークフローの統合のための設定をサポートすることもでき、よりインテリジェントなインタラクティブアプリケーションを実現できます。このモジュールはUART通信を介してホストデバイスと対話し、JSONフォーマットのデータパケットを使用するため、非常に使いやすい設計となっています。

## 内蔵機能ユニット

| ユニット | ユニット名 | 機能 |
|----------|------------|------|
| sys | システム | モジュールパラメータの設定、モジュールステータスの取得 |
| kws | キーワード検出 | 音声内のキーワードの検出 |
| asr | 音声認識 | 音声をテキストに変換 |
| llm | 生成モデル | 入力テキストに基づいて新しいテキストを生成 |
| tts | 音声合成 | テキストを音声に変換 |
| audio | システム音声インターフェース | マイク音声へのアクセスと音声再生 |

## 使用手順

1. モジュールをM5Stackメインコントローラ（Basic/M5Core2/M5Core3など）とスタックするか、USB-TTLコンバータを使用してTX/RXと電源に直接接続します。正常に起動すると、モジュールは緑色に点灯します。

2. プログラムでUARTインターフェースを初期化します（ピン設定は実際に接続されているデバイスに基づき、インターフェース設定は115200bps 8N1）。

3. 以下の使用例を参照し、初期化フレームを送信して目的のユニットサービスを有効化します。

## 通信インターフェース

LLMモジュールのUARTインターフェースは、デフォルトで115200bps 8N1に設定されています。

## データパケットフォーマット

### 送信フレームの基本構造
```json
{
    "request_id": "001", 
    "work_id": "llm.1001",
    "action": "taskinfo",
    "object": "None",
    "data": "None"
}
```

- request_id: コンテキストを区別するためのセッションID
- work_id: サービス呼び出し時はキーワード+ID（例：llm.xxxx）、セットアップ時はユニット名のみ
- action: 呼び出すメソッド
- object: dataで渡すパラメータの構造を設定
- data: 送信するパラメータ

[以下、各ユニット（SYS、AUDIO、KWS、ASR、LLM、TTS）の詳細な仕様と設定方法、アプリケーション例が続きます...]

# エラーコード

| コード | 説明 | メッセージ |
|--------|------|------------|
| 0 | 操作成功 | Operation Successful! |
| -1 | 通信チャネル受信状態マシンリセット警告 | reace reset |
| -2 | JSON解析エラー | JSON format error |
| -3 | sysアクションマッチエラー | action match false |
| -4 | 推論データプッシュエラー | inference data push false |
| -5 | モデルの読み込み失敗 | Model loading failed |
| -6 | ユニットが存在しない | Unit Does Not Exist |
| -7 | 不明な操作 | Unknown Operation |
| -8 | ユニットリソース割り当て失敗 | Unit Resource Allocation Failed |
| -9 | ユニット呼び出し失敗 | unit call false |
| -10 | モデル初期化失敗 | Model init failed |
| -11 | モデル実行エラー | Model run failed |
| -12 | モジュール未初期化 | Module has not been initialised |
| -13 | モジュールが既に動作中 | Module already working |
| -14 | モジュールが動作していない | Module is not working |
| -19 | ユニットリソース解放失敗 | Unit Resource Free Failed |

# アプリケーション例

## テキスト音声変換
TTSユニットを使用してテキストを音声に変換します。

## テキストアシスタント
テキストをLLMモデルに入力し、推論を処理し、音声として再生します（LLM+TTS）。

## 音声アシスタント
KWSで起動 → ASRで音声をテキストに変換 → 変換したコンテンツをLLMの入力として推論 → 最後に推論結果をTTSで音声出力します（KWS+ASR+LLM+TTS）。



# SYSユニット

SYSユニットは、モジュールの動作パラメータの設定とモジュールの動作情報の取得に使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| lsmode | 利用可能なモデルの取得 | なし | sys.lsmode |
| hwinfo | CPU負荷、メモリ負荷、チップ温度の取得 | なし | sys.hwinfo |
| reset | ユニットのリセット | なし | リセット完了JSON |
| reboot | システムの再起動 | なし | なし |
| ping | システムの応答確認 | なし | なし |

### lsmode
利用可能なモデルを取得するコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "lsmode"
}
```

応答例：
```json
{
    "created": 1692652687,
    "data": [
        {
            "capabilities": [
                "Automatic_Speech_Recognition"
            ],
            "input_type": [
                "sys.pcm"
            ],
            "model": "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23",
            "output_type": [
                "asr.utf-8"
            ],
            "type": "asr"
        },
        ... [その他のモデル情報]
    ],
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "sys.lsmode",
    "request_id": "001",
    "work_id": "sys"
}
```

### hwinfo
CPU負荷、メモリ負荷、チップ温度を取得するコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "hwinfo"
}
```

応答例（CPU負荷0%、メモリ18%、温度46°C）：
```json
{
    "created": 1692652642,
    "data": {
        "cpu_loadavg": 0,
        "mem": 18,
        "temperature": 46350
    },
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "sys.hwinfo",
    "request_id": "001",
    "work_id": "sys"
}
```

### reset
システムリセットコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "reset"
}
```

リセット開始応答：
```json
{
    "created": 1692652712,
    "error": {
        "code": 0,
        "message": "llm server restarting ..."
    },
    "request_id": "001",
    "work_id": "sys"
}
```

リセット完了応答：
```json
{
    "request_id": "0",
    "work_id": "sys",
    "created": 1692652723,
    "error": {
        "code": 0,
        "message": "reset over"
    }
}
```

### reboot
システム完全再起動コマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "reboot"
}
```

再起動コマンド応答：
```json
{
    "created": 1692652822,
    "error": {
        "code": 0,
        "message": "rebooting ..."
    },
    "request_id": "001",
    "work_id": "sys"
}
```

注意：応答メッセージの後、システムは再起動します。再起動中にV0EUEURSという文字列が送信されますが、これはシステム起動文字列であり、無視して構いません。

### ping
システムサービスの通信テスト。モジュール電源投入後の通信状態確認に有用です：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "ping"
}
```

応答例：
```json
{
    "created": 1692652310,
    "error": {
        "code": 0,
        "message": ""
    },
    "request_id": "001",
    "work_id": "sys"
}
```

# AUDIOユニット

AUDIOユニットは、システムのサウンドカードを制御し、マイク音声へのアクセスと音声再生を行います。キーワード検出（KWS）と自動音声認識（ASR）ユニットの音声入力、および音声合成（TTS）モジュールの音声出力を提供します。KWSとASRユニットを使用する前に、AUDIOユニットを初期化する必要があります。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | 音声ユニットの設定 | audio.setup | なし（成功したwork_idを含む応答を返す） |
| exit | work_idの作業終了 | なし | なし |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | audio.taskinfo |

### setup
Audioユニットを初期化し、再生音量とサウンドカードスロット番号を設定します。

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| capcard | マイクサウンドカードインデックス | デフォルトシステムサウンドカード：0 |
| capdevice | マイクデバイスインデックス | オンボードシリコンマイク：0 |
| capVolume | 入力音量 | 0.0～10.0（1以上で増幅、デフォルト0.5） |
| playcard | スピーカーサウンドカードインデックス | デフォルトシステムサウンドカード：0 |
| playdevice | スピーカーデバイスインデックス | オンボードスピーカー：1 |
| playVolume | 出力音量 | 0.0～10.0（1以上で増幅、デフォルト0.5） |

設定コマンド例：
```json
{
    "request_id": "1",
    "work_id": "audio",
    "action": "setup",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.5
    }
}
```

初期化応答：
```json
{
    "created": 1692659008,
    "error": {
        "code": 0,
        "message": "audio setup successful"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### pause
Audioユニット一時停止コマンド：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692659049,
    "error": {
        "code": 0,
        "message": "audio pause"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### work
Audioユニット開始コマンド：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "work",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.25
    }
}
```

開始応答：
```json
{
    "created": 1692659297,
    "error": {
        "code": 0,
        "message": "audio work start"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### exit
Audioユニットの終了と解放：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692659370,
    "error": {
        "code": 0,
        "message": "audio exit"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### taskinfo
Audioユニットの状態照会：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692659454,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

停止中の応答：
```json
{
    "created": 1692659499,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

解放済みの応答：
```json
{
    "created": 1692659403,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

# LLMユニット

LLM（大規模言語モデル）ユニットは、入力テキストに基づいて応答を生成することができます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | LLMユニットの設定 | llm.setup | なし（成功したwork_idを含む応答を返す） |
| inference | 推論の実行 | 通常: llm.utf-8（モデルの違いはsys.lsmodeで確認可能） | なし（データ送信結果のみを返す。最終的な推論結果は設定に依存） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | llm.taskinfo |

### setup
LLMユニットを初期化し、指定したモデルを設定します。現在プリインストールされているモデル：
- qwen2.5-0.5b

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | プリインストールモデル "qwen2.5-0.5b" |
| response_format | 出力フォーマット | 標準出力: "llm.utf-8"<br>ストリーミング出力: "llm.utf-8.stream" |
| input | 入力 | ASR入力: "asr.xxx"（ASRユニットのwork_id）<br>UART入力: "llm.utf-8"<br>UARTストリーミング入力: "llm.utf-8.stream" |
| enkws | 進行中のプロセスのKWSによる中断 | KWSで中断: true<br>KWSで中断しない: false |
| max_length | 最大出力トークン長の設定 | 最大: 1024, 推奨: 127 |
| prompt | モデル初期化プロンプト | - |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

#### ASRからの入力設定
ASR（音声認識）を入力データとして設定するLLMユニットの初期化：
```json
{
    "request_id": "4",
    "work_id": "llm",
    "action": "setup",
    "object": "llm.setup",
    "data": {
        "model": "qwen2.5-0.5b",
        "response_format": "llm.utf-8.stream",
        "input": "asr.1001",
        "enoutput": true,
        "enkws": true,
        "max_token_len": 127,
        "prompt": "You are a knowledgeable assistant capable of answering various questions and providing information."       
    }
}
```

#### UARTからの入力設定
UARTインターフェースを入力データとして設定するLLMユニットの初期化：
```json
{
    "request_id": "4",
    "work_id": "llm",
    "action": "setup",
    "object": "llm.setup",
    "data": {
        "model": "qwen2.5-0.5b",
        "response_format": "llm.utf-8",
        "input": "llm.utf-8.stream",
        "enoutput": true,
        "enkws": true,
        "max_token_len": 127,
        "prompt": "You are a knowledgeable assistant capable of answering various questions and providing information."
    }
}
```

LLMユニット初期化応答：
```json
{
    "created": 1692664107,
    "data": "None",
    "error": {
        "code": 0,
        "message": "llm setup successful"
    },
    "object": "None",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### inference
UART経由で推論データを送信：

ストリーミング入力の例：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "inference",
    "object": "llm.utf-8.stream",
    "data": {
        "delta": "What's ur name?",
        "index": 0,
        "finish": true
    }
}
```

非ストリーミング入力の例：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "inference",
    "object": "llm.utf-8",
    "data": "What's ur name?"
}
```

推論応答データ：
```json
{
    "created": 1692664605,
    "data": {
        "delta": "I'm not a person, but I'm here to help with any questions you may have. How can I assist you today?\n",
        "finish": true,
        "index": 0
    },
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.utf-8.stream",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### pause
LLMユニット一時停止コマンド：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692664941,
    "error": {
        "code": 0,
        "message": "llm pause"
    },
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### work
LLMユニット開始コマンド：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692664972,
    "error": {
        "code": 0,
        "message": "llm work"
    },
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### exit
LLMユニットの終了と解放：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692664858,
    "data": "None",
    "error": {
        "code": 0,
        "message": "llm exit"
    },
    "object": "None",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### taskinfo
LLMユニットの状態照会：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692664730,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.state",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

停止中の応答：
```json
{
    "created": 1692664823,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.state",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

解放済みの応答：
```json
{
    "created": 1692664881,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.state",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

# KWSユニット

KWSユニットはキーワード検出に使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | KWSユニットの設定 | kws.setup | なし（成功したwork_idを含む応答を返す） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | kws.taskinfo |

### setup
KWSユニットを初期化し、中国語/英語認識モデルを設定します。
（注意：KWSキーワードフィールドでは中国語/英語の混在は許可されません）

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | 英語モデル: "sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01"<br>中国語モデル: "sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01" |
| kws | KWSキーワードテキスト | 中国語/英語の混在不可、英語は大文字のみ |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

英語認識モデルでのKWS設定例：
```json
{
    "request_id": "2",
    "work_id": "kws",
    "action": "setup",
    "object": "kws.setup",
    "data": {
        "model": "sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01",
        "response_format": "kws.bool",
        "input": "sys.pcm",
        "enoutput": true,
        "kws": "HELLO"
    }
}
```

初期化応答（注：セットアップ処理には約9秒かかります）：
```json
{
    "created": 1692660576,
    "error": {
        "code": 0,
        "message": "kws setup successful"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

キーワード検出時の応答：
```json
{
    "created": 1692660576,
    "error": {
        "code": 0,
        "message": "kws setup successful"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### pause
KWSユニット一時停止コマンド：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692660626,
    "error": {
        "code": 0,
        "message": "kws pause"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### work
KWSユニット開始コマンド：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692660651,
    "error": {
        "code": 0,
        "message": "kws work"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### exit
KWSユニットの終了と解放：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692654383,
    "error": {
        "code": 0,
        "message": "kws exit"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### taskinfo
KWSユニットの状態照会：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692654305,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.1001"
}
```

停止中の応答：
```json
{
    "created": 1692654535,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.1001"
}
```

解放済みの応答：
```json
{
    "created": 1692654452,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.0"
}
```

# ASRユニット

ASRユニットは音声をテキストに変換するために使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | ASRユニットの設定 | asr.setup | なし（成功したwork_idを含む応答を返す） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | asr.taskinfo |

### setup

ASRユニットを初期化し、中国語/英語モデルを設定します。

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | 英語モデル: "sherpa-ncnn-streaming-zipformer-20M-2023-02-17"<br>中国語モデル: "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23" |
| response_format | 出力フォーマット | 標準出力: "asr.utf-8"<br>ストリーミング出力: "asr.utf-8.stream" |
| input | 入力 | LLM入力: "llm.xxx"（llmユニットのwork_id）<br>UART入力: "tts.utf-8"<br>UARTストリーミング入力: "tts.utf-8.stream" |
| enkws | KWSによる起動の有効化 | KWSで起動後ASR実行: true<br>KWS起動なし、ASRは継続的に動作: false |
| rule1 | 起動から未認識コンテンツまでのタイムアウト | 単位：秒 |
| rule2 | 認識の最大間隔時間 | 単位：秒 |
| rule3 | 認識の最大タイムアウト | 単位：秒 |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

英語モデルでのASR設定例：
```json
{
    "request_id": "3",
    "work_id": "asr",
    "action": "setup",
    "object": "asr.setup",
    "data": {
        "model": "sherpa-ncnn-streaming-zipformer-20M-2023-02-17",
        "response_format": "asr.utf-8",
        "input": "sys.pcm",
        "enoutput": true,
        "enkws": true,
        "rule1": 2.4,
        "rule2": 1.2,
        "rule3": 30
    }
}
```

ASRユニット初期化応答：
```json
{
    "created": 1692667736,
    "error": {
        "code": 0,
        "message": "asr setup successful"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

ASR認識応答：
```json
{
    "created": 1692655176,
    "data": {
        "delta": " hello",
        "index": "0"
    },
    "object": "asr.stream",
    "request_id": "004",
    "work_id": "asr.1003"
}
```

### pause
ASRユニット一時停止コマンド：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692670174,
    "error": {
        "code": 0,
        "message": "asr pause"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### work
ASRユニット開始コマンド：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692670213,
    "error": {
        "code": 0,
        "message": "asr work"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### exit
ASRユニットの終了と解放：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692670254,
    "error": {
        "code": 0,
        "message": "asr exit"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### taskinfo
ASRユニットの状態照会：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692669923,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.1002"
}
```

停止中の応答：
```json
{
    "created": 1692653792,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.1002"
}
```

解放済みの応答：
```json
{
    "created": 1692669874,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.0"
}
```# 概要

LLMモジュールは、KWS（キーワード検出）、ASR（音声認識）、LLM（大規模言語モデル）、TTS（音声合成）などの機能ユニットを統合しています。各ユニットは独立したモジュールとして動作することも、データワークフローの統合のための設定をサポートすることもでき、よりインテリジェントなインタラクティブアプリケーションを実現できます。このモジュールはUART通信を介してホストデバイスと対話し、JSONフォーマットのデータパケットを使用するため、非常に使いやすい設計となっています。

## 内蔵機能ユニット

| ユニット | ユニット名 | 機能 |
|----------|------------|------|
| sys | システム | モジュールパラメータの設定、モジュールステータスの取得 |
| kws | キーワード検出 | 音声内のキーワードの検出 |
| asr | 音声認識 | 音声をテキストに変換 |
| llm | 生成モデル | 入力テキストに基づいて新しいテキストを生成 |
| tts | 音声合成 | テキストを音声に変換 |
| audio | システム音声インターフェース | マイク音声へのアクセスと音声再生 |

## 使用手順

1. モジュールをM5Stackメインコントローラ（Basic/M5Core2/M5Core3など）とスタックするか、USB-TTLコンバータを使用してTX/RXと電源に直接接続します。正常に起動すると、モジュールは緑色に点灯します。

2. プログラムでUARTインターフェースを初期化します（ピン設定は実際に接続されているデバイスに基づき、インターフェース設定は115200bps 8N1）。

3. 以下の使用例を参照し、初期化フレームを送信して目的のユニットサービスを有効化します。

## 通信インターフェース

LLMモジュールのUARTインターフェースは、デフォルトで115200bps 8N1に設定されています。

## データパケットフォーマット

### 送信フレームの基本構造
```json
{
    "request_id": "001", 
    "work_id": "llm.1001",
    "action": "taskinfo",
    "object": "None",
    "data": "None"
}
```

- request_id: コンテキストを区別するためのセッションID
- work_id: サービス呼び出し時はキーワード+ID（例：llm.xxxx）、セットアップ時はユニット名のみ
- action: 呼び出すメソッド
- object: dataで渡すパラメータの構造を設定
- data: 送信するパラメータ

[以下、各ユニット（SYS、AUDIO、KWS、ASR、LLM、TTS）の詳細な仕様と設定方法、アプリケーション例が続きます...]

# エラーコード

| コード | 説明 | メッセージ |
|--------|------|------------|
| 0 | 操作成功 | Operation Successful! |
| -1 | 通信チャネル受信状態マシンリセット警告 | reace reset |
| -2 | JSON解析エラー | JSON format error |
| -3 | sysアクションマッチエラー | action match false |
| -4 | 推論データプッシュエラー | inference data push false |
| -5 | モデルの読み込み失敗 | Model loading failed |
| -6 | ユニットが存在しない | Unit Does Not Exist |
| -7 | 不明な操作 | Unknown Operation |
| -8 | ユニットリソース割り当て失敗 | Unit Resource Allocation Failed |
| -9 | ユニット呼び出し失敗 | unit call false |
| -10 | モデル初期化失敗 | Model init failed |
| -11 | モデル実行エラー | Model run failed |
| -12 | モジュール未初期化 | Module has not been initialised |
| -13 | モジュールが既に動作中 | Module already working |
| -14 | モジュールが動作していない | Module is not working |
| -19 | ユニットリソース解放失敗 | Unit Resource Free Failed |

# アプリケーション例

## テキスト音声変換
TTSユニットを使用してテキストを音声に変換します。

## テキストアシスタント
テキストをLLMモデルに入力し、推論を処理し、音声として再生します（LLM+TTS）。

## 音声アシスタント
KWSで起動 → ASRで音声をテキストに変換 → 変換したコンテンツをLLMの入力として推論 → 最後に推論結果をTTSで音声出力します（KWS+ASR+LLM+TTS）。



# SYSユニット

SYSユニットは、モジュールの動作パラメータの設定とモジュールの動作情報の取得に使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| lsmode | 利用可能なモデルの取得 | なし | sys.lsmode |
| hwinfo | CPU負荷、メモリ負荷、チップ温度の取得 | なし | sys.hwinfo |
| reset | ユニットのリセット | なし | リセット完了JSON |
| reboot | システムの再起動 | なし | なし |
| ping | システムの応答確認 | なし | なし |

### lsmode
利用可能なモデルを取得するコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "lsmode"
}
```

応答例：
```json
{
    "created": 1692652687,
    "data": [
        {
            "capabilities": [
                "Automatic_Speech_Recognition"
            ],
            "input_type": [
                "sys.pcm"
            ],
            "model": "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23",
            "output_type": [
                "asr.utf-8"
            ],
            "type": "asr"
        },
        ... [その他のモデル情報]
    ],
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "sys.lsmode",
    "request_id": "001",
    "work_id": "sys"
}
```

### hwinfo
CPU負荷、メモリ負荷、チップ温度を取得するコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "hwinfo"
}
```

応答例（CPU負荷0%、メモリ18%、温度46°C）：
```json
{
    "created": 1692652642,
    "data": {
        "cpu_loadavg": 0,
        "mem": 18,
        "temperature": 46350
    },
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "sys.hwinfo",
    "request_id": "001",
    "work_id": "sys"
}
```

### reset
システムリセットコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "reset"
}
```

リセット開始応答：
```json
{
    "created": 1692652712,
    "error": {
        "code": 0,
        "message": "llm server restarting ..."
    },
    "request_id": "001",
    "work_id": "sys"
}
```

リセット完了応答：
```json
{
    "request_id": "0",
    "work_id": "sys",
    "created": 1692652723,
    "error": {
        "code": 0,
        "message": "reset over"
    }
}
```

### reboot
システム完全再起動コマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "reboot"
}
```

再起動コマンド応答：
```json
{
    "created": 1692652822,
    "error": {
        "code": 0,
        "message": "rebooting ..."
    },
    "request_id": "001",
    "work_id": "sys"
}
```

注意：応答メッセージの後、システムは再起動します。再起動中にV0EUEURSという文字列が送信されますが、これはシステム起動文字列であり、無視して構いません。

### ping
システムサービスの通信テスト。モジュール電源投入後の通信状態確認に有用です：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "ping"
}
```

応答例：
```json
{
    "created": 1692652310,
    "error": {
        "code": 0,
        "message": ""
    },
    "request_id": "001",
    "work_id": "sys"
}
```

# AUDIOユニット

AUDIOユニットは、システムのサウンドカードを制御し、マイク音声へのアクセスと音声再生を行います。キーワード検出（KWS）と自動音声認識（ASR）ユニットの音声入力、および音声合成（TTS）モジュールの音声出力を提供します。KWSとASRユニットを使用する前に、AUDIOユニットを初期化する必要があります。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | 音声ユニットの設定 | audio.setup | なし（成功したwork_idを含む応答を返す） |
| exit | work_idの作業終了 | なし | なし |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | audio.taskinfo |

### setup
Audioユニットを初期化し、再生音量とサウンドカードスロット番号を設定します。

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| capcard | マイクサウンドカードインデックス | デフォルトシステムサウンドカード：0 |
| capdevice | マイクデバイスインデックス | オンボードシリコンマイク：0 |
| capVolume | 入力音量 | 0.0～10.0（1以上で増幅、デフォルト0.5） |
| playcard | スピーカーサウンドカードインデックス | デフォルトシステムサウンドカード：0 |
| playdevice | スピーカーデバイスインデックス | オンボードスピーカー：1 |
| playVolume | 出力音量 | 0.0～10.0（1以上で増幅、デフォルト0.5） |

設定コマンド例：
```json
{
    "request_id": "1",
    "work_id": "audio",
    "action": "setup",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.5
    }
}
```

初期化応答：
```json
{
    "created": 1692659008,
    "error": {
        "code": 0,
        "message": "audio setup successful"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### pause
Audioユニット一時停止コマンド：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692659049,
    "error": {
        "code": 0,
        "message": "audio pause"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### work
Audioユニット開始コマンド：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "work",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.25
    }
}
```

開始応答：
```json
{
    "created": 1692659297,
    "error": {
        "code": 0,
        "message": "audio work start"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### exit
Audioユニットの終了と解放：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692659370,
    "error": {
        "code": 0,
        "message": "audio exit"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### taskinfo
Audioユニットの状態照会：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692659454,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

停止中の応答：
```json
{
    "created": 1692659499,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

解放済みの応答：
```json
{
    "created": 1692659403,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```


# TTSユニット

TTSユニットはテキストを音声に変換するために使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | TTSユニットの設定 | tts.setup | なし（成功したwork_idを含む応答を返す） |
| inference | 推論の実行 | 通常: tts.utf-8（モデルの違いはsys.lsmodeで確認可能） | なし（データ送信結果のみを返す。最終的な推論結果は設定に依存） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | tts.taskinfo |

### setup
TTSユニットを初期化し、中国語/英語モデルを設定します。

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | 英語モデル: "single_speaker_english_fast"<br>中国語モデル: "single_speaker_fast" |
| input | 入力 | LLM入力: "llm.xxx"（LLMユニットのwork_id）<br>UART入力: "tts.utf-8"<br>UARTストリーミング入力: "tts.utf-8.stream" |
| enkws | プロセスのKWSによる中断 | KWSで中断: true<br>KWSで中断しない: false |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

#### LLMからの入力設定
英語テキスト音声変換モデルでTTSユニットを初期化し、LLM推論結果を入力として設定：
```json
{
    "request_id": "5",
    "work_id": "tts",
    "action": "setup",
    "object": "tts.setup",
    "data": {
        "model": "single_speaker_english_fast", 
        "response_format": "tts.base64.wav",
        "input": "llm.1004",
        "enoutput": true,
        "enkws": true
    }
}
```

#### UARTからの入力設定
英語テキスト音声変換モデルでTTSユニットを初期化し、UARTコマンドストリーミング入力を設定：
```json
{
    "request_id": "5",
    "work_id": "tts",
    "action": "setup",
    "object": "tts.setup",
    "data": {
        "model": "single_speaker_english_fast", 
        "response_format": "tts.base64.wav",
        "input": "tts.utf-8.stream",
        "enoutput": true,
        "enkws": true
    }
}
```

TTSユニット初期化応答：
```json
{
    "created": 1692668824,
    "error": {
        "code": 0,
        "message": "tts setup successful"
    },
    "request_id": "5",
    "work_id": "tts.1004"
}
```

### inference
UART経由でTTS変換データ内容を送信します。各モデルは一度に1つの言語のみをサポートします。異なる言語を変換する場合は、exitでTTSユニットを解放し、setupで再初期化してください。

注意：変換するテキストは必ずピリオドで終わる必要があります：
- 英語テキストの場合は英語のピリオド . （半角記号）を使用
- 中国語テキストの場合は中国語のピリオド 。（全角記号）を使用
- 文の区切りには , （半角記号）を使用

ストリーミング入力の例：
```json
{
    "request_id": "4", 
    "work_id": "tts.1004",
    "action": "inference",
    "object": "tts.utf-8.stream",
    "data": {
        "delta": "I don't know what your name.",
        "index": 0,
        "finish": true
    }
}
```

非ストリーミング入力の例：
```json
{
    "request_id": "4", 
    "work_id": "tts.1004",
    "action": "inference",
    "object": "tts.utf-8",
    "data": "I don't know what your name."
}
```

### pause
TTSユニット一時停止コマンド：
```json
{
    "request_id": "5",
    "work_id": "tts.1004",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692668916,
    "error": {
        "code": 0,
        "message": "tts pause"
    },
    "request_id": "5",
    "work_id": "tts.1004"
}
```

### work
TTSユニット開始コマンド：
```json
{
    "request_id": "5",
    "work_id": "tts.1004",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692668944,
    "error": {
        "code": 0,
        "message": "tts work"
    },
    "request_id": "5",
    "work_id": "tts.1004"
}
```

### exit
TTSユニットの終了と解放：
```json
{
    "request_id": "5",
    "work_id": "tts.1004",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692669052,
    "error": {
        "code": 0,
        "message": "tts exit"
    },
    "request_id": "5",
    "work_id": "tts.1004"
}
```

### taskinfo
TTSユニットの状態照会：
```json
{
    "request_id": "5",
    "work_id": "tts.1004",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692668878,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "tts.state",
    "request_id": "5",
    "work_id": "tts.1004"
}
```

停止中の応答：
```json
{
    "created": 1692668968,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "tts.state",
    "request_id": "5",
    "work_id": "tts.1004"
}
```

解放済みの応答：
```json
{
    "created": 1692669081,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "tts.state",
    "request_id": "5",
    "work_id": "tts.1004"
}
```

# アプリケーション例

## テキスト音声変換
TTSユニットを使用してテキストを音声に変換します。

1. Audioユニットの初期化：
```json
{
    "request_id": "1",
    "work_id": "audio",
    "action": "setup",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.5
    }
}
```

Audioユニット初期化応答：
```json
{
    "created": 1692652475,
    "error": {
        "code": 0,
        "message": "audio setup successful"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

2. TTSユニットを初期化し、英語テキスト音声変換モデルを設定し、UARTコマンド入力を設定：
```json
{
    "request_id": "5",
    "work_id": "tts",
    "action": "setup",
    "object": "tts.setup",
    "data": {
        "model": "single_speaker_english_fast", 
        "response_format": "tts.base64.wav",
        "input": "tts.utf-8",
        "enoutput": true,
        "enkws": true
    }
}
```

TTSユニット初期化応答：
```json
{
    "created": 1692652569,
    "error": {
        "code": 0,
        "message": "tts setup successful"
    },
    "request_id": "5",
    "work_id": "tts.1001"
}
```

3. テキストを入力してTTS変換を開始：
```json
{
    "request_id": "4", 
    "work_id": "tts.1001",
    "action": "inference",
    "object": "tts.utf-8",
    "data": "Hello My Friend."
}
```

## テキストアシスタント
テキストをLLMモデルに入力し、推論を処理し、音声として再生します（LLM+TTS）。

1. Audioユニットの初期化：
```json
{
    "request_id": "1",
    "work_id": "audio",
    "action": "setup",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.5
    }
}
```

Audioユニット初期化応答：
```json
{
    "created": 1692652330,
    "error": {
        "code": 0,
        "message": "audio setup successful"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

2. LLMユニットを初期化し、UARTインターフェースを入力データとして設定：
```json
{
    "request_id": "4",
    "work_id": "llm",
    "action": "setup",
    "object": "llm.setup",
    "data": {
        "model": "qwen2.5-0.5b",
        "response_format": "llm.utf-8",
        "input": "llm.utf-8",
        "enoutput": true,
        "enkws": true,
        "max_token_len": 127,
        "prompt": "You are a knowledgeable assistant capable of answering various questions and providing information."
    }
}
```

LLMユニット初期化応答：
```json
{
    "created": 1692652323,
    "error": {
        "code": 0,
        "message": "llm setup successful"
    },
    "request_id": "4",
    "work_id": "llm.1001"
}
```

3. TTSユニットを初期化し、英語テキスト音声変換モデルを設定し、LLM推論結果を入力として設定：
```json
{
    "request_id": "5",
    "work_id": "tts",
    "action": "setup",
    "object": "tts.setup",
    "data": {
        "model": "single_speaker_english_fast", 
        "response_format": "tts.base64.wav",
        "input": "llm.1001",
        "enoutput": true,
        "enkws": true
    }
}
```

TTSユニット初期化応答：
```json
{
    "created": 1692652354,
    "error": {
        "code": 0,
        "message": "tts setup successful"
    },
    "request_id": "5",
    "work_id": "tts.1002"
}
```

4. UART経由で推論データを送信：
```json
{
    "request_id": "4",
    "work_id": "llm.1001",
    "action": "inference",
    "object": "llm.utf-8",
    "data": "What's ur name?"
}
```

5. 音声出力を伴う推論応答データ：
```json
{
    "created": 1692652407,
    "data": "I'm not a person, but I'm here to help with any questions you may have. How can I assist you today?\n",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.utf-8",
    "request_id": "4",
    "work_id": "llm.1001"
}
```

## 音声アシスタント
KWSで起動 → ASRで音声をテキストに変換 → 変換したコンテンツをLLMの入力として推論 → 最後に推論結果をTTSで音声出力します（KWS+ASR+LLM+TTS）。

1. Audioユニットの初期化：
```json
{
    "request_id": "1",
    "work_id": "audio",
    "action": "setup",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.5
    }
}
```

Audioユニット初期化応答：
```json
{
    "created": 1692652330,
    "error": {
        "code": 0,
        "message": "audio setup successful"
    },
    "request_id": "1",
    

# LLMユニット

LLM（大規模言語モデル）ユニットは、入力テキストに基づいて応答を生成することができます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | LLMユニットの設定 | llm.setup | なし（成功したwork_idを含む応答を返す） |
| inference | 推論の実行 | 通常: llm.utf-8（モデルの違いはsys.lsmodeで確認可能） | なし（データ送信結果のみを返す。最終的な推論結果は設定に依存） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | llm.taskinfo |

### setup
LLMユニットを初期化し、指定したモデルを設定します。現在プリインストールされているモデル：
- qwen2.5-0.5b

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | プリインストールモデル "qwen2.5-0.5b" |
| response_format | 出力フォーマット | 標準出力: "llm.utf-8"<br>ストリーミング出力: "llm.utf-8.stream" |
| input | 入力 | ASR入力: "asr.xxx"（ASRユニットのwork_id）<br>UART入力: "llm.utf-8"<br>UARTストリーミング入力: "llm.utf-8.stream" |
| enkws | 進行中のプロセスのKWSによる中断 | KWSで中断: true<br>KWSで中断しない: false |
| max_length | 最大出力トークン長の設定 | 最大: 1024, 推奨: 127 |
| prompt | モデル初期化プロンプト | - |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

#### ASRからの入力設定
ASR（音声認識）を入力データとして設定するLLMユニットの初期化：
```json
{
    "request_id": "4",
    "work_id": "llm",
    "action": "setup",
    "object": "llm.setup",
    "data": {
        "model": "qwen2.5-0.5b",
        "response_format": "llm.utf-8.stream",
        "input": "asr.1001",
        "enoutput": true,
        "enkws": true,
        "max_token_len": 127,
        "prompt": "You are a knowledgeable assistant capable of answering various questions and providing information."       
    }
}
```

#### UARTからの入力設定
UARTインターフェースを入力データとして設定するLLMユニットの初期化：
```json
{
    "request_id": "4",
    "work_id": "llm",
    "action": "setup",
    "object": "llm.setup",
    "data": {
        "model": "qwen2.5-0.5b",
        "response_format": "llm.utf-8",
        "input": "llm.utf-8.stream",
        "enoutput": true,
        "enkws": true,
        "max_token_len": 127,
        "prompt": "You are a knowledgeable assistant capable of answering various questions and providing information."
    }
}
```

LLMユニット初期化応答：
```json
{
    "created": 1692664107,
    "data": "None",
    "error": {
        "code": 0,
        "message": "llm setup successful"
    },
    "object": "None",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### inference
UART経由で推論データを送信：

ストリーミング入力の例：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "inference",
    "object": "llm.utf-8.stream",
    "data": {
        "delta": "What's ur name?",
        "index": 0,
        "finish": true
    }
}
```

非ストリーミング入力の例：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "inference",
    "object": "llm.utf-8",
    "data": "What's ur name?"
}
```

推論応答データ：
```json
{
    "created": 1692664605,
    "data": {
        "delta": "I'm not a person, but I'm here to help with any questions you may have. How can I assist you today?\n",
        "finish": true,
        "index": 0
    },
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.utf-8.stream",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### pause
LLMユニット一時停止コマンド：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692664941,
    "error": {
        "code": 0,
        "message": "llm pause"
    },
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### work
LLMユニット開始コマンド：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692664972,
    "error": {
        "code": 0,
        "message": "llm work"
    },
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### exit
LLMユニットの終了と解放：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692664858,
    "data": "None",
    "error": {
        "code": 0,
        "message": "llm exit"
    },
    "object": "None",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

### taskinfo
LLMユニットの状態照会：
```json
{
    "request_id": "4",
    "work_id": "llm.1003",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692664730,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.state",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

停止中の応答：
```json
{
    "created": 1692664823,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.state",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

解放済みの応答：
```json
{
    "created": 1692664881,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "llm.state",
    "request_id": "4",
    "work_id": "llm.1003"
}
```

# KWSユニット

KWSユニットはキーワード検出に使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | KWSユニットの設定 | kws.setup | なし（成功したwork_idを含む応答を返す） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | kws.taskinfo |

### setup
KWSユニットを初期化し、中国語/英語認識モデルを設定します。
（注意：KWSキーワードフィールドでは中国語/英語の混在は許可されません）

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | 英語モデル: "sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01"<br>中国語モデル: "sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01" |
| kws | KWSキーワードテキスト | 中国語/英語の混在不可、英語は大文字のみ |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

英語認識モデルでのKWS設定例：
```json
{
    "request_id": "2",
    "work_id": "kws",
    "action": "setup",
    "object": "kws.setup",
    "data": {
        "model": "sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01",
        "response_format": "kws.bool",
        "input": "sys.pcm",
        "enoutput": true,
        "kws": "HELLO"
    }
}
```

初期化応答（注：セットアップ処理には約9秒かかります）：
```json
{
    "created": 1692660576,
    "error": {
        "code": 0,
        "message": "kws setup successful"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

キーワード検出時の応答：
```json
{
    "created": 1692660576,
    "error": {
        "code": 0,
        "message": "kws setup successful"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### pause
KWSユニット一時停止コマンド：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692660626,
    "error": {
        "code": 0,
        "message": "kws pause"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### work
KWSユニット開始コマンド：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692660651,
    "error": {
        "code": 0,
        "message": "kws work"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### exit
KWSユニットの終了と解放：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692654383,
    "error": {
        "code": 0,
        "message": "kws exit"
    },
    "request_id": "2",
    "work_id": "kws.1001"
}
```

### taskinfo
KWSユニットの状態照会：
```json
{
    "request_id": "2",
    "work_id": "kws.1001",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692654305,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.1001"
}
```

停止中の応答：
```json
{
    "created": 1692654535,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.1001"
}
```

解放済みの応答：
```json
{
    "created": 1692654452,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "kws.state",
    "request_id": "2",
    "work_id": "kws.0"
}
```

# ASRユニット

ASRユニットは音声をテキストに変換するために使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | ASRユニットの設定 | asr.setup | なし（成功したwork_idを含む応答を返す） |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| exit | work_idの作業終了 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | asr.taskinfo |

### setup

ASRユニットを初期化し、中国語/英語モデルを設定します。

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| model | 変換モデル | 英語モデル: "sherpa-ncnn-streaming-zipformer-20M-2023-02-17"<br>中国語モデル: "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23" |
| response_format | 出力フォーマット | 標準出力: "asr.utf-8"<br>ストリーミング出力: "asr.utf-8.stream" |
| input | 入力 | LLM入力: "llm.xxx"（llmユニットのwork_id）<br>UART入力: "tts.utf-8"<br>UARTストリーミング入力: "tts.utf-8.stream" |
| enkws | KWSによる起動の有効化 | KWSで起動後ASR実行: true<br>KWS起動なし、ASRは継続的に動作: false |
| rule1 | 起動から未認識コンテンツまでのタイムアウト | 単位：秒 |
| rule2 | 認識の最大間隔時間 | 単位：秒 |
| rule3 | 認識の最大タイムアウト | 単位：秒 |
| enoutput | UART出力の有効化 | 有効: true<br>無効: false |

英語モデルでのASR設定例：
```json
{
    "request_id": "3",
    "work_id": "asr",
    "action": "setup",
    "object": "asr.setup",
    "data": {
        "model": "sherpa-ncnn-streaming-zipformer-20M-2023-02-17",
        "response_format": "asr.utf-8",
        "input": "sys.pcm",
        "enoutput": true,
        "enkws": true,
        "rule1": 2.4,
        "rule2": 1.2,
        "rule3": 30
    }
}
```

ASRユニット初期化応答：
```json
{
    "created": 1692667736,
    "error": {
        "code": 0,
        "message": "asr setup successful"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

ASR認識応答：
```json
{
    "created": 1692655176,
    "data": {
        "delta": " hello",
        "index": "0"
    },
    "object": "asr.stream",
    "request_id": "004",
    "work_id": "asr.1003"
}
```

### pause
ASRユニット一時停止コマンド：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692670174,
    "error": {
        "code": 0,
        "message": "asr pause"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### work
ASRユニット開始コマンド：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "work"
}
```

開始応答：
```json
{
    "created": 1692670213,
    "error": {
        "code": 0,
        "message": "asr work"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### exit
ASRユニットの終了と解放：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692670254,
    "error": {
        "code": 0,
        "message": "asr exit"
    },
    "request_id": "3",
    "work_id": "asr.1002"
}
```

### taskinfo
ASRユニットの状態照会：
```json
{
    "request_id": "3",
    "work_id": "asr.1002",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692669923,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.1002"
}
```

停止中の応答：
```json
{
    "created": 1692653792,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.1002"
}
```

解放済みの応答：
```json
{
    "created": 1692669874,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "asr.state",
    "request_id": "3",
    "work_id": "asr.0"
}
```# 概要

LLMモジュールは、KWS（キーワード検出）、ASR（音声認識）、LLM（大規模言語モデル）、TTS（音声合成）などの機能ユニットを統合しています。各ユニットは独立したモジュールとして動作することも、データワークフローの統合のための設定をサポートすることもでき、よりインテリジェントなインタラクティブアプリケーションを実現できます。このモジュールはUART通信を介してホストデバイスと対話し、JSONフォーマットのデータパケットを使用するため、非常に使いやすい設計となっています。

## 内蔵機能ユニット

| ユニット | ユニット名 | 機能 |
|----------|------------|------|
| sys | システム | モジュールパラメータの設定、モジュールステータスの取得 |
| kws | キーワード検出 | 音声内のキーワードの検出 |
| asr | 音声認識 | 音声をテキストに変換 |
| llm | 生成モデル | 入力テキストに基づいて新しいテキストを生成 |
| tts | 音声合成 | テキストを音声に変換 |
| audio | システム音声インターフェース | マイク音声へのアクセスと音声再生 |

## 使用手順

1. モジュールをM5Stackメインコントローラ（Basic/M5Core2/M5Core3など）とスタックするか、USB-TTLコンバータを使用してTX/RXと電源に直接接続します。正常に起動すると、モジュールは緑色に点灯します。

2. プログラムでUARTインターフェースを初期化します（ピン設定は実際に接続されているデバイスに基づき、インターフェース設定は115200bps 8N1）。

3. 以下の使用例を参照し、初期化フレームを送信して目的のユニットサービスを有効化します。

## 通信インターフェース

LLMモジュールのUARTインターフェースは、デフォルトで115200bps 8N1に設定されています。

## データパケットフォーマット

### 送信フレームの基本構造
```json
{
    "request_id": "001", 
    "work_id": "llm.1001",
    "action": "taskinfo",
    "object": "None",
    "data": "None"
}
```

- request_id: コンテキストを区別するためのセッションID
- work_id: サービス呼び出し時はキーワード+ID（例：llm.xxxx）、セットアップ時はユニット名のみ
- action: 呼び出すメソッド
- object: dataで渡すパラメータの構造を設定
- data: 送信するパラメータ

[以下、各ユニット（SYS、AUDIO、KWS、ASR、LLM、TTS）の詳細な仕様と設定方法、アプリケーション例が続きます...]

# エラーコード

| コード | 説明 | メッセージ |
|--------|------|------------|
| 0 | 操作成功 | Operation Successful! |
| -1 | 通信チャネル受信状態マシンリセット警告 | reace reset |
| -2 | JSON解析エラー | JSON format error |
| -3 | sysアクションマッチエラー | action match false |
| -4 | 推論データプッシュエラー | inference data push false |
| -5 | モデルの読み込み失敗 | Model loading failed |
| -6 | ユニットが存在しない | Unit Does Not Exist |
| -7 | 不明な操作 | Unknown Operation |
| -8 | ユニットリソース割り当て失敗 | Unit Resource Allocation Failed |
| -9 | ユニット呼び出し失敗 | unit call false |
| -10 | モデル初期化失敗 | Model init failed |
| -11 | モデル実行エラー | Model run failed |
| -12 | モジュール未初期化 | Module has not been initialised |
| -13 | モジュールが既に動作中 | Module already working |
| -14 | モジュールが動作していない | Module is not working |
| -19 | ユニットリソース解放失敗 | Unit Resource Free Failed |

# アプリケーション例

## テキスト音声変換
TTSユニットを使用してテキストを音声に変換します。

## テキストアシスタント
テキストをLLMモデルに入力し、推論を処理し、音声として再生します（LLM+TTS）。

## 音声アシスタント
KWSで起動 → ASRで音声をテキストに変換 → 変換したコンテンツをLLMの入力として推論 → 最後に推論結果をTTSで音声出力します（KWS+ASR+LLM+TTS）。



# SYSユニット

SYSユニットは、モジュールの動作パラメータの設定とモジュールの動作情報の取得に使用されます。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| lsmode | 利用可能なモデルの取得 | なし | sys.lsmode |
| hwinfo | CPU負荷、メモリ負荷、チップ温度の取得 | なし | sys.hwinfo |
| reset | ユニットのリセット | なし | リセット完了JSON |
| reboot | システムの再起動 | なし | なし |
| ping | システムの応答確認 | なし | なし |

### lsmode
利用可能なモデルを取得するコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "lsmode"
}
```

応答例：
```json
{
    "created": 1692652687,
    "data": [
        {
            "capabilities": [
                "Automatic_Speech_Recognition"
            ],
            "input_type": [
                "sys.pcm"
            ],
            "model": "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23",
            "output_type": [
                "asr.utf-8"
            ],
            "type": "asr"
        },
        ... [その他のモデル情報]
    ],
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "sys.lsmode",
    "request_id": "001",
    "work_id": "sys"
}
```

### hwinfo
CPU負荷、メモリ負荷、チップ温度を取得するコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "hwinfo"
}
```

応答例（CPU負荷0%、メモリ18%、温度46°C）：
```json
{
    "created": 1692652642,
    "data": {
        "cpu_loadavg": 0,
        "mem": 18,
        "temperature": 46350
    },
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "sys.hwinfo",
    "request_id": "001",
    "work_id": "sys"
}
```

### reset
システムリセットコマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "reset"
}
```

リセット開始応答：
```json
{
    "created": 1692652712,
    "error": {
        "code": 0,
        "message": "llm server restarting ..."
    },
    "request_id": "001",
    "work_id": "sys"
}
```

リセット完了応答：
```json
{
    "request_id": "0",
    "work_id": "sys",
    "created": 1692652723,
    "error": {
        "code": 0,
        "message": "reset over"
    }
}
```

### reboot
システム完全再起動コマンド：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "reboot"
}
```

再起動コマンド応答：
```json
{
    "created": 1692652822,
    "error": {
        "code": 0,
        "message": "rebooting ..."
    },
    "request_id": "001",
    "work_id": "sys"
}
```

注意：応答メッセージの後、システムは再起動します。再起動中にV0EUEURSという文字列が送信されますが、これはシステム起動文字列であり、無視して構いません。

### ping
システムサービスの通信テスト。モジュール電源投入後の通信状態確認に有用です：
```json
{
    "request_id": "001", 
    "work_id": "sys",
    "action": "ping"
}
```

応答例：
```json
{
    "created": 1692652310,
    "error": {
        "code": 0,
        "message": ""
    },
    "request_id": "001",
    "work_id": "sys"
}
```

# AUDIOユニット

AUDIOユニットは、システムのサウンドカードを制御し、マイク音声へのアクセスと音声再生を行います。キーワード検出（KWS）と自動音声認識（ASR）ユニットの音声入力、および音声合成（TTS）モジュールの音声出力を提供します。KWSとASRユニットを使用する前に、AUDIOユニットを初期化する必要があります。

## メソッド一覧

| メソッド | 機能 | 入力タイプ | 出力タイプ |
|----------|------|------------|------------|
| setup | 音声ユニットの設定 | audio.setup | なし（成功したwork_idを含む応答を返す） |
| exit | work_idの作業終了 | なし | なし |
| pause | タスク操作の一時停止 | なし | なし |
| work | タスク操作の再開 | なし | なし |
| taskinfo | すべてのタスクインスタンス情報の取得 | なし | audio.taskinfo |

### setup
Audioユニットを初期化し、再生音量とサウンドカードスロット番号を設定します。

#### パラメータ説明

| パラメータ | 説明 | 入力値 |
|------------|------|---------|
| capcard | マイクサウンドカードインデックス | デフォルトシステムサウンドカード：0 |
| capdevice | マイクデバイスインデックス | オンボードシリコンマイク：0 |
| capVolume | 入力音量 | 0.0～10.0（1以上で増幅、デフォルト0.5） |
| playcard | スピーカーサウンドカードインデックス | デフォルトシステムサウンドカード：0 |
| playdevice | スピーカーデバイスインデックス | オンボードスピーカー：1 |
| playVolume | 出力音量 | 0.0～10.0（1以上で増幅、デフォルト0.5） |

設定コマンド例：
```json
{
    "request_id": "1",
    "work_id": "audio",
    "action": "setup",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.5
    }
}
```

初期化応答：
```json
{
    "created": 1692659008,
    "error": {
        "code": 0,
        "message": "audio setup successful"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### pause
Audioユニット一時停止コマンド：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "pause"
}
```

一時停止応答：
```json
{
    "created": 1692659049,
    "error": {
        "code": 0,
        "message": "audio pause"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### work
Audioユニット開始コマンド：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "work",
    "object": "audio.setup",
    "data": {
        "capcard": 0,
        "capdevice": 0,
        "capVolume": 0.5,
        "playcard": 0,
        "playdevice": 1,
        "playVolume": 0.25
    }
}
```

開始応答：
```json
{
    "created": 1692659297,
    "error": {
        "code": 0,
        "message": "audio work start"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### exit
Audioユニットの終了と解放：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "exit"
}
```

終了応答：
```json
{
    "created": 1692659370,
    "error": {
        "code": 0,
        "message": "audio exit"
    },
    "request_id": "1",
    "work_id": "audio.1000"
}
```

### taskinfo
Audioユニットの状態照会：
```json
{
    "request_id": "1",
    "work_id": "audio.1000",
    "action": "taskinfo"
}
```

実行中の応答：
```json
{
    "created": 1692659454,
    "data": "running",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

停止中の応答：
```json
{
    "created": 1692659499,
    "data": "stopped",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```

解放済みの応答：
```json
{
    "created": 1692659403,
    "data": "deinit",
    "error": {
        "code": 0,
        "message": ""
    },
    "object": "audio.state",
    "request_id": "1",
    "work_id": "audio.1000"
}
```
