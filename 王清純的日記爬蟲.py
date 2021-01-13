# 載入爬蟲所需的套件
import os
import time
import re
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from opencc import OpenCC


# 定義將簡體轉為繁體的變數
cc = OpenCC('s2hk')


# 建立替換檔案名稱非法字元的函數
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替換為下劃線
    return new_title


# 設定url
driver = Chrome('./爬蟲/1_王清純的日記/chromedriver')  # 指定瀏覽器的位置
url = 'https://www.douban.com/people/nevertouchwyl/notes?start={}&type=note'
page = 130


for i in range(1):
    # 使用Chrome瀏覽器瀏覽網頁
    driver.get(url=url.format(page))
    # print(driver.page_source)

    # 將html轉為BeautifulSoup型別
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title_soup = soup.select('div[class="note-header-container"]')
    # print(title_soup)

    for title_list_soup in title_soup:
        tmp_title_list = title_list_soup.select('a')
        tmp_url_list = title_list_soup.select('a[class="j a_unfolder_n"]')
    # print(tmp_url_list)

    # 取出標題
        for title_list in tmp_title_list:
            title = title_list.text
            title = cc.convert(title)
            print(title)

        # 取出文章url
        for url_list in tmp_url_list:
            article_url = url_list['href']
            print(article_url)

            # 帶著regpop=1的cookies訪問網頁以防止彈跳視窗阻礙爬蟲
            driver.get(article_url)
            try:
                driver.find_element_by_class_name('ui-overlay-close').click()
            except:
                pass
            # 得到取消登入的cookies
            cookie = driver.get_cookies()

            # 取得文章內容
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            soup_article = soup.select('div[class="note"]')
            tmp_soup_article = soup_article[1].text
            tmp_article = cc.convert(tmp_soup_article)

            # 篩選掉作者的個人資訊
            try:
                article = tmp_article.split('=')[0]
                # print(article)
            except:
                article = tmp_article

            # 將文章寫入文字檔
            try:
                with open('./爬蟲/1_王清純的日記/{}.txt'.format(title), 'w', encoding='utf-8') as f:
                    f.write(article)
            except FileNotFoundError or OSError:  # 若檔案名稱有非法字元，即使用line 13 建立的method
                with open('./爬蟲/1_王清純的日記/{}.txt'.format(validateTitle(title)), 'w', encoding='utf-8') as f:
                    f.write(article)
            except:
                pass

            # 休息五秒再繼續跳下一篇文章
            # time.sleep(10)

    # 休息五秒跳入下一頁
    time.sleep(5)

    page += 10

    print("==========================heading to page {}======================================".format(page))
