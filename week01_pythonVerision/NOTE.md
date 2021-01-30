学习笔记


01 如何正確區分Python的版本：
----
1. 舊版的軟體開發多為python 2.7版本, 目前新的多以python 3.7, https://www.python.org/downloads/  下載 Windows x86-64 executable installer
2. tensorFlow2為例，官網會寫支援3.5~3.8版本，故建議不要選擇最新的版本，以免不能用。
3. 各版本有不同特性，要到Python.org看文件說明，解釋各版本的新變化。"向後不兼容的"、"新的內置特性"。
4. linux下載的是原代碼，通過make和make install把原代碼編譯成python可執行的程序。

02 在不同操作系統中安裝python
----
1. 安裝目錄不要中文、空格、特殊字符。非必要情況盡可能安裝一個python解釋器。安裝多個python版本須注意path環境設置。

03 多個python解釋器共存會有甚麼問題
----
1. 在windows系統可以用py -0指令看目前電腦安裝幾個版本的python，mac os則是輸入python 按兩下tab鍵。
2. 平時執行python程序，會輸入python3 空格 projectName venv執行，但不知道python3會執行哪個版本。
3. Python3 -V可以看目前版本。
4. 更改python指定的版本路徑，echo $PATH 可以查看安裝路徑，複製第一段路徑
5. 指令 ls 路徑/3.8/bin或/3.7/bin，可以列出路徑下的檔案內容
6. 調換位置，將3.7調換到前面，執行python3時使用3.7版本，指令export PATH=/Library…/3.7/bin:$PATH。
7. 以上設置當電腦重新開機後又會重置，需要建立環境設置文件，指令vim /etc/profile，將export PATH=/Library…/3.7/bin:$PATH 貼到文件的最後一行，再按i鍵進入insert模式，按esc進入保存模式輸入:wq進行保存。輸入:q!退出。若要求管理員權限，可以再vim錢加上sudo。
8. 指令pip可看到已安裝的pip版本，windows執行pip -V，pip安裝擴展包時，會安裝到預設的python版本中，其他版本的python並不會被安裝pip所安裝的擴展包。
9. 指令輸入ls  /Library/…/3.7，來到python3.7的安裝目錄
10. 指令ls  /Library/…/3.7/lib，底下又有一個python3.7的資料夾，指令ls  /Library/…/3.7/lib/python3.7，找到site-packages/，裡面就是所有擴展包第三方庫。Ls /Library/…/3.8/lib/python3.8/site-packages/列出3.8版本安裝的第三方庫。
11. 不同版本內site-package/都有pip，且名字相同。在安裝擴展包時，使用pip3.7指令，會安裝到python3.7的版本內，pip3.8則會安裝到python3.8版本內。

04 Python交互模式使用
----
1. 進入python3，help(str)可以看到class str相關的function，在linux要使用help('str')。
2. 若pip -V沒有發現已安裝的pip，在linux安裝pip3，sudo apt-get install python3-pip
3. 安裝ipython，指令pip3 install ipython，安裝過程若顯示warning: installed in '/home/…./.local/bin'，則需要到該目錄，ls 會顯示方才安裝第三方庫，使用指令sudo mv iptest iptest3 ipython ipython3 pygmentize /usr/local/bin，將path移到local，在terminal執行ipython指令時，才可正常運作。
4. 更改鏡像站的指令，pip install -I https:/pypi.tuna.tsinghua.edu.edu.cn/simple pip -U，更新
5. pip安裝加速，配置文件liux: ~/.pip/pip.conf，pip ~指令可以直接回到用戶根目錄。
6. 指令mkdir -p .pip建立文件夾，cd .pip進入.pip文件夾，用vim pip.conf，新增文件。貼上index-url = https:/pypi.tuna.tsinghua.edu.edu.cn/simple，再按i鍵進入insert模式，完成後按esc，再按:wq退出。

05 Python IDE的使用技巧
----
1. 在vs code官網下載linux版本的deb安裝檔案，於terminal執行sudo dpkg -i 檔案名稱.deb，開始安裝。安裝完後，指令code 即可開啟vs code程序。
2. 打開txt檔右下角顯示utf-8表示編碼格式，若不匹配，會產生亂碼。打開py檔，左下角顯示當前以哪個版本的python解釋器解釋。
3. 左邊有搜索、擴展，可安裝ranbow fart、python
4. 游標在句子內，按option+左右方向鍵，移動時是以一個單詞為距離移動。Command+上或下，可快速移動到開頭或結尾。option+上下，可以整行調整順序。在行號前增加斷點。Ctrl + /可以將選取的範圍變成註解。
5. Run>Start Debugging(F5)，偵測設定檔選python檔案。顯示單行運行、單步跳過等等選項。左側顯示目前變量，過程中可以設定變量的值。
6. 在linux環境安裝jupyter，pip3 install jupyter，執行jupyter notebook。

06 Python 項目的一般開發流程及虛擬環境配置
----
1. 搞清需求、編寫原代碼、使用Python編譯器轉換為目標代碼(.pyc結尾)、運行程序、測試、修復錯誤、再運行與測試
2. python是解釋性的語言，所以需要在生產環境安裝完全相同的解釋器，可以製作"虛擬環境"方便整個遷移，以方便保持環境一致性。
3. 引入虛擬環境 指令python3 -m venv，venv是python自帶的模塊，意思是執行python3的時候加載venv的模塊venv後面加上虛擬環境的名稱，例如: python3 -m venv myfirstvenv，虛擬環境即創建在目錄當中。Ls myfirstvenv/bin可以看到目前該環境安裝的第三方庫。切換至虛擬環境就不會有python多個版本的問題。
4. 創建好虛擬開發環境後，用指令source myfirstvenv/bin/activate，指令which python3，可以看虛擬環境的python安裝位置。執行deactivate，離開虛擬環境。
5. 創建不同版本的虛擬環境，做不同環境的程序測試。
6. 當程序設計好，要遷移到生產環境中，將.py打包壓縮傳到生產環境並在生產環境安裝相同版本的python。activate開發環境的虛擬環境，指令pip3 freeze查看虛擬環境中安裝那些第三方庫。指令pip3 freeze > requirements.txt，cat requirements.txt查看。離開deactivate，activate第二個虛擬環境，指令pip install -r ./requirements.txt，透過txt檔列出的第三方庫安裝。指令pip3 freeze，第二個虛擬環境即安裝好相同的第三方庫。

07 Python的基本數據類型
----
1. None, Bool, 數值(整數、浮點、負數), 序列(字串、列表、元組), 集合(字典), 可調用
2. 關係運算符==, !=, >, <
3. 單引、雙引、三引號都可以作為字串。例如: 輸入變數名稱x，再按tab，會列出相關的function
4. 列表['a','b','c'], append, extend
5. Z=('a','b','c')  元組與list是同繼承同一個class，有相同的function，如count()
6. python之禪，import this，核心觀念
7. 字典dict1 = {'k1': 'v1', 'k2':'v2'}，dict['k1']可調用裡面的value。

08 Python的高級數據類型
----
1. collections容器數據類型、namtuple()命名元組、deque雙端隊列、counter計數器、orderedDict有順序的字典(哈希算法)
2. 打開collection官方文檔。 https://docs.python.org/zh-tw/3.7/library/collections.html
3. 示範from collections import deque，atog = deque('def')建立deque(['d','e','f'])的隊列。

09 控制流: 數據類型對應算法
----
1. 將複雜的算法拆解，做成遞歸。
2. If 條件判斷式、while的演示、while I < len(list1)。盡量用for i in list1，方有pythonic的風格，可以用for來做迭代。

10 函數和模塊的區別
----
1. 常見模塊
	1. time、datetime、logging、random、json、pathlib、os.path
	1. 模塊包含最細微的就是函數，模塊.py組合起來就是包。
2. 自己創建模塊。Touch short.py, touch main.py，vim main.py開始編輯。
	1. Import short
	1. Vim short.py，加入def short_func(): print('life is short')，編輯完後，cat short.py，可查看文檔。
	1. If __name__ == '__main__': short_func()，當直接執行short.py時，才會運行以下程序。若作為模塊導入到其他py文件中，則不會被執行。以上寫法叫做dander，變數名稱前後有兩個底線。

11 Python標準庫: 日期時間處理
----
1. time、datetime、logging、random、json、pathlib、os.path，到python官方文檔查看詳細說明。
2. 在terminal使用ipython做練習，
	1. import time
	1. Time.time() 返回時間戳
	1. Time.localtime()，返回struct_time格式
	1. Time.strftime("%Y-%m-%d %X", time.localtime()) 將struct_time轉成字串
	1. Time.strptime( "2020-10-20 17:46:49", "%Y-%m-%d %X") ，把字串轉乘struct_time
	1. 在官方文檔的strftime可以看到%Y的各種格式說明。
	1. 時間偏移的操作，用time比較複雜，可用datetime
	1. From datetime import datetime，或是用from datetime import *
	1. Datetime.today() , datetime.now()顯示的是一樣的結果。
	1. 顯示昨天datetime.today() - timedelta(days = 1)或是datetime.today() + timedelta(days = -1)
	1. 其中days參數哪來？可以到timedelta官方文檔看。

12 Python標準庫：日誌處理
----
1. 自己輸出的話，規則跟格式會不準確，所以使用logging較方便，也不用自己去定義。先到官方文檔查看。
2. 日誌當中有級別差異，info、warning、error(必須優化，跟後端連接有問題)、critical。Logging.debug級別，可以帶入參數。
3. 在ipython中，import logging，print預設輸出沒有debug, info，只會打印warning, error, critical。
4. 日誌系統基本配置，使用logging.basicConfig查看官方文檔
	1. Filename設定文件名
	1. level，預設info級別以上才會紀錄，可以自己調整為debug級別也可以紀錄。例如：level = logging.debug
	1. datefmt使用指定的日期與時間格式，格式與time.strftime相同
	1. format指定存入log檔案的格式，在官方文檔中搜尋format看有哪些屬性可以設定，asctime, lineno, levelname, message是常用的屬性
	1. 在terminal中，先確認帳戶有存取權限。Import logging
		i. 設置logging.basicConfig(filename='test.log')
		ii. 再寫方才打的
		    ...: logging.debug("debug message")
		    ...: logging.info("info message")
		    ...: logging.warning("warning message")
		    ...: logging.error("error message")
		    ...: logging.critical("critical message")
	1. 離開ipython, cat test.log查看方才建立的log文件檔，即可看到方才的message。
	1. 再打開ipython，依然指定filename='test.log'，並不會覆寫，而是追加寫入。 
	1. Logging.basicConfig(filename='test.log', level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S', format = '%(asctime)s %(name)-8s ％(levelname)-8s [line: %(lineno)d] %(message)s')，其中%(asctime)s後變得s是輸出類型為string的意思。

13 Python標準庫：路徑處理
----
1. 進到ipython，from random import *, 或是import random，則需要輸入random.random()來使用，該功能會隨機輸出0.0~1.0之間的浮點數。
	1. 用randrange(0,101,2)則從0~100、步長為2，隨機選號。Choice(['red', 'blue', 'orange'])則是從中隨機選一個。
	1. 隨機抽取多個元素sample([1,2,3,4,5], k=4)從中隨機抽許四個元素。
2. 保存簡單配置的文件，通常以ini, json, xml格式。python則多用json較輕量
	1. Import json，json.loads('[ "foo", {"bar": ["baz", null, 1.0, 2]}]')，會將json文檔中的字串做解碼。
	1. 做編碼則是json.dumps("[ "foo", {"bar": ["baz", null, 1.0, 2]}]")
3. 編程中需對檔案路徑做處理，使用os.path，pathlib
	1. 在ipython執行from pathlib import Path
	1. p = Path()
	1. p.resolv() 顯示當前的完整路徑，若想定義其他的路徑用path = '/usr/local/a.txt.py'，再用p = Path(path)加入到Path當中。
	1. 輸入p.再按tab可以看到該類別的相關功能，p.name可以顯示檔名，去掉path前變得路徑；p.stem 可以看到檔名，但去掉檔名後綴；只想要後綴副檔名，則用p.suffix。
	1. 用p.suffixes可以list格式輸出剛檔的多重複檔名，因為在linux系統中常見多重副檔名，如.tar.gz或.tar.bz2。
	1. 用p.parent，可以看到路徑名稱，不包含檔名。用p.parents則出現“可迭代”的對象，用for in in p.parents: print(i)取用，可做多級路徑的處理。
	1. 用p.parts，將路徑以元組形式輸出，路徑分段顯示。
4. 較舊的方式會用os數據庫，import os
	1. 獲得test.log完整路徑，用os.path.adspath('test.log')
	1.  用path = 'usr/local/a.txt'，os.path.basename(path)獲得文件名，os.path.dirname(path)顯示路徑名
	1. 判斷文件是否存在，或是是文件還是目錄，用os.path.exists('/etc/passwd')
	1. 通常在處理文件前，會先確認該文件是否存在，才不會覆蓋掉重要的文件。若不存在，再進行創建。
	1. 用os.path.isfile('/etc/passwd')或os.path.isdir('/etc/passwd')判斷目標是一個文件或是目錄。
	1. 希望把兩個路徑連接在一起，os.path.join('a','b'), os.path.join('/a', 'b') 

14 Python標準庫：手動實現守護進程daemon
----
1. 通常應用在服務器端，linux開機時，直接運行程序，沒有登入，所以拿不到用戶的session等訊息。daemon進程可以確保終端關掉時，程序可繼續運行。在windows中稱為服務，開機時自動運行起來；在linux中叫做daemon進程。脫離終端(terminal)後，仍繼續運行。
2. 先參考業界標準，到python官方文檔python developer's guide >>PEP index, standard daemom process library。PEP 3143
3. python的daemon進程是參考unix network設計，UNP和APUE都是同一個作者。 若英文難懂，可以搜尋“APUE第13章守護進程daemon”
4. 調用fork, 使父進程exit。從stackoverflow或github查相關資料。複製別人的程序，在自己的VS code做修改、操作。
5. #!/usr/bin/env/ python聲明此程序是什麼解釋環境，bash就會認出是此為python腳本
	1. 引入三個庫sys, os, time，sys是用來做標準的輸出和錯誤輸出。os創建子進程，time 顯示當前的日期。
	1. 從結構看，此腳本包含兩個函式，daemonzie與test，test只是顯示每秒時間戳，而daemonize會被作為模塊，可以放到其他程序中。
	1. daemonzie包含三個參數，在linux中分別為0, 1, 2，皆墨認為'/dev/null' 皆指向空。
		1. Stdin標準輸入
		1. stdout標準輸出
		1. Stderr錯誤輸出
	1. 此處調用時，只改stdout，由於daemon要脫離終端，把標準輸出改成文件，跟一般在終端用print輸出不一樣。一般工作不會寫死路徑，都會指向dev/null。
	1. Daemonzie()內的架構：
		1. 首先創建子進程，把父進程關掉，用pid = os.fork()
			1. try與except，一旦創建進程失敗，就會拋出OSError。
			1. 創建進程有最大數量的限制
			1. 一旦錯誤，就樣退出，sys.exit(1)
			1. 當pid > 0，可認定為父進程，sys.exit(0)將父進程退出。父進程先於子進程exit提出，會讓子進程變成一個孤兒進程，即可倍init這個用戶級別的守護進程收養。init就是一號進程。
			1. 正常退出exit()帶0值進去，若為異常退出，則帶入非零的值，例如exit(1)。
		1. 設置
			1. 變更目錄位置 os.chdir('/')，要確認進程不佔用任何目錄，否則不能umount。例如：程序是在移動硬碟上，若沒有變跟目錄位置到根目錄，要卸載硬碟時，會顯示busy狀態，沒辦法卸載硬碟。根目錄只有在關機時才會卸載。
			2. 用os.umask(0)指定0，讓他擁有任何文件的寫入權限。
			3. 用os.setsid()，進程成為新的會話組和組長。
		1. 第二次創建子進程fork
			1. 基本上與第一次一樣，為防止第一次fork有異常退出，所以再做一次fork
			2. 經過第二次fork已經進入真正的daemon進程
		1. 調整文字描述符、複製描述符
			1. 重新定向標準描述符
	1. Test()測試daemonize()是否有在運行
		1. 比print更底層的輸出方式 sys.stdout.write，用os.getpid()獲得當前的進程的pid
		1. 用time.locationtime()或teim.ctime()裝當前的時間，實際開發中都統一用一種方式。
		1. 清空緩存sys.stdout.flush()，讓標準輸出可以立即打印到日誌上。
		1. 讓程序暫停一秒，time.sleep(1)
6. 在終端terminal中運行daemon.py
	1. 指令ps -ef | grep deamon查看是否仍在運行。
	1. 指令tail -f d1.log 以自動更新的方式查看日誌。
	1. 關閉掉當前terminal後，再新開terminal仍可查看到該daemon持續運行。


15 Python標準庫：正則表達式實戰
----
1. 到python官方文檔，查看re的說明，建議全部通讀。
2. 主要用來提取字串和修改字串
	1. 實務上如用戶提交訊息時，如密碼，可對訊息做驗證。
	1. 實務上給定文本，作文本的處理
	1. 實務上爬蟲時，可以將抓下來的文本處理得更規範，便需要用正則作多次的替換。
3. 常用元字符：
	1. 點.
	1. 星號.* 零次～任意次
	1. at字符＠，遇到郵箱的時候
	1. ＾匹配開頭
	1. .com＄ 匹配結尾
	1. ＋ 一次～任意次
4. 模塊內容：
	1. Complie有兩種方法：
		1. Prog = re.complie(pattern)
		    result = prog.match(string)
		1. Result = re.match(pattern, string) 單一使用時。
		1. 若會不斷重複使用，建議用re.complie()保存這個正則對象以便使用
	1. re帶有許多常量，需要去背誦。函數如re.split, re.findal, re.search, re.match, re.sub 是經常用到的。使用物件導向或re.功能是一樣的。但當重複使用的時候，可以用物件導向。
5. 打開ipython, import re
	1. 定義content = "123123123"
	1. re.match(".{11}", content)，點{11}字串長度11。
	1. re.match(".{11}", content).group() 匹配成功後輸出成字串，可以存到變數中。
	1. re.match(".{11}", content).span() 輸出位置index起始
	1. re.match("@", "123@123.com")會匹配不成功，因為預設是要完全一致，才會成功。改為re.match(".*@.", "123@123.com")，後面再加.group()可以把值組起來。
	1. re.match("(.*)@(.*)", "abc@123.com").group()將值分組，group(1)可以取第一組 "abc"
	1. 提取字符串裡面的內容會使用group()，正則三大目的，匹配、替換、提取字串。
6. 使用re.search()函數
	1. 返回字串中第一個查找到的值，re.search("@", "123@123.com")，返回match對應的符號。
7. 使用re.findall()函數
	1. 返回所有符合條件的字符串，結果為list
8. 使用re.sub()函數替換
	1. re.sub("123","456","123@123.com") 輸出'456@456.com'
	1. re.sub("\d", "xyz", "123@123.com") 輸出'xyzxyzxyz@xyzxyzxyz.com'
	1. re.sub("\d+", "xyz", "123@123.com") 輸出“xyz@xyz.com”
9. 使用re.split()函數將字串分割
	1. re.split("@", "123@123.com") 輸出 ['123', '123.com']
	1. 若分割之後，分割符號也想保留，可以用re.split("(@)", "123@123.com") 輸出 「'123', '@', '123.com']
