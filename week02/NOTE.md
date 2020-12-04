学习笔记
01 
* OSI參考模型與TCP/IP模型
* OSI參考模型(理論上規定，須符合的規定):
	* 物理層
	* 數據鏈路層
	* 網絡層
	* 傳輸層
	* 會畫層
	* 表示層
	* 應用層
	3. TCP/IP模型(才是真的完成我們功能的模型，編程要參考的):
		a. 網絡接口層
		b. 網絡層
		c. 傳輸層
		d. 應用層
	4. 每一層面只關注他需要解決的問題，若無分層思維，則會胡亂去找。
	5. Socket編程，如何實現 網絡與傳輸層?
		a. 客戶端的應用程序>經過TCP或UDP，一般HTTP默認TCP，封裝成IP。經IP通道，Socket服務端經過socket解開。
		b. 知道自己是哪個協議，ex: HTTP使用TCP
		c. TCP協議要對應的端口。TCP就像分機號碼，透過socket的綁定，可以連到固定的應用程序。
	6. 程序模型變成Socket API，TCP Client與TCP Server。
		a. Socket()
		b. Bind()
		c. Listen()
		d. Accept()
		e. Recv()
		f. Send()
		g. Close()
		h. 實戰: 不使用開源框架的前提下完成一個echo服務端和echo客戶端。
02 寫一個Socket客戶端
	1. 用VS code打開mod2_client1.py，requests函式庫已經將底層進行封裝，此處編成時，僅看到應用層的部分，輸入網址即可。
	2. 若要用socket底層的部分來實現requests應用的功能也可以，但就要考慮Socket, connect, write, read, close
		a. send將訊息寫到網卡上面
		b. recv將訊息從網卡上讀出來
	3. 打開mod2_client2.py，即是將requests.get()攤開來，socket所做的事情。
		a. Socket.socket(socket.AF_INET, socket.SOCK_STREAM)中，AF_INET是使用IPv4地址，SOCK_STREAM是指TCP協定去連接。
		b. VS code快捷鍵，游標框選要運行的區域，按shift+enter。Print(f"s1:{s}")
			i. 結果解釋: fd=3代表使用的是三號描述符。0號文件描述符是標準輸入，1號是標準輸出，2號是錯誤輸出。若程序先加載其他文件，現在會看到4，號碼是依序向後的。
		c. 下一行s.connect(('www.httpbin.org', 80))指連接的服務端網址，建立TCP層面的連接。
			i. 再次打印s，會看到客戶端的ip與端口ladder，和服務端的ip、端口。
			ii. 其中域名被解析成ip的過程被隱藏。
		d. 繼續填充Socket，建立連接、發送數據，之前使用requests時，會默認將http頭發給服務器。
			i. 若使用socket，TCP的層面，則得發這些訊息。
			s.send(b'GET / HTTP/1.1\r\nHOST:time.geekbang.org\r\nConnection: close\n\r\n')
			ii. 發出後得接收返回的訊息，因不知道s.recv(1024)會有多少訊息，故使用while True的死循環。其中1024是每次接收多少字符，並將內容存到buffer數組。用s.close()將文件關閉。
		e. 拿到數據後，用b''二進位的空字串將buffer數組串接成string，存在response變數中。
			i. 用split('\r\n\r\n', 1)做分離為header與html。
			ii. 因為前面用b''二進制，所以要用decode('utf-8')轉換。若為windows系統，得用GBK才不會是亂碼。
			iii. 由於html內容較長，這邊是寫入到index.html的方法，不在terminal打印出來。
		f. 應用層requests的好處是對底層進行封裝，編程較簡單；相對地為強調效率，有些協議在TCP解決，沒有上升到應用層，例如:直接用TCP協議發送binary等等這些數據，達到高效的通信。
	4. Mac os 寫入文件時，若發生權限不足的狀況，可以sudo chown -R 使用者名稱 文件夾路徑，開啟寫入權限。
03 Echo Server實戰
	1. 最早出現的服務器是Echo，向服務端發送字符，原樣地發回客戶端，主要用來證明TCP的連接是通，作為健康檢查的機制。
	2. VS code快捷鍵，按住ctrl+左鍵，點擊要查找的class名稱，可以看該class是怎麼實現的。
	3. 如何實現echo_client? 跟上一節一樣，先建立s 套接字，在作s.connect()。
	4. While True當中，先要求用戶輸入訊息，用s.sendall()送到服務端，其中訊息要用encode()編譯成binary，服務端才能接收。If not data，當接收服務端訊息發生堵塞，則用break關閉掉s；若有數據近來，則將他打印出來，打印前一樣要將接收到binary訊息decode解碼。
	5. 服務端該如何做? 接收請求、發送訊息。
		a. 服務端跟客戶端第一個用的函數不一樣，是s.bind((HOST, PORT))，綁訂到主機和端口上。為何要綁定?因為listen()表示要接收多少連接，指定使用哪個端口；進入listen狀態，其他程序就不能再占用這個端口。
		b. 用s.accept()接收客戶端的連接
04 Web開發必備前端基礎
	1. 客戶端最上層的，即是我們使用的瀏覽器。
	2. 爬蟲第一步，用相應的庫將客戶端替換掉，使python程式能解析HTTP協議。
	3. 能解析甚麼? 在網頁上檢視原代碼，如何看專有的名詞?
		a. Link ref
		b. W3C標準，只要知道web主要部分，結構(html)、表現(css)、行為(js)。
		c. Jquery.js可以使用Ajax的異部數據同步的基礎，可通過xml發送請求，展現網頁時藉javascript更新我們的DOM數據。展現網頁的過程中，異步地更新數據近來。
		d. 可關注jQuery的dollar.ajax的方法，目前異步更新數據重要的手段。

05 HTTP協議和瀏覽器的關係
	1. 爬蟲是用python程序模擬客戶端瀏覽器接收HTTP訊息的行為以及發起請求。
	2. 打開網頁>檢查>network>header，檢視HTTP頭部Headers的訊息。
		a. headers裡存放使用者登入、發出的指令等訊息，控制的東西也寫到Headers。
		b. General裡，request URL即是請求的網頁，在此做頁面的跳轉。
			i. HTTP狀態碼Status code，1xx信息響應、2xx成功響應、3xx重定向、4xx客戶端響應、5xx服務端響應
			ii. 常見403,404…就是客戶端請求的網頁不存在，得檢查封裝好的爬蟲裡請求的地址是不是有錯誤。
			iii. 請求方式request method，點擊連結、翻頁時，都是用GET的方式"請求內容"。
			iv. POST的方式，用在用戶名的登入"發送內容"。
		c. Request header其中的cookie是需要留意的，當有cookie時，代表使用者帶著用戶名稱與密碼向服務端發起請求。如果已經登入成功，cookie就包含登入的驗證訊息。爬蟲時，該如何帶著驗證訊息、保持登入，以便持續爬蟲呢? 即用此加密過後的訊息進行提交。
			i. User-Agent:告訴服務端目前客戶端的瀏覽器形式，亦有反爬蟲的作用。一般爬蟲模擬正常用戶，一方面是cookie中驗證訊息，第二部分即是user-agent做模擬。
06 requests庫入門實戰
	1. 提出需求，獲取豆瓣電影的內容，寫入文件。
	2. 打開mod2_requests.py，關鍵在requests.get(myurl, headers = header)，爬回的資料存入response
		a. 其中response.text可以打印網頁內容，response.status_code可以返回狀態碼。
		b. 結果返回200表示連結服務端正常。
	3. Python預習標準庫時，有urllib，from urllib import request，要用兩行resp = request.urlopen("http://httpbin,org/get") 與 resp.read().decode()，遠沒有requests這種第三方庫方便。
	4. 其中request.get中的header參數就是模擬瀏覽器的headers，若沒有用header，則會出現418碼返回錯誤。
	5. 爬蟲的關鍵在於，盡可能讓python程式盡可能向正常使用者，用header與cookies
07 異常捕獲處理
	1. 保存文檔兩種方法
		a. Open，需要用close()關閉
		b. With open上下文管理器，會自動關閉，以免達到文件開啟數量的上限，造成開啟失敗。
	2. 異常捕獲: 錯誤和異常不同
		a. 語法錯誤
		b. 需求理解錯誤
		c. 寫入失敗
	3. 異常也是一個類Traceback
		a. 異常類把錯誤消息打包成一個對象
		b. 然後該對向會自動查找到調用棧
		c. 直到運行系統找到明確聲明如何處理這些類異常的位置
	4. 所有異常繼承自BaseException
	5. Traceback顯示了出錯的位置，顯示的順序和異常信息對象傳播的方向是相反的
	6. traceback的顯示方式與我們直覺由上到下看是相反的，在最下面才是產生異常的真正原因。
	7. 常見異常有六種:
		a. lookupError的indexerror和
	8. 打開範例 exception_demo, p1_dive0.py, p2_try.py, p3_chain.py
	9. 用except Exception as e: 其中Exception指捕獲所有異常。程序執行中捕獲到任一個異常，後續就不會再捕到。
	10. 自己定義異常class，雖然所有exception都是繼承自BaseException，但我們定義exception時，都要從"Exception"繼承。
		a. 類中, def __init__(self, ErrorInfo)其中ErroInfo參數可以當作固定格式來記憶。
		b. 父類super().__init__(self, ErroInfo)也要記錄
		c. 定義def __str__(self)使class可以print輸出。
		d. 最後finally，無論結果如何，都會執行的部分。用del userinput刪除占用的內存。
	11. 最常發生的異常為打開文件，該如何美化?
		a. 使用pretty_errors函式庫，pip install pretty_errors
		b. 使用With打開文件，會自動關閉文件。用open()需要用try, finally將文件close。
		c. 打開code p7_custom_with.py，自己實現with 的功能。
			i. 其中def __call__(self)將class偉裝成一個函數來使用。
		d. 像__str__這種前後有雙下畫線的函數，統稱為魔術方法。
08 重構：增加程序的健壯性
	1. 讓requests功能的網頁可以爬蟲、抓error、下載到本地。
	2. Requests.get()容易沒回應或出錯, 做try and exception
	3. Response.text存到本地文件，
		a. 首先打開mod2_requests_v2.py, from pathlib import *以及import sys 
		b. 編成美化符合PEP-8，的規範，或是google python風格指引，當然各公司也會有自己的風格規範。
		c. 增加異常捕獲，requests.exceptions.ConnectTimeout，當連線時間過長時，raise 異常。可以看requests官方文檔，瞭解它判斷連線超時的條件。
		d. 測試時可設定連線時間，requests.get(‘’, timeout=0.001)，只要時間超過，及返回錯誤。
		e. 當捕獲系統內置的異常，requests的異常是自己定義的，所以即使異常，程序還是會持續向下運作，所以要做sys.exit(1)退出。建議可以做重複三次的練線嘗試。其中返回參數1，是一個非正常狀態退出。可以自己定義，例如：100是什麼異常，200是什麼異常，方便開發者捕獲異常。
	4. 寫入到文件常有哪些操作？
		a. 在文件同級的目錄中，新建一個folder，再存進去。
		b. 利用Path(__file__)取得當前腳本文件的路徑，該值type為一個string。
		c. 使用p.resolve()確保得到一個絕對路徑，p.resolve().parent則是當前目錄的父目錄，並存到變數pyfile_path。
		d. 連接路徑，使用path的內置方法.joinpath('html')建立玉存放文件的目錄。接下來建立判斷，如果沒有該目錄則新建，若無即可直接存放。
		e. 判斷if not html_path.is_dir(): Path.mkdir(html_path)，Path內置的功能mkdir()。有目錄後，再建立存放文件的路徑page，這時候文件還沒有建立。
		f. 用with open，w寫入,encoding='uft-8'，f.write(response.text)
		g. 當文件無法打開FileNotFoundError, 常有使用者權限不夠，而無法打開所造成的錯誤。
09深入了解HTTP協議
	1. 使用ipython，import requests，r = requests.get('http://www.httpbin.org/')
	2. 查詢目前url，可以用r.url
	3. 透過requests傳遞參數，定義payload = {'key1': 'value1', 'key2': ['value2', 'value3']}，把參數帶入requests.get('http://www.httpbin.org', params=payload)，再用r.url可看到參數被帶到url內，http://www.httpbin.org/?key1=value1&key2=value2&key2=value3'
	4. 若本地登入時，用get把帳號、密碼帶入，會變成明碼，有安全性的問題；參數過多造成url過長，也會有問題。
	5. 用瀏覽器“檢查”>network ，查看請求的頭部與響應的頭部，response headers, request headers。
	6. 查看request header，服務端是怎麼判定使用者不是用瀏覽器訪問，而是用request? 
		a. cookie，當訪問服務端時，服務端會丟一個cookie給瀏覽器。若登入使用者，也會返回一個cookie，寫入到客戶端的瀏覽器。
		b. 拿requests模擬使用者，就是帶著cookie進行訪問。
		c. HOST存放主機名，用在服務器端如果是集群化，透過host可以訪問到具體的某一個主機上邊。若host只有ip地址，會被網站發現而被攔截，或請求異常。當寫大型一點的爬蟲，獲釋自動化測試的時候，會把持url的主機名和host一致。
		d. refer是指“從哪個網頁轉過來的”，例如：https://cn.bing.com/只從bing連結到該網頁的。常在反爬蟲中使用。  
		e. User-agent，若不知道該用哪個user設定，可以直接複製自己的電腦瀏覽器的設定。
	
10深入了解POST方式和cookie
	1. 直接把url貼到瀏覽器請求內容的方式稱為get，按F12快速打開檢查，network中看status_code為405錯誤。
	2. 使用post時，帶入的data參數是一個dict()的type。只用requests的內置功能.json()，可以把數據以json化的方式打印在terminal上。
	3. 專門用作http協議學習的網站http://www.httpbin.org/
	4. 希望訊息以post輸入的時候，不要有明碼。在瀏覽器中輸入http://httpbin.org/cookies/set/sessioncookie/123456789，其中sessioncookie模擬為用戶帳號，後面的數字模擬為用戶密碼，模擬用post的方式交給服務器。
	5. network中顯示status_code: 302是服務端讓客戶端進行頁面的跳轉。跳轉到cookies頁面，可看到有加密過的密碼、session保存cookie的有效期，但此處是以明碼的方式做儲存。
	6. 若通過requests請求，以seesion()方式儲存cookie，事實上requests總是默認使用seesion()方式。
	7. 也可以用with requests.Session() as s:的方式請求頁面信息，此上下文管理器，可以讓程序寫作風格更加python化。
	8. 打開p4_cookie_requests.py，模擬使用者登入，先打開douban.com並用檢查>network用測試用帳號來查看登入後的狀況。點擊登入後，可發現basic才是實際登入時跳轉的頁面，查看headers可以研究哪些是使用requests方式需要實現的。 
		a. 第一個：request URL請求的連結是什麼，需要知道信息被post到哪一個網頁中。
		b. 第二個：請求方式一定是POST
		c. Scrapy如何封裝這些信息？會用start_url
		d. User-agent, host, referer有的在瀏覽器上設置很長的一串地址，登入成功後要彖轉回原來的頁面，有的是通過瀏覽器的地址寫很長的地址來跳轉。
		e. 登入成功後寫入很長的信息到cookie。
	9. python程序中，from fake_useragent import UserAgent，設置ua = UserAgent(verify_ssl=False)使用 ua.random, 讓每次user-agent都不同。referer從瀏覽器中複製出來。
	10. 希望整個程序當中都使用同一個Session實例發出請求，s = requests.Session()，才能進行cookie的保存。看源代碼可發現Session()是使用urllib3函式庫的connect pooling功能，當發起連接時，會選用空閑的連接進行發起。可向多個主機發起請求，底層的TCP會被重用，以提升性能。可以看requests源代碼，了解他如何實現。
	11. 現在發起請求仍會有405錯誤，因尚未設定user-agent，回到瀏覽器，user-agent下面Form Data中可看到除提交用戶名字和密碼，還有ck:與remember, ticket，在requests中要提交完整，form_data要完全相同。將參數login_url, data, headers帶入s.post()中，並幫結果存到response變數中。
	12. 登入成功後，可以再對新的url2進行訪問，這裏因為已經登入成功，可以帶者經驗證的用戶名密碼的cookies用s.get()訪問，一定要帶著headers訪問。
	13. 也可以用新的session進行請求，response3 = newsession.get(url3, headers, cookies = s.cookies)
	14. 將內容寫入文件中，with open('profile.html' 'w+') as f: 其中w+為追加寫入的方式。
11使用XPath匹配網頁內容＆實現翻頁功能
	1.  翻頁事實上是點擊一個連結，以get的方式請求內容，每一頁增加25的規律。Start=0即是第一頁，start=25等於第二頁。當沒有後一頁時，須以邏輯判斷處理。
	2. 打開mod2_pageturn.py，功能的實現，import requests, 以及lxml中的XPath做網頁內容匹配。多頁迭代容易出現反爬蟲的功能，用from time import sleep每翻一頁休息5秒，避免請求過快。
	3. 用urls儲存所有頁面的url，由於後續不會再變動，所以tuple的方式儲存多個字符串。Tuple(元組)
	4. 用for in ，將tuple拆包。用get_url_name()對每一個page做操作，這樣成序看起來比叫優雅。
	5. 看get_url_name(myurl)，
		a. 將每頁內容存入變數response
		b. 使用XPath提取HTML中的特殊內容，提取前需要先封裝成特殊的對象，用lxml的etree.HTML()將頁面進行解析，存到變數selector。
		c. 對網頁的專門搜索工具selector.xpath()，其中搜索的語法，須用正則表達式來搜索。在瀏覽器的檢查頁面，找到該html內容，例如某個title，右鍵copy Xpath，即可看到正則表達式搜尋該物件所需的語法，crtl+F在搜尋欄貼上，即可找到該html物件，但這樣的語法是很複雜的。
		d. 在檢查html的搜尋欄打'/div'，會查找到該頁面所有div標籤，兩個斜槓//div找到第一個div。//div[@class='hd']，限定class為hd的div，搜索蘭右邊會發現，凡事class為hd都會被找到。
		e. //div[@class='hd']/a/span[1]表示class為hd的div底下的a標籤底下的span籤中的第一個。(此處index是從1開始，而不是0)，剛好可以抓到25個。
		f. 回到python語言file_name = selector.xpath('//div[@class='hd']/a/span[1]/text()')，用text()只取其中的text。
		g. 取鏈結地址，//div[@class='hd']/a/@href，取出所有鏈接。
		h. 電影名稱取出來多個元素以列表方式儲存，需要進一步用zip()將兩個列表連接，並轉換成dict()存到film_info。

12使用自頂向下的設計思維拆分項目代碼
	1. 從整體分析一個比較複雜的大問題。分析方法可以重用。拆分到你能解決的範疇。
	2. 爬蟲可模擬scrapy框架，專門做分布式爬蟲的框架。如果用requests自己實現分布式的爬蟲，也看參考較成熟的框架怎麼實現的。搜索"scrapy架構圖"，如何從requests進化成scrapy。
	3. requests可是做一個簡單的瀏覽器，抓取後下載到本地的過程也可以做拆解。從理論出發，得從設計模式考慮；或是學習現成的框架如何實現拆分。scrapy分為八個步驟：
		a. 最核心的部分是引擎，做各總業務的調度。即是多線程或協程。為何要做多線程？當頁數過多時，若使用for循環，時間會非常漫長。引擎解決請求的效率問題。
		b. 問題已拆分出如何實現多線程？解析成自己能解決的問題。
		c. 將headers提前出來做，拆分為SPIDERS
		d. 誰先發起？較科學的順序，即來到“調度器”，做併發的控制。發起時同時進行多少連接
		e. “下載器”如同requests真正發起請求的。
		f. “管道”每個網頁進行保存，儲存檔案的部分，如果是文字、圖片，則要用到open()，若要存到數據庫，則要與數據庫連接。
		g. 拆分到可重複的程度。拆分到自己可以解決的實例。
13模擬Scrapy拆分爬除框架 (sample file: mod2_miniScrapy.py)
	1. 使用函式庫
		a. /import requests
		b. /from lxml import etree
		c. /from queue import Queue 隊列，現實中進行排隊
		d. /import threading 多線程，模擬多個請求，併發向服務器發起請求
		e. /import json
	2. 框架圖當中，拆成五個組件
		a. ENGINE
		b. SCHEDULER調度器
		c. SPIDER
		d. DOWNLOADER下載器
		e. ITEM PIPLINES
	3.  定義存放網頁的任務隊列：
		a. 使用Queue()內置功能put()把要請求的網頁放到隊列裡。
		b. /class CrawlThread(thread.Thread)繼承Thread這個類，其中def __init__(self, thread_id, queue):中的super().__init__()是父類已經做的初始化讓他再執行一次。確保子類繼承的時候，不會把初始化的__init__覆蓋掉。
		c. /self.headers 可以自行在做更多功能，如random的方式
		d. /def run(self)則是重寫多線程run的方法，self.scheduler()真正進行調度。
		e. /def scheduler(self): 模擬隊列調度，當self.queue.empty()為空的時候，即不進行處理。不為空，則訪問book.douban.com/top250，回到requests提前準備的部分。通過requests.get()進行下載。以上在實際商業上，需要再把隊列功能與下載器功能再抽象出來，再次進行封裝，應為更加獨立的功能模塊。
		f. 頁面內容分析，使用flag標誌位？
		g. 啟動線程self.queue.get(False)獲取內容，參數為false時隊列為空，拋出異常。若非異常，表示已將網頁內容取回，使用self.parse_data(item)對網頁進行處理為正常文本。再保存到隊列當中。
		h.  將結果存到json文件中，thread = ParserThread(thread_id, dataQueue, pipeline_f)用data_Queue進行數據的抓取。
		i. /crawl_name_list三個爬取數據的線程，讀取pageQueue裡面的內容，pageQueue的內容則由調度器def scheduler()來生成我們要爬取的頁面。從pageQueue抓取的頁面，則會放到dataQueue內，再由parse_data()處理data_queue裡的內容，並存到book.json檔案內。
		j. /with open中的thread則是將原本的串行過程變成併行過程。
		k. 存到book.json後，即是標準的json格式檔案。
	4. 盲目使用大框架，反而會產生不必要的bug。



本週作業：
1. （需提交代码作业）不使用开源框架，基于 TCP 协议改造 echo 服务端和客户端代码，实现服务端和客户端可以传输单个文件的功能。
2. （需提交代码作业）使用 requests 库抓取知乎任意一个话题下排名前 15 条的答案内容 (如果对前端熟悉请抓取所有答案)，并将内容保存到本地的一个文件。
3. 通过课程代码，熟练掌握 HTTP 协议头、返回码、HTML 等知识点，这些在后面开发 Web 服务端程序时会频繁使用到。
