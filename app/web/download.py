#coding=utf8
from . import web

import os
import json

from app import db


from selenium import webdriver
from bs4 import BeautifulSoup



from config import basedir
import requests

from app.WorkingDaysConfig import WorkingDaysConfig









def mkdir(path):
    # 引入模块


    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)


        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在

        return False






def download_img(img_url,path):

    header = {} # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
    r = requests.get(img_url, headers=header, stream=True)


    list = img_url.split("/")
    image_name = list[-1]

    image_path = os.path.join(basedir, 'static/downloads/'+path, image_name)
    if r.status_code == 200:
        f = open(image_path, 'w')
        f.write(r.content) # 将内容写入图片
        f.close()

    del r


@web.route("/workingdays")
def readworkingdays():
    driver = webdriver.Chrome()
    driver.get("https://api.workingdays.org/1.2/api-countries.php")
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find("div", attrs={"class": "scroller"})

    list = []

    table = div.find("table")
    tbody = table.find("tbody")
    trs = tbody.select("tr")
    for tr in  trs:
        tds = tr.select("td")
        n = len(tds)
        dict = {}
        for i in  range(0,n):
            td = tds[i]
            if  0 == i:
                dict["configId"]  =  td.text
            elif 1 == i:
                dict["code"] = td.text
            elif 2 == i:
                cts = td.contents
                stringlist =[]
                for ct in  cts:
                    try:
                        s = ct.text

                    except:
                        stringlist.append(ct.strip())

                dict["configurations"] = json.dumps(stringlist)
            elif 3 ==i:
                dict["default_configuration"] = td.text.strip()
            elif 4 ==i:
                a = td.find("a")
                dict["website"] = a.attrs["href"]

        list.append(dict)
        try:
            wc = WorkingDaysConfig(dict)
            db.session.add(wc)
            db.session.commit()
        except Exception as e:

            db.session.rollback()






    db.session.close()


    driver.quit()
    return json.dumps(list)





