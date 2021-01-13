# 載入所需要的套件
import requests
import time
import os
import re
from bs4 import BeautifulSoup


# 建立 headers 與設定 url
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}
url = 'https://www.ptt.cc/bbs/prozac/index{}.html'
page = 1267


# 建立替換檔案名稱非法字元的函數
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替換為下劃線
    return new_title


# 向PTT憂鬱版送出請求
for i in range(153):    # 憂鬱版共1267頁
    res = requests.get(url=url.format(page), headers=headers)
    # print(res)   # get response <Response [200]>
    html = res.text
    # print(html)

    # 將 html 轉換成 BeautifulSoup 型態
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    # 取出包著標題與標題url的標籤
    title_list = soup.select('div[class="title"]')
    # print(title_list)

    # 用迴圈個別取出抓取每一個標題、網址、內容
    for title_soup in title_list:
        # print(title_soup)
        title_tmp_soup = title_soup.select('a')

        if len(title_tmp_soup) == 0:
            pass
        else:
            title = title_tmp_soup[0].text
            title_url = 'https://www.ptt.cc' + title_tmp_soup[0]['href']
            print(title, '\n', title_url)

            # 爬取標題內容
            res_article = requests.get(url=title_url, headers=headers)
            soup_article = BeautifulSoup(res_article.text, 'html.parser')
            soup_article_content = soup_article.select(
                'div[id="main-content"]')[0].text
            article = soup_article_content.split('※ 發信站:')[0]     # 將留言去除

            # print(article)

            print('============================================================', '\n')

            # 存取標題內容
        try:
            with open('./爬蟲/2_PTT憂鬱版/{}.txt'.format(title), 'w', encoding='utf-8') as f:
                f.write(article)
        except FileNotFoundError or OSError:  # 若檔案名稱有非法字元，即使用line 20 建立的method
            with open('./爬蟲/2_PTT憂鬱版/{}.txt'.format(validateTitle(title)), 'w', encoding='utf-8') as f:
                f.write(article)
        except:
            pass

    # 換頁
    page -= 1

    # 若因連線或其他error中斷可以直接從上一個顯示的index開始爬
    print("===================================換頁(開始爬index{})============================================".format(page))

    # 讓爬蟲休息七秒鐘～
    time.sleep(7)
