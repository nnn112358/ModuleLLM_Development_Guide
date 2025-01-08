## Version情報
LLM Module Firmware Upgrade https://docs.m5stack.com/en/guide/llm/llm/image
からdebをダウンロードしてインストールする。

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
## Depth anything 
 llm-depth-anything_1.3-m5stack1_arm64.debをインストール後、/opt/m5stack/data/depth_anything/ディレクトリに、
depth_anything.axmodel、mode_depth_anything.jsonを配置したところ、動くことを確認しました。

```
root@m5stack-LLM:# tree /opt/m5stack/data/depth_anything/
/opt/m5stack/data/depth_anything/
 depth_anything.axmodel
 mode_depth_anything.json
````

 mode_depth_anything.json:https://github.com/m5stack/StackFlow/blob/dev/projects/llm_framework/main_depth_anything/mode_depth_anything.json

```
openbuddy-llama3.2-1B
total size=3145728KB(3072MB),used=1300104KB(1269MB + 648KB),remain=1845624KB(1802MB + 376KB),partition_number=1,block_number=388

llm-llama3.2-1B
total size=3145728KB(3072MB),used=1300068KB(1269MB + 612KB),remain=1845660KB(1802MB + 412KB),partition_number=1,block_number=388

llm-qwen2.5-1.5B
total size=3145728KB(3072MB),used=1641200KB(1602MB + 752KB),remain=1504528KB(1469MB + 272KB),partition_number=1,block_number=664

llm-qwen2.5-0.5B
total size=3145728KB(3072MB),used=537356KB(524MB + 780KB),remain=2608372KB(2547MB + 244KB),partition_number=1,block_number=572
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



