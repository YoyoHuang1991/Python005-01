#!/user/bin/env python
# -*- coding:utf-8 -*-
'''
#學號: G20200389060057
#姓名: 黃喻榆
#作業＆總結連結: https://github.com/YoyoHuang1991/Python005-01/tree/master/week01

功能: 
1. 編寫一個函數，當函數被調用時，將調用的時間紀錄在日誌中
2. 保存位置為: /var/log/python-當前日期/test.log
創建; 2020-11-24
'''


import logging
import os
import time

def test():
    logging.info("test()被執行。")

def main():
    os.umask(0)
    today = time.strftime("%Y%m%d", time.localtime())
    path = '/var/log/python-'+today+'/'
    try:
        os.chdir(path)
    except:
        os.mkdir(path)
        os.chdir(path)

    logging.basicConfig(filename = 'test.log',
                        level = logging.DEBUG,
                        datefmt = '%Y-%m-%d %H:%M:%S',
                        format = "%(asctime)s %(name)-8s %(levelname)-8s [line:%(lineno)d] %(message)s"
                        )
    
    logging.info("main()被執行。")
    test()
    logging.warning("程序結束。")

if __name__ == "__main__":
    main()

