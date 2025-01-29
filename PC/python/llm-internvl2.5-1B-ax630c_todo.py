##うまく動かない。



import socket
import json
import argparse
import base64

def create_tcp_connection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30.0)  # C++実装に合わせて30秒のタイムアウトを設定
    sock.connect((host, port))
    return sock

def send_json(sock, data):
    json_data = json.dumps(data, ensure_ascii=False) + '\n'
    sock.sendall(json_data.encode('utf-8'))

def receive_response(sock):
    response = ''
    try:
        while True:
            part = sock.recv(4096).decode('utf-8')
            if not part:
                break
            response += part
            if '\n' in response:
                break
    except socket.timeout:
        print("応答タイムアウト")
        return None
    return response.strip()

def create_vlm_setup_data():
    return {
        "request_id": "vlm_setup",
        "work_id": "vlm",
        "action": "setup",
        "object": "vlm.setup",
        "data": {
            "model": "internvl2.5-1B-ax630c",  # api_vlm.hに合わせてモデル名を修正
            "response_format": "vlm.utf-8.stream",
            "input": ["vlm.utf-8.stream"],  # 入力フォーマットを修正
            "enoutput": True,
            "enkws": True,
            "max_token_len": 255,
            "prompt": ""  # 空の文字列に変更
        }
    }

def setup_vlm(sock):
    init_data = create_vlm_setup_data()
    send_json(sock, init_data)
    response = receive_response(sock)
    if response is None:
        return None
    response_data = json.loads(response)
    
    if response_data.get('error', {}).get('code', -1) != 0:
        print(f"エラー: {response_data.get('error')}")
        return None
    
    return response_data.get('work_id')

def send_image_and_prompt(sock, work_id, image_path, prompt):
    # 画像ファイルを読み込み
    """
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # 画像データを送信
    image_json = {
        "RAW": len(image_data),
        "request_id": "vlm_inference",
        "work_id": work_id,
        "action": "inference",
        "object": "yolo.jpeg.base64"  # オブジェクトタイプを修正
    }
    send_json(sock, image_json)
    sock.sendall(image_data)
    """
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

def main(host, port):
    try:
        sock = create_tcp_connection(host, port)
        print("VLMをセットアップ中...")
        vlm_work_id = setup_vlm(sock)
        if not vlm_work_id:
            return
        print("セットアップ完了")
        
        while True:
            image_path = "test2.jpg"
            image_path = input("filename: ")

            if image_path.lower() == 'exit':
                break
                
            prompt = "Describe in 60 characters"

            try:
                send_image_and_prompt(sock, vlm_work_id, image_path, prompt)
                
                while True:
                    response = receive_response(sock)
                    if response is None:
                        break
                    response_data = json.loads(response)
                    
                    if 'data' in response_data:
                        delta = response_data['data'].get('delta', '')
                        finish = response_data['data'].get('finish', False)
                        
                        print(delta, end='', flush=True)
                        
                        if finish:
                            print()
                            break
            except Exception as e:
                print(f"エラーが発生しました: {e}")
                continue
        
        # セッションの終了
        send_json(sock, {
            "request_id": "vlm_exit",
            "work_id": vlm_work_id,
            "action": "exit"
        })
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VLM TCP Client')
    parser.add_argument('--host', type=str, default='m5stack-LLM.local', 
                       help='サーバーホスト名 (デフォルト: m5stack-LLM.local)')
    parser.add_argument('--port', type=int, default=10001,
                       help='サーバーポート (デフォルト: 10001)')
    
    args = parser.parse_args()
    main(args.host, args.port)