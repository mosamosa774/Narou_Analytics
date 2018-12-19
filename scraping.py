#soup -*- coding: utf-8 -*- 
#pip install requests
#pip install beautifulsoup4
#pip install lxml
import requests
from bs4 import BeautifulSoup
import sys
import time
import json
import collections as cl
import codecs
from datetime import datetime

def getRankingList():
    url = sys.argv[1]
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    rank = "best"
    ranking_list = []

    for i in range(1,101):
        ranking = soup.find_all("a", id=rank+str(i))
        for a in ranking:
            ranking_list.append( (a.text,  a.attrs['href'], 0) )

    return ranking_list

def searchSimilarNovel(main_novel_page,depth,novelList,target_list):
    if depth >= int(sys.argv[2]):
        return target_list
    recommend = main_novel_page.find_all("div", class_="recommend_novel")
    for i in recommend:
        haveDone = False
        novel = i.find("span").text
        print(novel)
        for j in novelList:
            if novel == j[0]:
                haveDone = True
                break
        for j in target_list:
            if novel == j[0] or haveDone:
                haveDone = True
                break
        print(haveDone)
        if not haveDone:
            target_list.append( (novel,i.find("a").attrs['href'],depth+1) )
    return target_list

def analyzeNovel(title,main_novel_page,novelList):
    hrefs = main_novel_page.find_all("a")
    for i in hrefs:
        if i.text == "小説情報":
            time.sleep(1)
            res = requests.get(i.attrs['href'])
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, 'lxml')
            attr = soup.find_all("tr")
            for j in attr:
                _attr = j.find("th")
                if _attr.text == "作者名":
                    name = j.find("td").text
                elif _attr.text == "キーワード":
                    keyword = j.find("td").text
                elif _attr.text == "ジャンル":
                    genre = j.find("td").text
                elif _attr.text == "感想":
                    impre = j.find("td").text
                elif _attr.text == "総合評価":
                    _eval = j.find("td").text
                elif _attr.text == "ポイント評価":
                    each_eval = j.find("td").text
                elif _attr.text == "文字数":
                    word_count = j.find("td").text
            novelList.append( (title,name,keyword,genre,impre,_eval,each_eval,word_count) )
            break
    return novelList
    
def startAnalytics():
    novelList = []
    target_list = getRankingList()
    while target_list:
        novel = target_list.pop(0)
        time.sleep(1)
        res = requests.get(novel[1])
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, 'lxml')

        novelList = analyzeNovel(novel[0],soup,novelList)
        print("Done!!:"+novel[0])
        print("Depth:"+str(novel[2]))
        target_list = searchSimilarNovel(soup,novel[2],novelList,target_list)

    ys = cl.OrderedDict()
    for i in novelList:
        data = cl.OrderedDict()
        data["作者名"] = i[1].replace("\xa0","").replace("\n"," ")
        data["キーワード"] = i[2].replace("\xa0","").replace("\n"," ")
        data["ジャンル"] = i[3].replace("\xa0","").replace("\n"," ")
        data["感想"] = i[4].replace("\xa0","").replace("\n"," ")
        data["総合評価"] = i[5].replace("\xa0","").replace("\n"," ")
        data["ポイント評価"] = i[6].replace("\xa0","").replace("\n"," ")
        data["文字数"] = i[7].replace("\xa0","").replace("\n"," ")

        ys[i[0]] = data

    now = datetime.now()
    with codecs.open('NovelEvaluationData_'+str(now).replace(":"," ").split(".")[0]+'.json','w','utf-8') as f:
        dump = json.dumps(ys,ensure_ascii=False,indent=2)
        f.write(dump)

startAnalytics()