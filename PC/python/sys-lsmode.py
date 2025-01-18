#システムモードのリストを取得するためのコード

import socket
import json
import argparse

def receive_full_data(sock):
    data = b''
    while True:
        packet = sock.recv(4096)
        if not packet:
            break
        data += packet

        if b'\n' in data:
            break

    return data.split(b'\n')

def main(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f'Connected to server at {host}:{port}')

        # システムモードリスト取得リクエスト
        lsmode_json_data = {
            "request_id": "001",
            "work_id": "sys",
            "action": "lsmode"
        }
        
        # JSONデータの送信
        json_string = json.dumps(lsmode_json_data)
        client_socket.sendall(f"{len(json_string):<10}".encode('utf-8'))
        client_socket.sendall(json_string.encode('utf-8'))

        # レスポンスの受信と表示
        while True:
            data_packets = receive_full_data(client_socket)
            if not data_packets:
                print("No more data from server, closing connection...")
                break

            for data in data_packets:
                if not data:
                    continue

                try:
                    response = data.decode("utf-8")
                    print(f'Received response: {response}')
                    json_data = json.loads(response)
                    print("System modes:", json.dumps(json_data, indent=2))
                    return  # 応答を受け取ったら終了

                except json.JSONDecodeError as e:
                    print(f'Error parsing JSON: {e}')
                except Exception as e:
                    print(f'Unexpected error: {e}')

    finally:
        client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Client to send JSON data.')
    #parser.add_argument('--host', type=str, default='localhost', help='Server hostname (default: localhost)')
    parser.add_argument('--host', type=str, default='m5stack-LLM.local', help='Server hostname (default: m5stack-LLM.local)')
    parser.add_argument('--port', type=int, default=10001, help='Server port (default: 10001)')

    args = parser.parse_args()
    main(args.host, args.port)