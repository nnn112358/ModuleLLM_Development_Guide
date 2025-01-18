## overview
Module-LLMのStackFlowのAPIへ、PCのPythonからアクセスするサンプル。<br>

Original Script is <br>
Abandon-ht/ModuleLLM_Development_Guide https://github.com/Abandon-ht/ModuleLLM_Development_Guide  <br>
https://docs.m5stack.com/en/guide/llm/llm630_compute_kit/stackflow<br>

## How to 

Module-LLMと同じネットワークに接続して、Pythonスクリプトを実行します。<br>
また、Module-LLMから、Pythonスクリプトを実行することも可能です。<br>
--hostの後にModule-LLMのIPアドレスを指定します。<br>
--hostの後に指定がない場合は、Module-LLMはDNSでm5stack-LLM.localのホスト名が割り振られますので、m5stack-LLM.localにアクセスするようにしています。<br>
Pythonスクリプトの中の promptで、返信するキャラクターが変わるので、好きに書き換えてみましょう。<br>
promptに日本語を入れると日本語でLLMが回答してくれます。英語を入れると英語になります。<br>

```
$ python llm-qwen2.5-0.5B.py --host m5stack-LLM.local(or 192.168.1.10)
Setup LLM...
Setup LLM finished.
Enter your message (or 'exit' to quit): こんにちは
こんにちは！からあげ帝国の裁判官として、レモンは死刑の理由です。しかし、あなたが質問に答えるべきは、あな たがどのような状況に遭遇したかです。具体的な質問があれば、より具体的な回答を提供いただけますか？

Enter your message (or 'exit' to quit):
```



## Version情報
LLM Module Firmware Upgrade https://docs.m5stack.com/en/guide/llm/llm/image
からdebをダウンロードしてインストールする。
インストールしてある,LLMのサービスは以下で確認します。
```
root@m5stack-LLM:~# dpkg -l | grep llm
ii  lib-llm                                                   1.4                                     arm64        llm-module
ii  llm-asr                                                   1.3                                     arm64        llm-module
ii  llm-audio                                                 1.3                                     arm64        llm-module
ii  llm-audio-en-us                                           0.2                                     arm64        llm-module
ii  llm-audio-zh-cn                                           0.2                                     arm64        llm-module
ii  llm-camera                                                1.3                                     arm64        llm-module
ii  llm-depth-anything                                        1.3                                     arm64        llm-module
ii  llm-kws                                                   1.3                                     arm64        llm-module
ii  llm-llama3.2-1b-prefill-ax630c                            0.2                                     arm64        llm-module
ii  llm-llm                                                   1.4                                     arm64        llm-module
ii  llm-melotts                                               1.3                                     arm64        llm-module
ii  llm-melotts-zh-cn                                         0.2                                     arm64        llm-module
ii  llm-openbuddy-llama3.2-1b-ax630c                          0.2                                     arm64        llm-module
ii  llm-qwen2.5-0.5b-prefill-20e                              0.2                                     arm64        llm-module
ii  llm-qwen2.5-1.5b-ax630c                                   0.3                                     arm64        llm-module
ii  llm-qwen2.5-coder-0.5b-ax630c                             0.2                                     arm64        llm-module
ii  llm-sherpa-ncnn-streaming-zipformer-20m-2023-02-17        0.2                                     arm64        llm-module
ii  llm-sherpa-ncnn-streaming-zipformer-zh-14m-2023-02-23     0.2                                     arm64        llm-module
ii  llm-sherpa-onnx-kws-zipformer-gigaspeech-3.3m-2024-01-01  0.3                                     arm64        llm-module
ii  llm-sherpa-onnx-kws-zipformer-wenetspeech-3.3m-2024-01-01 0.3                                     arm64        llm-module
ii  llm-single-speaker-english-fast                           0.2                                     arm64        llm-module
ii  llm-single-speaker-fast                                   0.2                                     arm64        llm-module
ii  llm-skel                                                  1.3                                     arm64        llm-module
ii  llm-sys                                                   1.3                                     arm64        llm-module
ii  llm-tts                                                   1.3                                     arm64        llm-module
ii  llm-vlm                                                   1.4                                     arm64        llm-module
ii  llm-yolo                                                  1.4                                     arm64        llm-module
ii  llm-yolo11n                                               0.2                                     arm64        llm-module
ii  llm-yolo11n-hand-pose                                     0.3                                     arm64        llm-module
ii  llm-yolo11n-pose                                          0.3                                     arm64        llm-module
ii  llm-yolo11n-seg                                           0.2                                     arm64        llm-module
```

===

## Refer
m5stack/StackFlow https://github.com/m5stack/StackFlow  
m5stack/M5Module-LLM https://github.com/m5stack/M5Module-LLM  
projects_llm_framework_doc https://github.com/m5stack/StackFlow/tree/main/doc/projects_llm_framework_doc  
LLMモジュールJSON APIドキュメント https://github.com/m5stack/StackFlow/tree/main/doc  
LLM_Module_API_v1.0.0_CN.pdf https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/protocol/M140/LLM_Module_API_v1.0.0_CN.pdf  
LLM Module Firmware Upgrade https://docs.m5stack.com/en/guide/llm/llm/image  
M5stack LLM Module買う-4  https://kinneko.fanbox.cc/posts/9088305  
IPアドレスを喋る@washishi https://x.com/washishi/status/1866229894763708587  
Abandon-ht/ModuleLLM_Development_Guide https://github.com/Abandon-ht/ModuleLLM_Development_Guide  



