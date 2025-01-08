##　Version情報

![image](https://github.com/user-attachments/assets/1a01561d-8c25-4aac-95dd-811c61eb8dfe)

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



