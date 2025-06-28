import logging
from flask import Flask, request, Response
import requests
import os
from werkzeug.exceptions import HTTPException
import json
#from werkzeug.server.shutdown import shutdown_server
import socket
import threading
import time
import random
import struct
from flask_sock import Sock
import base64

from flask_socketio import SocketIO, send, emit
#import socketio


# 로컬 서버의 URL
LOCAL_SERVER_URL = "http://localhost:8188"
m_port01=5347
m_port02=8347
m_timePeriod=200
m_sssChunk='Sosdijfaoisdjfjwefnmvnh932nvirnfu92ncsS'
m_endChunk='Easdoijfidscmckmkeovsopvm20fmv29vkmfmfE'
#return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

#gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 module:app

app = Flask(__name__)
sock = Sock(app)

sock_clients = []
# 로그 설정
logging.basicConfig(filename='server_output03.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


#socketio = SocketIO(app, cors_allowed_origins="*")

def checkBinaryType(content_type):
    binary_mime_types = [
        #application/octet-stream
        "application/octet-stream", "application/zip", "application/gzip",
        "application/x-tar", "application/pdf", "application/msword",
        "application/vnd.ms-excel", "application/vnd.ms-powerpoint",
        "application/x-7z-compressed", "application/x-rar-compressed",
        "application/x-bzip", "application/x-bzip2", "application/x-executable",
        "image/", "audio/", "video/", "font/"
    ]

    return any(content_type.startswith(mime) for mime in binary_mime_types)
    
def websockLog(message, file_path='server_output04.log'):
    with open(file_path, 'a') as log_file:
        log_file.write(str(m_port02)+" "+message + '\n')

websockLog("start")

@sock.route('/ws')
def echo(sock):
    sock_clients.append(sock)
    msg='{"type": "status", "data": {"status": {"exec_info": {"queue_remaining": 0}}, "sid":"9f583d8724674873954bcb8dec717c3b"}}'
    msg='{"type": "status", "data": {"status": {"exec_info": {"queue_remaining": 0}}, "sid": "7e30fb7aa73546f6b368a191ca54702a"}}'
    websockLog(f"---------------websock conect------------------")
    #sock.send(msg)
    aa={}
    aa["cmd"]="connectWebsockFromServer"
    json_data = json.dumps(aa,indent=4)
    if m_client_num>0:
      sendToClient(json_data)
    while True:
        data = sock.receive()
        print(f"-- websock 바깥클라이언트로부터 메시지 수신: {data}")
        websockLog(f"--websock 바깥클라이언트로부터 메시지 수신: {data}")
        #sock.send(data)
        aa["cmd"]="sendsockFromServer"
        json_data = json.dumps(aa,indent=4)
        if m_client_num>0:
          sendToClient(json_data)
    

"""
# 클라이언트로부터 메시지를 받아서 WebSocket 서버로 전송
@socketio.on('message')
def handle_message(msg):
    print(f"Received from client: {msg}"+str(request.sid))
    websockLog(f"Received from client: {msg}"+str(request.sid))
    #sio.send(msg)
    
# 클라이언트 WebSocket 연결 시 연결 처리
@socketio.on('connect')
def handle_connect():
    print("Client connected to proxy server. "+str(request.sid)+" "+str(request.namespace))
    websockLog("Client connected to proxy server. "+str(request.sid)+" "+str(request.namespace))
    #client_sockets[request.sid] = request.namespace
    #TARGET_WS_SERVER = 'http://34.30.238.162:7222'  # 서버 주소
    #sio.connect(TARGET_WS_SERVER)
    

# 클라이언트 WebSocket 연결 종료 시 연결 종료 처리
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected from proxy server.")
    websockLog("Client disconnected from proxy server.")
    #if client_socket:
    #    client_socket.close()

"""





def sendDataSocket(client_socket, data):
  try:    
    # 데이터의 길이를 4바이트로 변환
    data_length = len(data)
    packed_length = struct.pack('!I', data_length)
    
    client_socket.sendall(m_sssChunk.encode())
    # 1. 데이터 길이를 전송
    client_socket.sendall(packed_length)
    
    # 2. 데이터를 전송, 끝에 '\n' 추가 (예시로)
    client_socket.sendall(data )  # '\n'으로 끝내기
    client_socket.sendall(m_endChunk.encode())
    
    #print(f"Sent data: {data}")
  except socket.error as e:
    print(f"handle_client socket error: {e}")
      
def errFix(client_socket):
  return


def receive_full_data(client_socket):
    # 서버에서 전송할 데이터의 길이를 먼저 받음 (4바이트로 길이를 전송한다고 가정)
    sssChk = client_socket.recv(len(m_sssChunk.encode()))
    chk01=1
    chk02=0
    if m_sssChunk.encode() == sssChk:
        chk01=0
        #print("서버에서 전송을 시작하는 신호를 받았습니다.")
    else:
        print("error sssChk error recv=",sssChk.decode('utf-8', errors='ignore'), flush=True)

    length_data = client_socket.recv(4)

    # 서버가 전송한 데이터 길이가 없으면 종료
    if len(length_data) == 0:
        print("서버에서 전송된 길이 정보를 받을 수 없습니다.")
        return
    
    # 길이 데이터를 unpack하여 실제 데이터의 길이로 변환
    data_length = struct.unpack('!I', length_data)[0]
    print(f"서버에서 보내는 데이터의 길이: {data_length} bytes")
    
    if data_length>900100100:
      print("error over len=" ,data_length, flush=True)
      chk02=1
    else:
      chk02=0
      
     
    if chk01+chk02 > 0:
      #xxx = client_socket.recv(65536)
      #errFix(client_socket)
      print("receive_full_data chk error")
      return "receive_full_data chk error"
    # 데이터를 길이만큼 받음
    complete_data = b''
    while len(complete_data) < data_length:
        remaining_length = data_length - len(complete_data)
        data_chunk = client_socket.recv(min(65536, remaining_length))  # 남은 길이만큼 받음
        if not data_chunk:
            print("데이터를 받을 수 없습니다. 서버 연결 종료?")
            break
        complete_data += data_chunk

    # 받은 데이터를 처리
    endcode = client_socket.recv(len(m_sssChunk.encode()))
    # 데이터의 끝에서 종료 신호 (예: 'END')를 받는지 확인
    if m_endChunk.encode() == endcode:
        chk03=0
        #print("서버에서 전송을 종료하는 신호를 받았습니다.")
    
    try:
        decoded_data = complete_data.decode('utf-8', errors='ignore')
        #print(f"받은 데이터: {decoded_data}")
    except UnicodeDecodeError:
        print("받은 데이터는 UTF-8로 디코딩할 수 없습니다. 원본 바이너리 데이터:")
        print(complete_data)

    return decoded_data



class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

m_person = Person("Alice", 25)


m_flag={"f":111,"xxxx":0,"jsondata":0,"j":0}

#m_flag["xxxx2"]=m_person



def test():
  print(m_flag)

test()
#exit()
def is_json(my_str):
    try:
        json.loads(my_str)
        return True
    except json.JSONDecodeError:
        return False

# 클라이언트 연결을 처리할 함수
def handle_client(client_socket):
    global m_flag,m_server_socket,m_client_num,m_client_socket,sock_clients
    while True:
        try:
            data = receive_full_data(client_socket)#client_socket.recv(4096)
        except socket.error as e:
            print(f"handle_client socket error: {e}")
            
        if data:
            message = data#.decode().strip()
            if is_json(message):
              print("################################json")
              jsondata = json.loads(message)
              message="json"
            else:
              message=message
          
            print(f"받은 데이터: {message}", flush=True)
            if message == "exit":
              print("종료 메시지를 받았습니다. 서버를 종료합니다.")
              client_socket.close()  # 클라이언트 연결 종료
              m_server_socket.close()  # 서버 종료
              exit()  # 서버 종료
            elif message == "kkaxnvowendmfwemdomdowemcmsklcnkladn":
              m_client_socket=client_socket
              m_client_num = m_client_num + 1
              print(f"kkax 새로운 클라이언트 연결:  n={m_client_num}", flush=True)
              print("kkax dddd",flush=True)
            elif message == "json":
              if jsondata["check"]=="sendsock":
                  try:
                    print(" sock_clients len = ",len(sock_clients))
                    sock_clients[-1].send(jsondata["msg"])  # 마지막 클라이언트에게 메시지 전송
                  except Exception as e:
                    print(f"---websock sending Error sending message: {e}")
                  #sock.send(jsondata["msg"])
                  print("-----",flush=True)
                  print(f" -----bb 내부 클리이언트로부터 웹속 메세지받았습니다 ",jsondata["msg"],flush=True)
                  
              elif jsondata["check"]=="aabbccqqa":
                  key=jsondata["key"]
                  print("key=",key)
                  m_flag[key]["f"]=112
                  m_flag[key]["jsondata"]=jsondata
                  m_flag[key]["j"]=jsondata
                  print("okooooooooo")
              else:
                  print(" jsondata check error")
            else:
              time.sleep(3)
            #client_socket.sendall(f"ㅏkk서버로부터 응답: {data.decode()}".encode())
        
        else:
            print(client_socket, flush=True)
            #print(vars(client_socket))
            print("클라이언트 연결 종료", flush=True)
            client_socket.close()
            m_client_num = m_client_num - 1
            break

m_client_socket=None
m_client_num = 0

def serverStart():
  global m_client_num
  # 서버 소켓 설정
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(('0.0.0.0', m_port01))
  print("서버가 시작되었습니다..." + str(m_client_num)," port=",m_port01 )
  server_socket.listen(5)
  return server_socket

m_server_socket=serverStart()

m_cnt=0
def connectChk(client_socket):
  global m_cnt
  while True:
    time.sleep(m_timePeriod)
    mm=str(m_port01)+" "+str(m_cnt)+" from server to client connect chek"+str(random.random())
    m_cnt += 1
    #print(mm)
    #client_socket.sendall(mm.encode())
    #sendDataSocket(client_socket,mm.encode())


def serverLoop():
  global m_client_num,m_client_socket
  print("serverLoop", flush=True)
  while True:
    client_socket, addr = m_server_socket.accept()
    
    #client_socket.sendall(f"connect CHK 001123".encode())
    sendDataSocket(client_socket,f"connect CHK 001123".encode())
    # 각 클라이언트마다 스레드를 생성하여 처리
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    ttt2 = threading.Thread(target=connectChk, args=(client_socket,))
    ttt2.start()

server_thread = threading.Thread(target=serverLoop)
server_thread.start()

def sendToClient(data):
  global m_client_socket
  #client_socket.sendall(f"ㅏkk서버로부터 응답: {data.decode()}".encode())
  if m_client_socket is not None:
    #m_client_socket.sendall(data.encode())
    sendDataSocket(m_client_socket,data.encode())
  return




@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def proxy(path=None):
    global m_flag,m_server_socket,m_client_num
    
    pathkey=path
    if path is None:
        path = ''
        pathkey=path
    """
    if pathkey in m_flag and m_flag[pathkey]["f"]==112:
        key=pathkey
        if m_flag[key]["j"]["content-type"]=="None":
          return Response(m_flag[key]["j"]["content"], status=m_flag[key]["j"]["status"],headers=m_flag[key]["j"]["headers"])#,content_type=m_flag["j"]["content-type"])
        else:
          return Response(m_flag[key]["j"]["content"], status=m_flag[key]["j"]["status"],headers=m_flag[key]["j"]["headers"],content_type=m_flag[key]["j"]["content-type"])
    """
                        
    while m_flag["f"] == 100:
      time.sleep(0.3)
    m_flag["f"] = 100
    print("k k path=",path," m_client_num =",m_client_num , flush=True)
    
    #sendToClient("senddata test 0011")
    # 경로가 '/'일 경우 처리
    
    
    # "exit" 경로를 처리하는 로직 추가
    if path == 'exit':
        logging.info("Server is shutting down...")
        shutdown_server()
        return "Server is shutting down...", 200

    url = f"{LOCAL_SERVER_URL}/{path}"

    # 로그에 기록할 정보들
    method = request.method
    data = request.data.decode('utf-8') if request.data else None
    headers = dict(request.headers)
    args = dict(request.args)
    
    aa={}
    aa["key"]=pathkey
    aa["cmd"]="request"
    aa["url"]=url
    aa["method"]=request.method
    aa["data"]= request.data.decode('utf-8') if request.data else None
    aa["headers"] = dict(request.headers)
    aa["args"] = dict(request.args)
    aa["files"]=""#dict(request.files) if len(request.files) > 0 else ""
    print("------aa[files]--",aa["files"],flush=True)
    
    if True:#files in request:
        if len(request.files)>0: #file in request.files:
            ddic=[]
            for key, file in request.files.items():
                # 파일 이름과 파일의 다른 정보를 가져옴
                filename = file.filename
                content_type = file.content_type
                filedata= base64.b64encode( file.stream.read() ).decode('utf-8')
                ddic.append((key, filename, content_type ,filedata))
                print(f"파일 키: {key}, 파일 이름: {filename}, 파일 MIME 타입: {content_type}")
            aa["files"]=ddic
            #print("--------file-----",request.files,flush=True)
            #aa["files"]=dict(request.files)
        
    #json_data = json.dumps(my_obj.to_dict(), indent=4)
    print("--chk01--",flush=True)
    json_data = json.dumps(aa,indent=4)
    print("--chk02--",flush=True)
    if m_client_num>0:
      sendToClient(json_data)
    else:
      return "aaaddkk" + str(m_client_num)
    # 로그 기록
    logging.info(f"Request Method: {method}")
    logging.info(f"Request URL: {url}")
    logging.info(f"Request Headers: {headers}")
    logging.info(f"Request Args: {args}")
    logging.info(f"Request Data: {data}")
    """
    # 각 HTTP 메소드에 맞는 처
    if method == 'GET':
        response = requests.get(url, params=request.args)
    elif method == 'POST':
        response = requests.post(url, data=request.data, headers=request.headers)
    elif method == 'PUT':
        response = requests.put(url, data=request.data, headers=request.headers)
    elif method == 'DELETE':
        response = requests.delete(url, headers=request.headers)
    elif method == 'PATCH':
        response = requests.patch(url, data=request.data, headers=request.headers)
    elif method == 'OPTIONS':
        response = requests.options(url)
    elif method == 'HEAD':
        response = requests.head(url)
    """
    key=path
    m_flag[key]={}
    m_flag[key]["f"]=100
    m_flag["f"]=100
    while m_flag[key]["f"] == 100:
      time.sleep(0.1)
    
    if m_flag[key]["f"] == 112:
      m_flag[key]["size"]=len(m_flag[key]["j"]["content"])
      m_flag["f"]=111
      print("m_flag m_flag okokokokaaaaqqqq")
      print("---content len=",len(m_flag[key]["j"]["content"]), flush=True)
      #Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
      if m_flag[key]["j"]["content-type"]=="None":
          return Response(m_flag[key]["j"]["content"], status=m_flag[key]["j"]["status"],headers=m_flag[key]["j"]["headers"])#,content_type=m_flag["j"]["content-type"])
      else:
          if checkBinaryType(m_flag[key]["j"]["content-type"]):#'image' in m_flag[key]["j"]["content-type"]:
              m_flag[key]["j"]["content"]=base64.b64decode(m_flag[key]["j"]["content"])
          return Response(m_flag[key]["j"]["content"], status=m_flag[key]["j"]["status"],headers=m_flag[key]["j"]["headers"],content_type=m_flag[key]["j"]["content-type"])

      #       content_type   
    else:
      print("its eeeeeelsesssselslslels")
      return "aaaaaa"
    
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    return "xxxx"
    # 응답의 원본 내용을 그대로 클라이언트로 반환
    #return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

@app.errorhandler(405)
def handle_invalid_method(error):
    return Response(
        f"Invalid HTTP Method! The method {request.method} is not allowed for this route.",
        status=405,
        content_type="text/plain"
    )

def shutdown_server():
    """서버 종료"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    # 서버 실행
    time.sleep(1)
    #socketio.run(app, host='0.0.0.0', port=m_port02, allow_unsafe_werkzeug = True)
    app.run(host='0.0.0.0', port=m_port02)
