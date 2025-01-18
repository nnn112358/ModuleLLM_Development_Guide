#!/usr/bin/env python3
import socket
import json
import time
import subprocess
import os
from pathlib import Path
import argparse

def get_wifi_ip():
    """Wi-Fi IPアドレスをサブプロセスを使用して取得"""
    try:
        cmd = "ip -4 addr show | grep -E 'inet .*(eth0|wlan0)' | awk '{print $2}' | cut -d/ -f1"
        result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        return result if result else None
    except subprocess.CalledProcessError:
        return None

def send_json_request(sock, request_data):
    """JSONリクエストをサーバーに送信"""
    try:
        json_string = json.dumps(request_data)
        sock.sendall(json_string.encode('utf-8'))
        print(f'送信したリクエスト: {json_string}')
        time.sleep(1)
    except Exception as e:
        print(f'リクエスト送信エラー: {e}')

def receive_response(sock):
    """サーバーからのレスポンスを受信して処理"""
    try:
        data = sock.recv(4096)
        if data:
            response = data.decode('utf-8')
            print(f'受信したレスポンス: {response}')
            return json.loads(response)
    except Exception as e:
        print(f'レスポンス受信エラー: {e}')
    return None

def main(host, port):
    os.chdir(Path(__file__).parent)
    
    wifi_ip = get_wifi_ip()
    if not wifi_ip:
        print("Wi-Fi IPアドレスが見つかりません")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f'サーバー {host}:{port} に接続しました')

        # オーディオセットアップ
        audio_setup = {
            "request_id": "audio_setup",
            "work_id": "audio",
            "action": "setup",
            "object": "audio.setup",
            "data": {
                "capcard": 0,
                "capdevice": 0,
                "capVolume": 0.5,
                "playcard": 0,
                "playdevice": 1,
                "playVolume": 0.15
            }
        }
        send_json_request(client_socket, audio_setup)
        receive_response(client_socket)

        # TTSセットアップ
        tts_setup = {
            "request_id": "melotts_setup",
            "work_id": "melotts",
            "action": "setup",
            "object": "melotts.setup",
            "data": {
                "model": "melotts_zh-cn",
                "response_format": "sys.pcm",
                "input": ["tts.utf-8.stream"],  # 配列に修正
                "enoutput": False,
                "enaudio": True
            }
        }
        send_json_request(client_socket, tts_setup)
        receive_response(client_socket)

        # TTS推論
        inference_request = {
            "request_id": "tts_inference",
            "work_id": "melotts.1001",  # work_idを修正
            "action": "inference",
            "object":  "tts.utf-8.stream",
            "data": {
                "delta": "Hello I am Stack chan.",
                "index": 0,
                "finish": True
            }
        }
        send_json_request(client_socket, inference_request)
        receive_response(client_socket)
        
        time.sleep(5)
        
        # リセット
        reset_request = {
            "request_id": "4",
            "work_id": "sys",
            "action": "reset"
        }
        send_json_request(client_socket, reset_request)
        receive_response(client_socket)

    except Exception as e:
        print(f'エラー: {e}')
    finally:
        client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Client to send JSON data.')
    #parser.add_argument('--host', type=str, default='localhost', help='Server hostname (default: localhost)')
    parser.add_argument('--host', type=str, default='m5stack-LLM.local', help='Server hostname (default: m5stack-LLM.local)')
    parser.add_argument('--port', type=int, default=10001, help='Server port (default: 10001)')

    args = parser.parse_args()
    main(args.host, args.port)