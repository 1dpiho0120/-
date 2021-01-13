# 載入爬蟲所需的套件
import requests
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime    # 載入日期的套件
from opencc import OpenCC        # OpenCC為簡體轉繁體的python套件


# 定義將簡體轉為繁體的變數
cc = OpenCC('s2hk')


# 建立替換檔案名稱非法字元的函數
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替換為下劃線
    return new_title


# 建立headers與設定url
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}
url = 'https://www.jianshu.com/u/e0755477c171?order_by=shared_at&page={}'
page = 1


for i in range(4):
    # 向部落格網址送出請求
    res = requests.get(url=url.format(page), headers=headers)
    # print(res)   # <Response [200]
    html = res.text
    # print(html)

    # 將html轉換為BeautifulSoup型態
    soup = BeautifulSoup(html, 'html.parser')
    soup_title_list = soup.select(
        'div[class="content"]')    # 取出包在標籤裡面的標題、網址、日期
    # print(soup_title_list)

    for content in soup_title_list:
        title = content.select('a[class="title"]')[0].text    # 取出標題
        title = cc.convert(title)    # 將標題從簡體轉為繁體
        title_url = 'https://www.jianshu.com' + \
            content.select('a[class="title"]')[0]['href']      # 取出文章網址

        date_time = content.select('span[class="time"]')

    # 取出文章日期
        for date_list in date_time:
            date_list = str(date_list)
            match = re.search(r'\d{4}-\d{2}-\d{2}', date_list)
            date = datetime.strptime(match.group(), '%Y-%m-%d').date()

        print(title, ' ', date, '\n', title_url)

        # 取出每一篇的文章內容
        res_article = requests.get(url=title_url, headers=headers)
        soup_article = BeautifulSoup(res_article.text, 'html.parser')
        article = soup_article.select('article')[0].text
        article = cc.convert(article)

        # print(article)
        print('=================================================')

        # 將內容以txt存檔
        with open('./爬蟲/1_抑鬱治療日記_71284332/{}_{}.txt'.format(title, date), 'w', encoding='utf-8') as f:
            f.write(article)

    page += 1
    print("============================scrolling down==============================")
