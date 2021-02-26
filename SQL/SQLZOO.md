docker建立microsoft SQL server，並使用SSMS連線至docker
====
## 在docker安裝microsoft SQL server
以下是官方教學 https://docs.microsoft.com/zh-tw/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15

先安裝好docker後，在powershell執行以下指令，安裝sql server及設定帳號、新database  
1. 下載映像檔與安裝
```shell
docker pull mcr.microsoft.com/mssql/server:2019-latest
```
2. 設定帳號與密碼
```shell
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=<YourStrong@Passw0rd>" 
   -p 1433:1433 
   --name sql1 
   -h sql1 
   -d mcr.microsoft.com/mssql/server:2019-latest
```

|參數|描述|
|----|----|
|-e "ACCEPT_EULA=Y"	|將 ACCEPT_EULA 變數設為任意值可確認您接受 終端使用者授權合約。 此為 SQL Server 映像的必要設定。|
|-e "SA_PASSWORD=<YourStrong@Passw0rd>"|	指定您自己的強式密碼，該密碼長度至少需為 8 個字元且符合 SQL Server 密碼需求。 此為 SQL Server 映像的必要設定。|
|-p 1433:1433	|將主機環境上的 TCP 連接埠 (第一個值) 對應至容器中的 TCP 連接埠 (第二個值)。 在本範例中，SQL Server 正在接聽容器中的 TCP 1433 且對主機上的連接埠 1433 公開。|
|--name sql1	|為容器指定自訂名稱，而不使用隨機產生的名稱。 若您執行數個容器，就無法使用此相同名稱。|
|-h sql1	|用來明確設定容器主機名稱，如果您未指定，則會預設為隨機產生之系統 GUID 的容器識別碼。|
|mcr.microsoft.com/mssql/server:2019-latest	|SQL Server 2019 Ubuntu Linux 容器映像。|

3. 檢視docker容器
```shell
docker ps -a
```
4. 建議您將 -h 與 --name 設為相同的值，這會讓識別目標容器更輕鬆。因為 **SA_PASSWORD 會顯示在 ps -eax 輸出**，且儲存在相同名稱的環境變數中，所以最後一個步驟是變更您的 SA 密碼。 請參閱下方步驟。

5. 使用 docker exec 來執行 sqlcmd，以使用 Transact-SQL 變更密碼。 在下列範例中，將舊密碼 <YourStrong!Passw0rd> 和新密碼 <YourNewStrong!Passw0rd> 取代為您自己的密碼值。
```shell
docker exec -it sql1 /opt/mssql-tools/bin/sqlcmd `
   -S localhost -U SA -P "<YourStrong@Passw0rd>" `
   -Q "ALTER LOGIN SA WITH PASSWORD='<YourNewStrong@Passw0rd>'"
```
## 連線至SQL server
1. sql1是方才建立**容器**時，--name參數指定的
```shell
docker exec -it sql1 "bash"
```
2. 進入容器後，以sqlcmd進行本機連線
```bash
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "<YourNewStrong@Passw0rd>"
```

## 以sqlcmd和Transact-SQL來建立新資料庫、新增資料及執行查詢
1. Transact-SQL命令，建立資料庫，需執行GO才會執行前面的指令。
```sql
CREATE DATABASE TestDB
SELECT Name from sys.Databases
GO
```
2. 使用TeastDB、新建資料表Inventory、插入兩筆資料
```sql
USE TestDB
CREATE TABLE Inventory (id INT, name NVARCHAR(50), quantity INT)
INSERT INTO Inventory VALUES (1, 'banana', 150); INSERT INTO Inventory VALUES (2, 'orange', 154);
GO
```
3. 選取資料
```sql
SELECT * FROM Inventory WHERE quantity > 152;
GO
```

## SSMS連線到docker內的SQL server
1. 伺服器名稱: localhost。
原本使用localhost,1433可以登入，但是進一步操作，都會出現error 18456，省掉,1433後，就不會出錯。
2. 驗證: SQL server驗證
3. 登入: sa 
4. 密碼: 方才設定的

## 移除容器
由於方才有製作port為1434的測試sql2，現在做刪除。
```shell
docker stop sql2   
docker rm sql2
```

## 還原資料庫
* 先從課本提供的範例網址下載檔案 https://www.delightpress.com.tw/bookothers/sknd00002.html
* 由於資料庫是建在docker內，還原時，無法抓到windows本機的資料，需要將資料庫備份複製到docker容器內。  
* 其中 42c4d50002bb為該server的docker name，可以用docker ps -a列出做查詢。
1. 複製整個資料夾
```shell
docker cp D:/Users/Yuyu/Desktop/test/ 42c4d50002bb:/var/opt/mssql/data/
```
2. 複製單個檔案
```shell
docker cp D:/Users/Yuyu/Desktop/test/test.txt 42c4d50002bb:/var/opt/mssql/data/test.txt
```
3. 將檔案從docker複製到本機，前後順序調換就可以
```shell
docker cp 42c4d50002bb:/var/opt/mssql/data/test.txt D:/Users/Yuyu/Desktop/test/test.txt 
```

書籍基本SQL用法
====

1. SELF JOIN(自我連結)，僅列出右邊的表主鍵等於左表的Upper_Dept_Id欄
```sql
SELECT  D.Dept_Name
		, P.Dept_Name Upper_Dept_Name
  FROM Departments D, Departments P
 WHERE P.Dept_Id = D.Upper_Dept_Id;
```


-- Select the code that shows the countries with a less than a third of the population of the countries around it

-- 1. 子查詢，列出同region其他國家的population/3
-- 2. 父查詢，population小於所有子查詢

/*
SELECT name, region
FROM bbc x
WHERE population < (SELECT population/3 
        FROM bbc y
        WHERE y.region=x.region AND y.name!=x.name)
*/

/*https://sqlzoo.net/wiki/SUM_and_COUNT 的第七題
計算各州人口超過10 million的國家有幾個。
*/
SELECT continent, COUNT(name)
FROM world
WHERE population >= 10000000
GROUP BY continent

/* JOIN常用寫法 */
SELECT A.N, B.N
FROM　A, B
WHERE A.N = B.N

SELECT A.N, B.N
FROM A INNER JOIN B
ON A.N = B.N

/* GROUP BY後若要加條件判斷，需使用HAVING */
SELECT continent
FROM world
GROUP BY continent
HAVING SUM(population) >= 100000000

SELECT SUM(population)
FROM world
WHERE region='Europe'

SELECT COUNT(name)
FROM world
WHERE population < 150000


/*面試會遇到的問題，JOIN兩個表，並計算各個team的總得分*/
SELECT teamname
      ,COUNT(player) AS SCORES
FROM eteam JOIN goal ON id=teamid
GROUP BY teamname
ORDER BY teamname

SELECT stadium
      ,COUNT(player) AS SCORES
FROM game JOIN goal ON game.id=goal.matchid
GROUP BY stadium

/* 有POL的比賽中，該場得分數，team1+team2的加總 */
SELECT matchid
      ,mdate
      ,COUNT(teamid)
FROM game JOIN goal ON game.id=goal.matchid
WHERE (team1='POL' OR team2='POL')
GROUP BY matchid, mdate

/*計算GER各場比賽的得分*/
SELECT matchid
      ,mdate
      ,COUNT(teamid)
FROM game JOIN goal ON game.id=goal.matchid
WHERE teamid='GER'
GROUP BY matchid,mdate

SQLZOO 04|SELECT within SELECT Tutorial
====
* 網址: https://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial
## 第5題
Microsoft SQL server若遇到float後面有很多0，需要使用CAST將float的數值改為int。用MySQL則不會出現很多零。
```sql
SELECT name
      ,CONCAT(
         CAST(
          ROUND(100*population/(select population from world where name='Germany'),0) 
          as int)
        ,'%') as percentage 
FROM world 
WHERE continent = 'Europe'
```
## 第8題
str字串間可以比大小，是依據database的字符集排序str的前後大小。name <=ALL 即排序第一個的name。
```sql
SELECT continent, name FROM world x
 WHERE name <= ALL
    (SELECT name FROM world y
        WHERE y.continent=x.continent
    )
```


SQLZOO 06|JOIN
====
* 題目網址: https://sqlzoo.net/wiki/The_JOIN_operation

## 第13題
查詢結果一直看不到team1與team2皆為0分的那兩場比賽，把JOIN改為LEFT JOIN才解決。
```sql
/*錯誤*/
SELECT mdate
      ,team1
      ,SUM(CASE WHEN teamid=team1 THEN 1 
            ELSE 0 
            END) score1
      ,team2
      ,SUM(CASE WHEN teamid=team2 THEN 1
            ELSE 0
            END) score2
FROM game JOIN goal ON matchid=id
GROUP BY mdate, team1,team2
ORDER BY mdate, matchid, team1, team2
/*正確*/
SELECT mdate
      ,team1
      ,SUM(CASE WHEN teamid=team1 THEN 1 
            ELSE 0 
            END) score1
      ,team2
      ,SUM(CASE WHEN teamid=team2 THEN 1
            ELSE 0
            END) score2
FROM game JOIN goal ON matchid=id
GROUP BY mdate,team1,team2
ORDER BY mdate, matchid, team1, team2
```

SQLZOO 07|More JOIN
====
