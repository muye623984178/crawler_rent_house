import os
import re

import requests


# 该爬虫仅仅适用于该笔趣阁网址’https://045690f8e96026.bqg997.com/‘

# 通过目录获得各个章节的超链接以及章节名称
def get_list(mulu):
    head = "https://045690f8e96026.bqg997.com"
    href = []
    title = []
    # list_html = requests.get('https://045690f8e96026.bqg997.com/htm/34973/list.html').content.decode('UTF-8')
    list_html = requests.get(mulu).content.decode('UTF-8')
    # print(list_html)
    txt_list = re.findall('<dd><a href ="(.*?)">(.*?)</a></dd>', list_html)
    # print(txt_list)
    for ele in txt_list:
        href.append(head + ele[0])
        title.append(ele[1])
    return href, title


# 获取当前链接的文本内容
def get_content(href):
    html = requests.get(href).content.decode('UTF-8')
    txt = re.findall('<div id="chaptercontent" class="Readarea ReadAjax_content">(.*?)请收藏：https://m.bqg997.com',
                     html, re.S)
    return txt[0].replace('<br />', '').replace('　　', '')


# 将文章内容保存下来
def save(title, txt, name):
    os.makedirs(name, exist_ok=True)
    # 判断一个文件夹是否存在，不存在就要创建.这里的第1个参数就是文件夹的名字，第2个参数表示如果文件夹已经存在，那就什么都不做
    filepath = os.path.join(name, title + '.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(txt)


# 由于一章分为多页，需要补全
def fixed(html, txt):
    for i in range(2, 5):
        html1 = html[0:-5] + '_' + str(i) + '.html'
        res = get_content(html1)
        if res == empty_html:
            break
        else:
            txt = txt + res
    return txt


def test_part(href, title, begin, end):
    h = []
    t = []
    k = 0
    for i in range(begin - 1, end):
        h.append(href[i])
        t.append(title[i])
        # print(get_content(h[i]))
        txt = get_content(h[k])
        txt = fixed(h[k], txt)
        save(t[k], txt, name)
        print(t[k] + "保存成功")
        k = k + 1


def test_all(href, title):
    for h, t in href, title:
        txt = get_content(h)
        txt = fixed(h, txt)
        save(t, txt, name)
        print(t + "保存成功")


# 第一步输入笔趣阁中书籍的编号
# "史上最强炼气期"的x为34973
name = input("请输入本书籍名称：")
x = input("请输入该本书籍的编号（网址中的数字）：")
begin = eval(input("请输入从第几章开始爬取（如3）："))
end = eval(input("请输入爬取到第几章（如10，请勿输入不存在的章节）："))
empty_html = get_content('https://045690f8e96026.bqg997.com/htm/' + x + '/1_6.html')

# 第二步获取书籍的目录
mulu = 'https://045690f8e96026.bqg997.com/htm/' + x + '/list.html'

# 第三步获取各章节的超链接地址以及章节名称
href, title = get_list(mulu)

# 第四步获取各章节文本内容，并保存到特定文件夹下
test_part(href, title, begin, end)

# 第五步通知用户爬虫完毕
print("爬虫已完成")
