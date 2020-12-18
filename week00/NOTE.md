1 Python訓練營week00
====
1. 安裝git 初始化倉庫並做最簡單的配置
   1. git init
   2. git config --global user.name 'yourname'
   3. git config --global user.email '必須是能接受到email的真實email'
   4. git config --global list

2. 完成一個最簡單的git操作流程:工作區、暫存區何倉庫
   1. git status #查看目前資料夾狀態，偵測是否有檔案修改
   2. linux指令pwd查看目前路徑
   3. 指令vim readme.md，"I"進入inser模式，退出Esc再輸入:wq ，write然後quit
   4. git add . 或是git add readme.md追蹤檔案變更，變成『已暫存』狀態
   5. git commit -m "create readme.md" ＃為提交作注釋
   6. git status #目前會顯示nothing to commit，變成『已提交』狀態
   7. 修改檔案後，git commit -m "readme 2.0"
   8. git log 可以查看commit的時間歷程

3. 將本地倉庫同步到遠程github倉庫
   1. 在github網頁版新增repository新增repos，並複製ssh連結
   2. 在本地倉庫的路徑下，git remote add origin git@github.com:….git
   3. ssh-keygen -t rsa -C "a5339577@gmail.com"
   4. 使用默認的金鑰名稱
   5. ssh -T git@github.com 查看是否已經連接
   6. git push -u origin master上傳

4. 訓練營提交作業的完整流程
   1. Fork是不影響原本程式碼的情況下，複製到自己的github空間。
   2. 再用git clone http，下載到本機電腦

2 使用terminal 操作git
====
1. Git --version確認是否安裝，mac os透過Xcode安裝
2. 透過touch指令可新增檔案
```Shell
touch "index.html" 
```
4. 回到上個commit的時間點，即使刪除檔案，使用此指令，檔案也可以恢復，作為回溯。
```Shell
git check out -- . 
```
5. 從github以下載到目前位置
```Shell
git clone https://github.com/LearnWebCode/welcome-to-git/ 
```
6.  顯示目前fetch與push的設定
```Shell
git remote -v 
```
7.  設定push的目的地。
```Shell
git remote set-url orgin https://github.com/YoyoHuang1991/gitworkflow.git
# 若都沒反應時，可以用
git remote add origin https://github.com/YoyoHuang1991/gitworkflow.git
```
asdfasdflajsdlfjlaskjdfklj

	
	
	




	
	
	
	
