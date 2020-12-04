# 使用requests库获取豆瓣影评
import requests
from pathlib import Path
import sys
from lxml import etree
# PEP-8
# Google Python 风格指引

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {'user-agent':ua}

myurl = 'https://www.zhihu.com/api/v4/questions/432348153/answers?include=content&limit=20&offset=0&platform=desktop&sort_by=default'

try:
    res = requests.get(myurl, headers=header)
except requests.exceptions.ConnectTimeout as e :
    print(f"requests库超时")
    sys.exit(1)


res.encoding = 'utf-8'
data = res.json()

#//span[@class="RichText ztext CopyrightRichText-richText"]



# 将网页内容改为存入文件
# 获得python脚本的绝对路径
p = Path(__file__)
pyfile_path = p.resolve().parent
# 建立新的目录html
html_path= pyfile_path.joinpath('html')

if not html_path.is_dir():
    Path.mkdir(html_path)
page = html_path.joinpath('zhihu.html')

# 上下文管理器
try:
    with open(page, 'w',  encoding='utf-8') as f:
        i = 1
        for line in data['data']:
            content = f"<h2>回覆{i}</h2>\n" + line['content'] + '\n'
            f.write(content)
            i+=1
except FileNotFoundError as e:
    print(f'文件无法打开,{e}')
except IOError as e:
    print(f'读写文件出错,{e}')
except Exception as e:
    print(e)
