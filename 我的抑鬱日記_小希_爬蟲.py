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


# 指定chrome driver的位置 & 設定url
driver = Chrome('./爬蟲/1_我的抑鬱日記_小希(廣東話)/chromedriver')
url = "http://heymaninfo.blogspot.com/"


# 使用chrome瀏覽部落格
driver.get(url)


for i in range(2):

    # 將html轉回BeautifulSoup型別
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 找出有標題與網址的標籤
    title_soup_list = soup.select('h3[class="post-title entry-title"]')

    # 取出標題與文章網址
    for tmp_title_list in title_soup_list:
        # print(tmp_title_list)
        title = tmp_title_list.text
        article_url = tmp_title_list.select('a')[0]['href']

        # 瀏覽文章內容的網址
        driver.get(article_url)
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        article_soup_list = soup2.select(
            'div[class="post-body entry-content"]')

        for tmp_article_list in article_soup_list:
            article = cc.convert(tmp_article_list.text)

        print(title, '\n', article_url)
        print(cc.convert(tmp_article_list.text))

    # 將滾輪移到最下面 → 點擊Older Posts
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    driver.find_element_by_class_name('blog-pager-older-link').click()
