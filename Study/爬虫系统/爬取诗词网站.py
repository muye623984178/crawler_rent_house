import os.path

import requests
from bs4 import BeautifulSoup

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/25'
    }

dirpath = "红楼梦/"
if not os.path.exists(dirpath):
    os.mkdir(dirpath)

def get_html(url):
    htm = requests.get(url, headers=headers).content.decode('UTF-8')
    return htm

def get_list(html):
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.prettify())
    muLu = soup.select('.book-mulu')
    li = muLu[0]
    # print(li)
    a = li.find_all('a')
    # print(a)
    gen = 'https://www.shicimingju.com'
    content_list = [{
        'title': "章节名称",
        'new_url': "章节链接"
    }]
    for i in a:
        new_url = gen + i['href']
        title = i.string
        # print(title + " " + new_url)
        content_list.append({
            'title': title,
            'new_url': new_url
        })
    # print(content_list)
    return content_list

def get_chapter_content(chapter):
    # print(chapter['new_url'])
    htm = requests.get(chapter['new_url'],headers=headers).content.decode('UTF-8')
    soup1 = BeautifulSoup(htm, 'lxml')
    # print(soup1.prettify())
    s1 = soup1.select('.chapter_content')[0]
    # print(s1)
    p = s1.text.replace('    ', '\n  ')
    # print(p)
    with open(dirpath + chapter['title'] + '.txt', 'w', encoding='UTF-8') as f:
        f.write(p)
        print("%s--章节下载成功"%chapter['title'])


if __name__ == "__main__":
    url = 'https://www.shicimingju.com/book/hongloumeng.html'
    htm = get_html(url)
    content_list = get_list(htm)
    for chapter in content_list[1:]:
        get_chapter_content(chapter)
