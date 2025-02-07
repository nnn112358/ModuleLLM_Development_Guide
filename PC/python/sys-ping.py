import socket
import json
import argparse

def main(host, port):
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
       # サーバー接続
       client.connect((host, port))
       print(f'Connected to {host}:{port}')
       
       # リクエストデータ作成
       request = {
           "request_id": "sys_ping",
           "work_id": "sys",
           "action": "ping",
           "object": "None",
           "data": "None"
       }
       
       # データ送信
       json_str = json.dumps(request)
       client.sendall(f"{len(json_str):<10}".encode() + json_str.encode())
       print(f'\nSent ping:\n{json.dumps(request, indent=2)}')
       
       # レスポンス受信
       response = b''
       while b'\n' not in response:
           chunk = client.recv(4096)
           if not chunk:
               break
           response += chunk
           
       # 結果表示
       print(f'\nReceived pong:\n{json.dumps(json.loads(response.decode()), indent=2)}')

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('--host', default='localhost')
   parser.add_argument('--port', type=int, default=10001)
   args = parser.parse_args()
   
   main(args.host, args.port)


