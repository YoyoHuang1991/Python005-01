学习笔记

01 MySQL安裝
====
1. 企業級部屬在linux操作系統，注意版本不同、安裝後避免yum自動更新、數據庫的安全性。
2. CentOS預設用MariaDB，一般我們用MySQL社區版。
3. 可用ssh連現在遠程的linux服務器，
4. 指令arch可查看目前linux是否為64位元系統
5. CentOS，可cat /etc/redhat-release，查看對應版本，使用yum安裝包時，需要先看。
6. 訪問dev.mysql.com，安裝5.7.32的社區版，選擇通用linux版本。先把所有包都下載完成，使用ls -lh可列出文件的大小和具體名字。
7. 先在virtual box 安裝cent OS 7的虛擬機，
    1. http://centos.cs.nctu.edu.tw/7.9.2009/isos/x86_64/
    2. 安裝完成後，設置顯示的字體大小    
    ```Shell
    [root@localhost ~]# cd /lib/kbd/consolefonts  //進入到有自體的目錄
    [root@localhost consolefonts]# ls                        //查看所有字體
    [root@localhost consolefonts]# setfont lat4-19                    //設置所選自體，19是字體大小
    [root@localhost consolefonts]# echo 'setfont lat4-16+'  >> /etc/bashrc         //設置為開機時默認字體
    ```
    3. 由於是最小安裝，網卡不會隨作業系統開機而開啟，
    ```Shell
    //1. 驗證yum 是否正常安裝
    [root@localhost ~]# yum --help 
    //2. 驗證配置resolv.conf:
    [root@localhost ~]# vi /etc/resolv.conf  
    //3. 進入vi編輯模式，按I進入insert添加以下兩行:
    nameserver 8.8.8.8
    search localdomain
    //4. 按Esc，輸入:wq退出vi
    //5. 驗證網卡配置，進入network-scripts找到ifcfg-ens33網卡配置文件
    [root@localhost ~]# cd /etc/sysconfig/network-scripts  
    [root@localhost network-scripts]# ls -a 
    [root@localhost network-scripts]# vi ifcfg-ens33
    //6. 按I進入insert模式，把onboot的值改為yes, 再按esc後輸入:wq關閉文件
    //7. 重新啟動CentOS
    [root@localhost network-scripts]# reboot
    //8. 驗證yum是否正常運作
    [root@localhost ~]# yum provides ifconfig
    ```
    4. 用yum安裝MySQL
    
8. 指令yum install mysql57-community-release-el7-10.noarch.rpm





   ![](./res/image-filter.png)
	
	

