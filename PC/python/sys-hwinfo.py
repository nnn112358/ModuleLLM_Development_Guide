import socket
import json

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

        # ハードウェア情報リクエストデータ
        hwinfo_json_data = {
            "request_id": "1",
            "work_id": "sys",
            "action": "hwinfo",
            "object": "None",
            "data": "None"
        }
        
        # JSONデータの送信
        json_string = json.dumps(hwinfo_json_data)
        client_socket.sendall(f"{len(json_string):<10}".encode('utf-8'))
        client_socket.sendall(json_string.encode('utf-8'))
        print(f'Sent hardware info request: {json_string}')

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
                    print("Hardware info response:", json.dumps(json_data, indent=2))
                    return  # 応答を受け取ったら終了

                except json.JSONDecodeError as e:
                    print(f'Error parsing JSON: {e}')
                except Exception as e:
                    print(f'Unexpected error: {e}')

    finally:
        client_socket.close()

if __name__ == '__main__':
    host = "192.168.20.8"  # サーバーのIPアドレス
    port = 10001           # サーバーのポート番号
    main(host, port)