#!/usr/bin/env python
# -*-coding:utf-8 -*-
import socket, struct, json
import os

def client_download(gd_client, download_dir):
    #2、以寫的方式開啟一個新檔案，接收服務端發來的檔案的內容寫入客戶的新檔案

    # 第一步：先收報頭的長度，來自服務端第一個send的conn.send(struct.pack('i',len(header_bytes)))
    print('gd_client.recv等待傳回的資料。')
    obj = gd_client.recv(4)
    print('gd_client.recv已收到傳回的資料。')
    header_size = struct.unpack('i',obj)[0] #檔案大小

    # 第二步：再收報頭，來自服務端第二個send的conn.send(header_bytes)，長度限定在header_size內，以免抓超過header之外的訊息
    header_bytes = gd_client.recv(header_size)

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
    file_name = header_dic['filename']
    # 第四步：接收真實的資料
    check_dir(download_dir) #先確認本地的dir是否存在，不存在則建立該dir
    with open(r'%s/%s'%(download_dir, file_name),'wb') as f:
        recv_size = 0
        while recv_size < total_size:  #當接收的資料已經達到該檔案的size表示接受完成，結束接收
            line = gd_client.recv(1024) #每字只接收1024字節
            f.write(line)
            recv_size += len(line)
            print('總大小：%s  已下載大小：%s' % (total_size, recv_size))

def check_dir(download_dir):
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)


def client_upload(conn, upload_dir, filename):
    header_dic = {
        'filename': filename, # 1.txt
        'file_size':os.path.getsize(r'%s/%s'%(upload_dir, filename)) # 路徑/1.txt
        }    
    header_json = json.dumps(header_dic) #將header_dic存成json檔案
    header_bytes = header_json.encode('utf-8') #將header轉成二進制資料方能傳輸

    # 第二步：先發送報頭的長度
    print(struct.pack('i',len(header_bytes)))
    conn.send(struct.pack('i',len(header_bytes)))  #‘i’傳入的數據類型，需與後面的value一致， struct.pack(fmt, value)將header_bytes的長度傳輸給客戶端

    # 第三步:再發報頭
    conn.send(header_bytes)
    # 第四步：再發送真實的資料
    with open('%s/%s'%(upload_dir, filename),'rb') as f:
        for line in f:
            conn.send(line)
    #總共傳送三次，header長度、header內容、檔案內容

download_dir = os.path.join(os.getcwd(), 'client_downloaded')
upload_dir = os.path.join(os.getcwd(), 'client_to_upload')
gd_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
gd_client.connect(('127.0.0.1',10000))

while True:
    #1、發命令
    cmd = input("請輸入[get或upload filename]，ex: get test.txt\n>>: ")
    #get a.txt
    if not cmd:
        continue
    else:
        if cmd.startswith('exit'):
            gd_client.close()
            break

        if len(cmd.split()) != 2:
            print('輸入錯誤。')
            continue

        if cmd.split()[0] == 'get': #接收來自服務端的檔案
            gd_client.send(cmd.encode('utf-8'))
            isfile = gd_client.recv(12)
            if isfile.decode('utf-8') == '無該檔案':
                print('Server沒有該檔案')
                continue
            client_download(gd_client, download_dir)
        elif cmd.split()[0] == 'upload':
            filedir = os.path.join(upload_dir, cmd.split()[1])
            if not os.path.isfile(filedir):
                print('該檔案不存在')
                continue
            gd_client.send(cmd.encode('utf-8'))
            gd_client.recv(4) #等待server端ready，以免後續資料全部upload，導致server端接受太多資料，而無法抓到header的資訊
            client_upload(gd_client, upload_dir, cmd.split()[1])
        else:
            print('指令錯誤。')
            continue

