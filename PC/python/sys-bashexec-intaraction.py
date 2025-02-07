import socket
import json
import argparse

def receive_and_display_responses(sock):
   while True:
       try:
           data = sock.recv(4096).decode()
           if not data:
               break
           response = json.loads(data)
           
           if "error" in response and response["error"]["code"] != 0:
               print(f"Error {response['error']['code']}: {response['error']['message']}")
               continue
               
           if "data" in response and isinstance(response["data"], dict):
               if "delta" in response["data"]:
                   print(response["data"]["delta"], end="")
           
           if data.find('"finish":true') != -1:
               break
       except Exception as e:
           print(f"Error: {e}")
           break

def main(host, port):
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
       try:
           client.connect((host, port))
           print(f'Connected to {host}:{port}')
           
           while True:
               command = input("Enter command: ")
               request = {
                   "request_id": "1",
                   "work_id": "sys",
                   "action": "bashexec",
                   "object": "sys.stream",
                   "data": {
                       "index": 0,
                       "delta": command + "\n",
                       "finish": True
                   }
               }
               
               json_str = json.dumps(request)
               client.send(json_str.encode())
               receive_and_display_responses(client)
               
       except KeyboardInterrupt:
           print("\nExiting...")
       except ConnectionRefusedError:
           print(f"Connection refused to {host}:{port}")
       except Exception as e:
           print(f"Error: {e}")

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('--host', default='localhost')
   parser.add_argument('--port', type=int, default=10001)
   args = parser.parse_args()
   
   main(args.host, args.port)