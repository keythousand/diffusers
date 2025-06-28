import os
import sys
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
from datetime import datetime
import urllib.parse

from flask_socketio import SocketIO, send, emit
#import socketio


print("ver check 0000020")

# 濡쒖뺄 �쒕쾭�� URL
LOCAL_SERVER_URL = "http://localhost:8188"
m_port01=5395
m_port02=8395
m_timePeriod=200
m_sssChunk='Sosdijfaoisdjfjwefnmvnh932nvirnfu92ncsS'
m_endChunk='Easdoijfidscmckmkeovsopvm20fmv29vkmfmfE'
#return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

#gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 module:app

app = Flask(__name__)
sock = Sock(app)

sock_clients = []


m_client_socketList=[]

# 濡쒓렇 �ㅼ젙
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
    print("--- sock request.args:", request.args)  # ImmutableMultiDict 異쒕젰
    print("--- sock request.args as dict:", request.args.to_dict())  # �뺤뀛�덈━ 蹂��� �� 異쒕젰

    sock_clients.append(sock)
    msg='{"type": "status", "data": {"status": {"exec_info": {"queue_remaining": 0}}, "sid":"9f583d8724674873954bcb8dec717c3b"}}'
    msg='{"type": "status", "data": {"status": {"exec_info": {"queue_remaining": 0}}, "sid": "7e30fb7aa73546f6b368a191ca54702a"}}'
    print(f"---------------websock conect------------------ len sock_clients =",len(sock_clients))
    websockLog(f"---------------websock conect------------------ len sock_clients =" + str( len(sock_clients)))
    #sock.send(msg)
    aa={}
    aa["cmd"]  = "connectWebsockFromServer"
    aa["args"] = urllib.parse.urlencode(request.args)#dict(request.args)
    print (" --------------------aa[args] = ",aa["args"])
    
    json_data = json.dumps(aa,indent=4)
    if m_client_num>0:
      sendToClient(json_data)
    while True:
        try:
            data = sock.receive()
            if data is None:  # 硫붿떆吏�媛� None�� 寃쎌슦 �곌껐 醫낅즺�� 寃껋쑝濡� 泥섎━
                sock_clients.pop()
                print("websock �대씪�댁뼵�멸� �곌껐�� 醫낅즺�덉뒿�덈떎.",len(sock_clients),flush=True)
                break
        except websockets.exceptions.ConnectionClosed:
            # WebSocket �곌껐�� �ロ삍�� �� �덉쇅 泥섎━
            sock_clients.pop()
            print("WebSocket �곌껐�� 醫낅즺�섏뿀�듬땲��.")
            break  # 猷⑦봽瑜� 醫낅즺�섍퀬 WebSocket �곌껐�� �レ쓬
        
        print(f"-- websock 諛붽묑�대씪�댁뼵�몃줈遺��� 硫붿떆吏� �섏떊: {data}")
        websockLog(f"--websock 諛붽묑�대씪�댁뼵�몃줈遺��� 硫붿떆吏� �섏떊: {data}")
        #sock.send(data)
        aa["cmd"]="sendsockFromServer"
        aa["data"]=data
        json_data = json.dumps(aa,indent=4)
        if m_client_num>0:
          sendToClient(json_data)
    print(" ----------------------sock func end-------------")
    

"""
# �대씪�댁뼵�몃줈遺��� 硫붿떆吏�瑜� 諛쏆븘�� WebSocket �쒕쾭濡� �꾩넚
@socketio.on('message')
def handle_message(msg):
    print(f"Received from client: {msg}"+str(request.sid))
    websockLog(f"Received from client: {msg}"+str(request.sid))
    #sio.send(msg)
    
# �대씪�댁뼵�� WebSocket �곌껐 �� �곌껐 泥섎━
@socketio.on('connect')
def handle_connect():
    print("Client connected to proxy server. "+str(request.sid)+" "+str(request.namespace))
    websockLog("Client connected to proxy server. "+str(request.sid)+" "+str(request.namespace))
    #client_sockets[request.sid] = request.namespace
    #TARGET_WS_SERVER = 'http://34.30.238.162:7222'  # �쒕쾭 二쇱냼
    #sio.connect(TARGET_WS_SERVER)
    

# �대씪�댁뼵�� WebSocket �곌껐 醫낅즺 �� �곌껐 醫낅즺 泥섎━
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected from proxy server.")
    websockLog("Client disconnected from proxy server.")
    #if client_socket:
    #    client_socket.close()

"""





m_sendDataSocket = 0
m_receive_full_data = 0

def client_status_print():
    print("-- client_status_print  m_sendDataSocket=",m_sendDataSocket,"   m_receive_full_data",m_receive_full_data);

def client_status_reset():
    m_sendDataSocket=0
    m_receive_full_data=0

def sendDataSocket(client_socket, data):
  global m_sendDataSocket
  while m_sendDataSocket == 1:
      time.sleep(0.01)
  m_sendDataSocket = 1
  try:    
    # �곗씠�곗쓽 湲몄씠瑜� 4諛붿씠�몃줈 蹂���
    data_length = len(data)
    packed_length = struct.pack('!I', data_length)
    
    client_socket.sendall(m_sssChunk.encode())
    # 1. �곗씠�� 湲몄씠瑜� �꾩넚
    client_socket.sendall(packed_length)
    
    # 2. �곗씠�곕� �꾩넚, �앹뿉 '\n' 異붽� (�덉떆濡�)
    client_socket.sendall(data )  # '\n'�쇰줈 �앸궡湲�
    client_socket.sendall(m_endChunk.encode())
    
    #print(f"Sent data: {data}")
  except socket.error as e:
    print(f"sendDataSocket   socket error: {e}")
  m_sendDataSocket = 0
      
def errFix(client_socket):
  return

m_flag={"f":111,"xxxx":0,"jsondata":0,"j":0}

def is_json(my_str):
    try:
        json.loads(my_str)
        return True
    except json.JSONDecodeError:
        return False


m_m_m=1
# �대씪�댁뼵�� �곌껐�� 泥섎━�� �⑥닔
def handle_client(client_socket):
 global m_flag,m_server_socket,m_client_num,m_client_socket,sock_clients,m_client_socketList
 print("000000000000-----------------------------------newnewnew")

 def recv_full(client_socket, expected_length):
    data = b""
    errcode=0
    while len(data) < expected_length:
        packet = client_socket.recv(expected_length - len(data))
        if not packet:
            print (" recv_full �곌껐�� �딆뼱議뚯뒿�덈떎.")
            errcode=1
            break;
            #raise ConnectionError(" recv_full �곌껐�� �딆뼱議뚯뒿�덈떎.")
        data += packet
    return (data,errcode)



    
#m_receive_full_data = 0
 def receive_full_data(client_socket):
  try:
    global m_receive_full_data
    while m_receive_full_data == 1:
      time.sleep(0.01)
    #m_receive_full_data = 1
  
    # �쒕쾭�먯꽌 �꾩넚�� �곗씠�곗쓽 湲몄씠瑜� 癒쇱� 諛쏆쓬 (4諛붿씠�몃줈 湲몄씠瑜� �꾩넚�쒕떎怨� 媛���)
    (sssChk,errcode) = recv_full(client_socket, len(m_sssChunk.encode()))
    if errcode == 1 : 
        m_receive_full_data = 0
        return
    #sssChk = client_socket.recv(len(m_sssChunk.encode()))
    chk01=1
    chk02=0
    chk03=1
    if m_sssChunk.encode() == sssChk:
        chk01=0
        #print("�쒕쾭�먯꽌 �꾩넚�� �쒖옉�섎뒗 �좏샇瑜� 諛쏆븯�듬땲��.")
    else:
        print("error sssChk error recv=",sssChk.decode('utf-8', errors='ignore'), flush=True)

    (length_data,errcode) = recv_full(client_socket, 4)#client_socket.recv(4)
    if errcode == 1 : 
        m_receive_full_data = 0
        return

    # �쒕쾭媛� �꾩넚�� �곗씠�� 湲몄씠媛� �놁쑝硫� 醫낅즺
    if len(length_data) == 0:
        print("�쒕쾭�먯꽌 �꾩넚�� 湲몄씠 �뺣낫瑜� 諛쏆쓣 �� �놁뒿�덈떎.")
        m_receive_full_data=0
        return
    
    # 湲몄씠 �곗씠�곕� unpack�섏뿬 �ㅼ젣 �곗씠�곗쓽 湲몄씠濡� 蹂���
    data_length = struct.unpack('!I', length_data)[0]
    print(f"�쒕쾭�먯꽌 蹂대궡�� �곗씠�곗쓽 湲몄씠: {data_length} bytes")
    
    if data_length>900100100:
      print("error over len=" ,data_length, flush=True)
      chk02=1
    else:
      chk02=0
      
     
    if chk01+chk02 > 0:
      #xxx = client_socket.recv(65536)
      #errFix(client_socket)
      print("receive_full_data chk error")
      m_receive_full_data=0
      return "receive_full_data chk error"
    # �곗씠�곕� 湲몄씠留뚰겮 諛쏆쓬
    complete_data = b''
    while len(complete_data) < data_length:
        remaining_length = data_length - len(complete_data)
        data_chunk = client_socket.recv(min(65536, remaining_length))  # �⑥� 湲몄씠留뚰겮 諛쏆쓬
        if not data_chunk:
            print("�곗씠�곕� 諛쏆쓣 �� �놁뒿�덈떎. �쒕쾭 �곌껐 醫낅즺?")
            break
        complete_data += data_chunk

    # 諛쏆� �곗씠�곕� 泥섎━
    #endcode = client_socket.recv(len(m_sssChunk.encode()))
    (endcode,errcode) = recv_full(client_socket, len(m_endChunk.encode()))
    if errcode == 1 : 
        m_receive_full_data = 0
        return
    # �곗씠�곗쓽 �앹뿉�� 醫낅즺 �좏샇 (��: 'END')瑜� 諛쏅뒗吏� �뺤씤
    if m_endChunk.encode() == endcode:
        chk03=0
        #print("�쒕쾭�먯꽌 �꾩넚�� 醫낅즺�섎뒗 �좏샇瑜� 諛쏆븯�듬땲��.")
    else: 
        print("error endcode = " ,endcode)
    
    try:
        decoded_data = complete_data.decode('utf-8', errors='ignore')
    except UnicodeDecodeError:
        print("諛쏆� �곗씠�곕뒗 UTF-8濡� �붿퐫�⑺븷 �� �놁뒿�덈떎. �먮낯 諛붿씠�덈━ �곗씠��:")
        print(complete_data)

    m_receive_full_data = 0
    return decoded_data
  except :
      print(" --------****** ---------*****-------**** except except except m_receive_full_data");
      m_receive_full_data=0
#def handle_client(client_socket):
#    global m_flag,m_server_socket,m_client_num,m_client_socket,sock_clients,m_client_socketList
 print("---------- intent ?? chk")   
 if m_m_m == 1:
    mmRand=random.randint(1, 999999)
    print(mmRand,"--- �뚯폆 �대씪�댁뼵�� 由ъ떆釉뚯슜 �곕젅�쒓� �앹꽦�섏뿀�붾뜲 �쒖닔踰덊샇�� ",mmRand)
    while True:
        try:
            data = receive_full_data(client_socket)#client_socket.recv(4096)
        except socket.error as e:
            print(mmRand,f"handle_client socket error: {e}")
            client_socket.close()
            m_client_num = m_client_num - 1
            print(mmRand,"  except error (client reset) �곌껐 醫낅즺�덈떎  m_client_num=",m_client_num)
            client_status_print()
            client_status_reset()
        
            
        if data:
            message = data#.decode().strip()
            if is_json(message):
              print(mmRand,"################################json",flush=True)
              jsondata = json.loads(message)
              message="json"
            else:
              message=message
          
            #print(mmRand,f"諛쏆� �곗씠��: {message}", flush=True)
            if message == "exit":
              print(mmRand,"醫낅즺 硫붿떆吏�瑜� 諛쏆븯�듬땲��. �쒕쾭瑜� 醫낅즺�⑸땲��.",flush=True)
              client_socket.close()  # �대씪�댁뼵�� �곌껐 醫낅즺
              m_server_socket.close()  # �쒕쾭 醫낅즺
              exit()  # �쒕쾭 醫낅즺
            elif message == "kkaxnvowendmfwemdomdowemcmsklcnkladn":
              m_client_socketList.append(client_socket)
              m_client_socket=client_socket
              m_client_num = m_client_num + 1
              print(mmRand,f"kkax �덈줈�� �대씪�댁뼵�� �곌껐:  n={m_client_num}", flush=True)
              print(mmRand,"kkax dddd",flush=True)
            elif message == "json":
              if jsondata["check"]=="sendsock":
                  try:
                    print(mmRand," sock_clients len = ",len(sock_clients),flush=True)
                    sock_clients[-1].send(jsondata["msg"])  # 留덉�留� �대씪�댁뼵�몄뿉寃� 硫붿떆吏� �꾩넚
                  except Exception as e:
                    print(f"---websock sending Error sending message: {e}")
                  #sock.send(jsondata["msg"])
                  print(mmRand,"-----",flush=True)
                  print(mmRand,f" -----bb �대� �대━�댁뼵�몃줈遺��� �뱀냽 硫붿꽭吏�諛쏆븯�듬땲�� ",jsondata["msg"],flush=True)

              elif jsondata["check"]=="resendEcho":
                  kkaakaakaka=1111
                  print(mmRand,"----- ok i get resendEcho-----",flush=True)
              elif jsondata["check"]=="aabbccqqa":
                  key=jsondata["key"]
                  print("key=",key)
                  m_flag[key]["f"]=112
                  m_flag[key]["jsondata"]=jsondata
                  m_flag[key]["j"]=jsondata
                  print(mmRand,"okooooooooo",flush=True)
              else:
                  print(mmRand," jsondata check error",flush=True)
            else:
              time.sleep(3)
            #client_socket.sendall(f"�뢫k�쒕쾭濡쒕��� �묐떟: {data.decode()}".encode())
        
        else:
            time.sleep(0.1)
            print(mmRand,"cccc ",client_socket, flush=True)
            #print(vars(client_socket))
            print(mmRand,"---------- no data recive(closing client) need to reset �대씪�댁뼵�� �곌껐 醫낅즺 �� �곕젅�ㅼ쓣 break�⑸땲��. mmRand=",mmRand, flush=True)
            print(mmRand,"--- �뚯폆 �대씪�댁뼵�� 由ъ떆釉뚯슜 �곕젅�쒖쓣 醫낅즺�� �쒖닔踰덊샇�� ",mmRand)
            client_status_print()
            client_status_reset()
            client_socket.close()
            m_client_num = m_client_num - 1
            break
            
            

m_client_socket=None
m_client_num = 0

def serverStart():
  global m_client_num
  # �쒕쾭 �뚯폆 �ㅼ젙
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(('0.0.0.0', m_port01))
  print("�쒕쾭媛� �쒖옉�섏뿀�듬땲��..." + str(m_client_num)," port=",m_port01 )
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

def serverSocketClose():
  global m_server_socket,m_client_socket
  print("------serverSocketClose client")
  if m_client_socket != None:
   try:
    m_client_socket.shutdown(socket.SHUT_RDWR)
   except OSError:
    pass  # �뚯폆�� �대� �ロ엺 寃쎌슦 �덉쇅 臾댁떆
   finally:
    m_client_socket.close()  
  print("------serverSocketClose server")
  try:
    m_server_socket.shutdown(socket.SHUT_RDWR)
  except OSError:
    pass  # �뚯폆�� �대� �ロ엺 寃쎌슦 �덉쇅 臾댁떆
  finally:
    m_server_socket.close()
  
def serverLoop():
  global m_client_num,m_client_socket
  print("serverLoop", flush=True)
  while True:
    try:
      client_socket, addr = m_server_socket.accept()
    except OSError:
      print(" serverLoop �먯꽌 OSError媛� �좎꽌 猷⑦봽媛� 醫낅즺�섏뿀�듬땲��.")
      break  # �뚯폆�� �ロ엳硫� 猷⑦봽 醫낅즺
    #m_client_socket = client_socket  handle_client�먯꽌 泥섎━�쒕떎.
    #client_socket.sendall(f"connect CHK 001123".encode())
    print("-----------�대씪�댁뼵�� 由ъ뒯�덈떎   ---(cleint reset)")
    client_status_print()
    client_status_reset()
    sendDataSocket(client_socket,f"connect CHK 001123".encode())
    # 媛� �대씪�댁뼵�몃쭏�� �ㅻ젅�쒕� �앹꽦�섏뿬 泥섎━
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    #ttt2 = threading.Thread(target=connectChk, args=(client_socket,))
    #ttt2.start()

server_thread = threading.Thread(target=serverLoop)
server_thread.start()

def sendToClient(data):
  global m_client_socket
  #client_socket.sendall(f"�뢫k�쒕쾭濡쒕��� �묐떟: {data.decode()}".encode())
  if m_client_socket is not None:
    #m_client_socket.sendall(data.encode())
    sendDataSocket(m_client_socket,data.encode())
  return


def shutdown_server():
    """�쒕쾭 醫낅즺"""
    print("00-----shutdown_server")
    serverSocketClose()
    try:
        print("0-----shutdown_server")
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            print("error func none-----shutdown_server")
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
    except Exception as e:
        print(f"----shutdown error {e}---")
        #return f"Error: {e}", 500
    #
    print("111-----shutdown_server")
    sys.exit(0)
    exit()
    os._exit(0)



@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def proxy(path=None):
    global m_flag,m_server_socket,m_client_num
    
    pathkey=path
    if path is None:
        path = ''
        pathkey=path

    if path == 'clientExit':
        print("clientExit clientExit clientExit clientExit clientExit")
        jj={}
        jj["cmd"]="clientExit"
        resjson=json.dumps(jj,indent=4)
        sendToClient(resjson)
        client_status_print()
        client_status_reset()
        return "clientExit",200
        
    if path == 'cchkConnect':
        print("ccccccccccc ccccccc")
        client_status_print()
        jj={}
        jj["cmd"]="resendEcho"
        resjson=json.dumps(jj,indent=4)
        sendToClient(resjson)
        #sendDataSocket(client_socket,resjson.encode())
        
        #str = "m_c"+ str(m_client_num)+"<BR>\n"+"okokok"
        strxx ="dsaoifjasoidfssssssssss m_client_num = "+str(m_client_num)+" ---"
        print("cc cc cc ---"+strxx)
        return "sssssssssstr " + strxx,200
    
    if path == 'exit':
        print(" exit --- shutdown_server")
        logging.info("Server is shutting down...")
        shutdown_server()
        return "Server is shutting down...", 200

    """
    if pathkey in m_flag and m_flag[pathkey]["f"]==112:
        key=pathkey
        if m_flag[key]["j"]["content-type"]=="None":
          return Response(m_flag[key]["j"]["content"], status=m_flag[key]["j"]["status"],headers=m_flag[key]["j"]["headers"])#,content_type=m_flag["j"]["content-type"])
        else:
          return Response(m_flag[key]["j"]["content"], status=m_flag[key]["j"]["status"],headers=m_flag[key]["j"]["headers"],content_type=m_flag[key]["j"]["content-type"])
    """
    start_time=datetime.now()
    #elapsed_time = (datetime.now() - start_time).total_seconds()
    
    while m_flag["f"] == 100:
      if (datetime.now() - start_time).total_seconds() > 30:
          print("----------------------- time out break 1111 ----------------")
          break
      time.sleep(0.3)
    m_flag["f"] = 100
    print("k k path=",path," m_client_num =",m_client_num , flush=True)
    
    #sendToClient("senddata test 0011")
    # 寃쎈줈媛� '/'�� 寃쎌슦 泥섎━
    
    
    # "exit" 寃쎈줈瑜� 泥섎━�섎뒗 濡쒖쭅 異붽�

    url = f"{LOCAL_SERVER_URL}/{path}"

    # 濡쒓렇�� 湲곕줉�� �뺣낫��
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
                # �뚯씪 �대쫫怨� �뚯씪�� �ㅻⅨ �뺣낫瑜� 媛��몄샂
                filename = file.filename
                content_type = file.content_type
                filedata= base64.b64encode( file.stream.read() ).decode('utf-8')
                ddic.append((key, filename, content_type ,filedata))
                print(f"�뚯씪 ��: {key}, �뚯씪 �대쫫: {filename}, �뚯씪 MIME ����: {content_type}")
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
      m_flag["f"] = 111  
      return "aaaddkk no client ..... num=" + str(m_client_num) ,200
    # 濡쒓렇 湲곕줉
    logging.info(f"Request Method: {method}")
    logging.info(f"Request URL: {url}")
    logging.info(f"Request Headers: {headers}")
    logging.info(f"Request Args: {args}")
    logging.info(f"Request Data: {data}")
    """
    # 媛� HTTP 硫붿냼�쒖뿉 留욌뒗 泥�
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
    
    start_time=datetime.now()
    while m_flag[key]["f"] == 100:
      if (datetime.now() - start_time).total_seconds() > 30:
          client_status_print()
          client_status_reset()
          return "-------- time break3333 ---------"
      if m_flag["f"]==2022:
          m_flag["f"]=111
          m_flag[key]["f"]=113
          return "-------- time break2222 ---------"
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
    # �묐떟�� �먮낯 �댁슜�� 洹몃�濡� �대씪�댁뼵�몃줈 諛섑솚
    #return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

@app.errorhandler(405)
def handle_invalid_method(error):
    return Response(
        f"Invalid HTTP Method! The method {request.method} is not allowed for this route.",
        status=405,
        content_type="text/plain"
    )

if __name__ == '__main__':
    # �쒕쾭 �ㅽ뻾
    time.sleep(1)
    #socketio.run(app, host='0.0.0.0', port=m_port02, allow_unsafe_werkzeug = True)
    app.run(host='0.0.0.0', port=m_port02)