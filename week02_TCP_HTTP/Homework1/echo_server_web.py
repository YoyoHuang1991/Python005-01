#!/usr/bin/env python
# -*-coding:utf-8 -*-
import socket
import struct
import json
import os

def client_get(conn, share_dir, filename):
    # 3、以讀的方式開啟檔案,讀取檔案內容傳送給客戶端
    # 第一步：製作固定長度的報頭
    header_dic = {
        'filename': filename, # 1.txt
        'file_size':os.path.getsize(r'%s/%s'%(share_dir, filename)) # 路徑/1.txt
        }    
    header_json = json.dumps(header_dic) #將header_dic存成json檔案
    header_bytes = header_json.encode('utf-8') #將header轉成二進制資料方能傳輸

    # 第二步：先發送報頭的長度
    conn.send(struct.pack('i',len(header_bytes)))  #‘i’傳入的數據類型，需與後面的value一致， struct.pack(fmt, value)將header_bytes的長度傳輸給客戶端

    # 第三步:再發報頭
    conn.send(header_bytes)
    # 第四步：再發送真實的資料
    with open('%s/%s'%(share_dir, filename),'rb') as f:
        for line in f:
            conn.send(line)

def client_upload(conn, save_dir):
    #2、以寫的方式開啟一個新檔案，接收服務端發來的檔案的內容寫入客戶的新檔案

    # 第一步：先收報頭的長度，來自服務端第一個send的conn.send(struct.pack('i',len(header_bytes)))
    print('conn等待傳回的資料。')
    obj = conn.recv(4)
    print(obj)
    print('gd_client.recv已收到傳回的資料。')
    header_size = struct.unpack('i',obj)[0] #header的長度，若沒有限制header的長度，後續接收會潮過該收的資料

    # 第二步：再收報頭，來自服務端第二個send的conn.send(header_bytes)，長度限定在header_size內，以免抓超過header之外的訊息
    header_bytes = conn.recv(header_size)

    # 第三步：從報頭中解析出對真實資料的描述資訊
    header_json = header_bytes.decode('utf-8') #將二進位制的資料轉乘str的type

    header_dic = json.loads(header_json)  #將str轉成dict的type
    '''
    header_dic = {
        'filename': filename, # 1.txt
        'file_size': os.path.getsize(r'%s/%s' % (share_dir, filename)) # 路徑/1.txt
        } 
    '''
    total_size = header_dic['file_size']
    file_name = 'from_client' + header_dic['filename']
    # 第四步：接收真實的資料
    check_dir(save_dir) #先確認本地的dir是否存在，不存在則建立該dir
    with open(r'%s/%s'%(save_dir, file_name),'wb') as f:
        recv_size = 0
        while recv_size < total_size:  #當接收的資料已經達到該檔案的size表示接受完成，結束接收
            line = conn.recv(1024) #每字只接收1024字節
            f.write(line)
            recv_size += len(line)
            print('總大小：%s  已下載大小：%s' % (total_size, recv_size))

def check_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)

share_dir = os.path.join(os.getcwd(), 'files_in_server')
gd_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gd_server.bind(('localhost', 10000)) # 0-65535: 0-1024給作業系統使用
gd_server.listen(5)

while True:
    print('等待accept()...')
    conn, client_addr = gd_server.accept()
    while True: # 通訊迴圈
        try:
            # 1、收命令
            print('等待接收...')
            res = conn.recv(8096) # b'get 1.txt'，等到接收8096個字節後，或client停止發送後，才會進入下個步驟。
            if not res: 
                break # 適用於linux作業系統

            # 2、解析命令，提取相應命令引數
            cmds = res.decode('utf-8').split() # ['get','1.txt']
            filename = cmds[1] #在client端已經確認cmds為長度為2的list
            
            if cmds[0] == 'get':  #傳送檔案給客戶端
                if not os.path.isfile(os.path.join(share_dir, filename)):
                    conn.send('無該檔案'.encode('utf-8'))
                    continue
                else:
                    conn.send('有該檔案'.encode('utf-8'))
                client_get(conn, share_dir, filename)
            elif cmds[0] == 'upload': #接收來自客戶端的檔案
                conn.send('yes'.encode('utf-8'))  #回覆client端暫停的recv()    
                client_upload(conn, share_dir) 

        except ConnectionResetError: # 適用於windows作業系統
            break
    conn.close()
gd_server.close()