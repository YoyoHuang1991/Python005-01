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

