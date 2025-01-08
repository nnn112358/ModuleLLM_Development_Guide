#!/usr/bin/env python3
import socket
import json
import time
import subprocess
import os
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'tts_script_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

def send_json_request(sock, request_data):
    try:
        json_string = json.dumps(request_data)
        sock.sendall(json_string.encode('utf-8'))
        logger.info(f'送信したリクエスト: {json_string}')
        time.sleep(1)
    except Exception as e:
        logger.error(f'リクエスト送信エラー: {e}')

def receive_response(sock):
    try:
        data = sock.recv(4096)
        if data:
            response = data.decode('utf-8')
            logger.info(f'受信したレスポンス: {response}')
            return json.loads(response)
    except Exception as e:
        logger.error(f'レスポンス受信エラー: {e}')
    return None

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_address = ('192.168.20.8', 10001)
        client_socket.connect(server_address)
        logger.info(f'サーバー {server_address[0]}:{server_address[1]} に接続しました')

        # オーディオセットアップ
        logger.info("オーディオセットアップを開始")
        audio_setup = {
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
        send_json_request(client_socket, audio_setup)
        receive_response(client_socket)

        # MeloTTSセットアップ
        logger.info("MeloTTSセットアップを開始")
        tts_setup = {
            "request_id": "2",
            "work_id": "melotts",
            "action": "setup",
            "object": "melotts.setup",
            "data": {
                "model": "melotts_zh-cn",
                "response_format": "sys.pcm",  # sys.pcmから変更
                "input": "tts.utf-8",  # .streamを削除
                "enoutput": False,
                "enaudio": True
            }
        }
        send_json_request(client_socket, tts_setup)
        receive_response(client_socket)

        # MeloTTS推論
        logger.info("MeloTTS推論を開始")
        inference_request = {
            "request_id": "3",
            "work_id": "melotts.1001",  # work_idを修正
            "action": "inference",
            "object": "tts.utf-8",
            "data": "Hello I am M five Stack."
        }
        send_json_request(client_socket, inference_request)
        response = receive_response(client_socket)
        
        if response and response.get('error', {}).get('code') != 0:
            logger.error(f"推論エラー: {response.get('error', {}).get('message')}")
        else:
            logger.info("音声合成が完了しました")
        
        time.sleep(5)
        
        # リセット
        logger.info("リセットコマンドを送信")
        reset_request = {
            "request_id": "4",
            "work_id": "sys",
            "action": "reset"
        }
        send_json_request(client_socket, reset_request)
        receive_response(client_socket)

    except Exception as e:
        logger.error(f'予期しないエラーが発生: {e}', exc_info=True)
    finally:
        logger.info("接続をクローズ")
        client_socket.close()
        logger.info("スクリプト終了")

if __name__ == '__main__':
    main()