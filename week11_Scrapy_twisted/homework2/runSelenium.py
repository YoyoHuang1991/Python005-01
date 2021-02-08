from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

"""
1. 104首頁搜尋『python 台北』:
https://www.104.com.tw/jobs/search/?keyword=python&area=6001001000&jobsource=2018indexpoc&ro=0

2. 滾輪往下，搜尋結果會先顯示23個，滑到18項，會加載10個結果；滑到第34個，會再加載29個
23 - 18 = 5
43 - 23 = 10
63 - 34 = 29
103 - 76 = 27
while article數量 < 100: 一直將滾輪往下滾。

3. 找到//button[@class ="b-btn b-btn--page js-next-page"] 加載下一頁，執行4次，加到五頁，但這個方法不可行，畫面沒也滑到button的位置，即使用js直接click仍不會加載。

當滾輪停下來，將100個職缺用thePage = pd.read_html(browser.page_source)抓下來存到thePage變數中。

targetElem = browser.find_element_by_xpath("//a[@id='pagnNextLink']/span[@id='pagnNextString']")
# browser.execute_script("arguments[0].scrollIntoView();", targetElem)    # 拖动到可见的元素去







"""
url ='http://www.espn.com/nba/statistics/player/_/stat/assists/sort/avgAssists/'

browser = webdriver.Chrome()  # 啟動 Chrome Browser， 'chromedriver.exe'與本 notebook 程式在同一路徑之下

browser.get(url)   # 連接目的地網頁伺服器

while True:

    try:
    
        button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Show More')))
        
        button.click()
        
        print("SHOW/LOAD MORE RESULTS button clicked")  # 共有 6 頁，第一頁不算，應該會執行按鈕 5 次
    
    except TimeoutException:
        
        print("No more SHOW/LOAD MORE RESULTS button to be clicked")  # 最後 10 秒後會遇上 selenium.common.exceptions.TimeoutException
        
        break


import pandas as pd

tables = pd.read_html(browser.page_source)

print('找出 %02d 個表格' % len(tables))

df1 = tables[0]  # 第一個表格

df2 = tables[1]  # 第二個表格

df3 = pd.concat([df1, df2], sort = False, axis = 1)  # sort = False 關閉警告訊息

df3.set_index('RK', inplace = True) 

pd.set_option('display.max.columns', 22)   # 在此例中無用處，因原表格內的欄位數目僅有六項

pd.set_option('display.max.rows', 262)

df3