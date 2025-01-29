##うまくうごかない

import socket
import json
import argparse
import base64
import cv2
import numpy as np
from datetime import datetime

def create_tcp_connection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def send_json(sock, data):
    json_data = json.dumps(data, ensure_ascii=False) + '\n'
    sock.sendall(json_data.encode('utf-8'))

def receive_response(sock):
    response = ''
    while True:
        part = sock.recv(4096).decode('utf-8')
        response += part
        if '\n' in response:
            break
    return response.strip()

def create_vlm_setup_data():
    return {
        "request_id": "vlm_setup",
        "work_id": "vlm",
        "action": "setup",
        "object": "vlm.setup",
        "data": {
            "model": "internvl2.5-1B-ax630c",
            "response_format": "vlm.utf-8.stream",
            "input": ["vlm.utf-8.stream"],
            "enoutput": True,
            "enkws": True,
            "max_token_len": 255,
            "prompt": "test"
        }
    }

def setup_vlm(sock):
    init_data = create_vlm_setup_data()
    send_json(sock, init_data)
    response = receive_response(sock)
    response_data = json.loads(response)
    
    if response_data.get('error', {}).get('code', -1) != 0:
        print(f"Error: {response_data.get('error')}")
        return None
    
    return response_data.get('work_id')

def capture_and_save_image(camera):
    ret, frame = camera.read()
    if not ret:
        print("カメラからの画像取得に失敗しました")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"capture_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename

def send_image_and_prompt(sock, work_id, image_path, prompt, is_file=True):
    # 画像データの取得
    if is_file:
        with open(image_path, 'rb') as f:
            image_data = f.read()
    
    # 画像データを送信
    image_json = {
        "RAW": len(image_data),
        "request_id": "vlm_inference",
        "work_id": work_id,
        "action": "inference",
        "object": "cv.jpeg.base64"
    }
    send_json(sock, image_json)
    sock.sendall(image_data)

    # プロンプトを送信
    prompt_json = {
        "request_id": "vlm_inference",
        "work_id": work_id,
        "action": "inference",
        "object": "vlm.utf-8.stream",
        "data": {
            "delta": prompt,
            "index": 0,
            "finish": True
        }
    }
    send_json(sock, prompt_json)



def capture_image(camera):
    """カメラから画像を取得し、ファイルとして保存します"""
    ret, frame = camera.read()
    if not ret:
        print("カメラからの画像取得に失敗しました")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"capture_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"画像を保存しました: {filename}")
    return filename


def main(host, port):
    sock = create_tcp_connection(host, port)
    camera = cv2.VideoCapture(0)  # USBカメラを初期化
    
    if not camera.isOpened():
        print("カメラのオープンに失敗しました")
        return

    try:
        print("VLMをセットアップ中...")
        vlm_work_id = setup_vlm(sock)
        if not vlm_work_id:
            return
        print("セットアップ完了")
        
        while True:
            input_type = input("入力方法を選択してください（1: USBカメラ, 2: 画像ファイル, exit: 終了）: ")
            
            if input_type.lower() == 'exit':
                break
            
            if input_type == '1':
                print("撮影を実行します...")
                image_path = capture_image(camera)
                if image_path is None:
                    continue
            else:
                image_path = input("画像のパスを入力してください: ")
            
            prompt = "何が映っているのか説明してください"
            send_image_and_prompt(sock, vlm_work_id, image_path, prompt)
            
            while True:
                response = receive_response(sock)
                response_data = json.loads(response)
                
                if 'data' in response_data:
                    delta = response_data['data'].get('delta', '')
                    finish = response_data['data'].get('finish', False)
                    
                    print(delta, end='', flush=True)
                    
                    if finish:
                        print()
                        break
        
        # セッションの終了
        send_json(sock, {
            "request_id": "vlm_exit",
            "work_id": vlm_work_id,
            "action": "exit"
        })
        
    finally:
        camera.release()
        cv2.destroyAllWindows()
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VLM TCP Client')
    parser.add_argument('--host', type=str, default='m5stack-LLM.local', 
                       help='サーバーホスト名 (デフォルト: m5stack-LLM.local)')
    parser.add_argument('--port', type=int, default=10001,
                       help='サーバーポート (デフォルト: 10001)')
    
    args = parser.parse_args()
    main(args.host, args.port)