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
   1. 在github網頁版新增repository新增repos，並複製http連結
   2. 在本地倉庫的路徑下，git remote add origin https://github.com/YoyoHuang1991/.....git
   3. git push -u origin master上傳

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

3 版本控制練習Git Branch
====
1. 在資料夾中新增明為index.html的檔案，在裡面寫入Hello world。
2. 在cmd中查看目前該資料夾中變動的檔案，並加為要commit的檔案，再commit到目前的branch 'main'之中。
```Shell
git status
git add index.html
git commit -m "新增index.html檔案"
```
3. 新增一個branch "testingVersion"，並從main轉到該branch中
```
git branch testingVersion
git checkout testingVersion
```
4. 現在繼續編輯index.html檔案，在第二行中寫上任意文字，例如: "I love Taichung"，儲存後關閉。
5. 將目前的狀態commit到branch testingVersion中。
```Shell
git status #查看index.html為紅字，表示已經變動
git add index.html #指定單一檔案加入commit
git add -a #加入所有變更的檔案 
git commit -m "在testingVersion中更新index.html"
```
6. 轉換回branch main，這時查看index.html的檔案，方才新增的文字"I love Taichung"已不見，因為在branch main的時間點仍存在最後一次commit到main的狀態。
```Shell
git checkout main  #轉回main，方才新增的文字不見
git checkout testingVersion #轉回testingVersion，方才新增的文字又出現
```
7. 若測試版本已經沒問題，要將testingVersion變動的內容merge融入main主要版本時，可以用以下指令
```Shell
git checkout main #先回到主要版本branch
git merge testingVersion #便能將testingVersion變動的內容合併
```
8. 上傳到github，若遠端發現使用者目前要上傳的branch與遠端不同，例如: testingVersion傳到main，則會反錯，要求先做merge，而不會逕行上傳，導致版本混亂。
```Shell
git checkout testingVersion #轉到testingVersion
git push origin testingVersion  #push時，指定到testingVersion的branch。
```
9. commit反悔怎麼辦? 以下練習建議在branch testingVersion中嘗試。
```Shell
git log --oneline testing
#顯示該branch的log紀錄，到最底端可以輸入儲存的檔名，將log備份，或直接按ctrl+c可以退出log
6d39669 (HEAD -> testing, origin/main, main) <E5><88><AA>
d540784 (master) in the main
000cfd7 week00 updated
7ffd549 <E6><96><B0><E5><A2><9E>week03 homework
dd84609 Update Homework.md
d9484a0 Update Homework.md
(END)
```
目前的最新commit狀態是在第一行6d39669，可以用以下指令用"相對"或"絕對"的方式退到想到的時點。 
```Shell
git reset HEAD^ #由最新的點往後退，HEAD為最新、^箭頭是上一個，
git reset HEAD^^ #退回前兩個，^愈多，退愈多次
git reset testing^^ #testing試只branch名稱，

git reset 7ffd549 #絕對時點，直接寫log第一欄的代碼
git reset 7ffd549^ #從絕對時點往前退
```

10. 透過網頁github 來merge branch
*  打開網頁
   1. github看到方才的push，右邊有compare& pull requests, 即是merge的功能
   2. merge前可以留下意見給其他開發者，assignees選擇自己，往下拉pull request
   3. 顯示we're going to merge 2 commits into master from count-to-fifteen
   4. Click merge pull requests. 再點confirm，完成merge後，可以選delete branch，將count-to-fifteen branch刪除。
*  打開cmd或terminal
   1. 在terminal 輸入 git checkout master，電腦端這邊仍只顯示1~10，尚未更新
   2. git pull origin master ，本機端方能更新
   3. git branch可以列出本機端有的branches
   ```Shell
   git branch -d testingVersion #刪除指定的branch
   ```
11. 關於git merge --no-ff的主題，可參閱下網站https://medium.com/@fcamel/%E4%BD%95%E6%99%82%E8%A9%B2%E7%94%A8-git-merge-no-ff-d765c3a6bef5


	
	
	




	
	
	
	
