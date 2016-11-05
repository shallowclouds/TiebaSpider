#coding=UTF-8
import requests
import re
import json
from bs4 import BeautifulSoup
import mysql.connector
#from pybloomfilter import BloomFilter

nexts=None

class TiebaSpider:
    soup=None
    idxPage=None
    preurl=r"http://tieba.baidu.com"
    nextPage=None
    pageCnt=0
    MaxPage=1
    pages=[]
    tableName="Test"
    userName="Spider"
    passwdValue="123456"
    postIdx=1
    spostIdx=1
    blf=None
    usedset=set()
    def __init__(self, url):

        if url is None:
            print("Error:the url cannot be empty")
            return
#        self.idxPage=requests.get(url)
#        self.soup=BeautifulSoup(self.idxPage.content,"html.parser")
        self.nextPage=url
        #self.soup = BeautifulSoup(open("1.html","rb"), "html.parser")

    def setMaxPage(self,mPage=1):
        self.MaxPage=mPage

    def setTableName(self,name="Test"):
        self.tableName=name

    def setUserAndPasswd(self,username="Spider",passwd="123456"):
        self.userName=username
        self.passwdValue=passwd

    def start(self):
        conn = mysql.connector.connect(user=self.userName,password=self.passwdValue,database=self.tableName)
        cursor=conn.cursor()
        #self.blf=BloomFilter(100000,0.001,"bf_test.bloom")
        #cursor.execute("select content from post where id=1")
        #temp=cursor.fetchall()
        #print(temp)
        #return

        cursor.execute("create table if not exists postUrl(id INT PRIMARY KEY ,url VARCHAR (50))")
        conn.commit()
        cursor.execute("create table if not exists post(id INT PRIMARY KEY ,content TEXT,pdata TEXT)")
        conn.commit()
        cursor.execute("select url from postUrl")
        usedurl=cursor.fetchall()
        for i in usedurl:
            self.usedset.add(i[0])
            print(i[0])
        usedurl.clear()
        cursor.execute("select max(id) from postUrl")
        maxId=cursor.fetchall()
        if maxId[0][0] is not None:
            self.postIdx=int(maxId[0][0])+1
        print("start from index"+str(self.postIdx))

        cursor.execute("select max(id) from post")
        maxId=cursor.fetchall()
        if maxId[0][0] is not None:
            self.spostIdx=int(maxId[0][0])+1
        print("start from small post index"+str(self.spostIdx))
        tre = re.compile(r"^/p")
        tt = re.compile(r"^next")
        while True:
            if self.pageCnt>=self.MaxPage:
                break
            pageNow=requests.get(self.nextPage)
            self.soup=BeautifulSoup(pageNow.content,"html.parser")
            atag = self.soup.find_all("a")
            for i in atag:
                if self.pageCnt>=self.MaxPage:
                    break
                allcs=i.attrs
                try:
                    #print(allcs["class"])
                    if re.match(tt,allcs["class"][0]):
                        self.nextPage=allcs["href"]
                        print(allcs["href"])
                except:
                    pass
                try:
                    if re.match(tre,allcs["href"]):
                        print(allcs["href"])
                        if allcs["href"] not in self.usedset:
                            self.usedset.add(allcs["href"])
                            self.pages.append(allcs["href"])
                            self.pageCnt=self.pageCnt+1
                        print(i.string)
                except:
                    pass

        postRe=re.compile(r"^post_content_")
        postNextRe=re.compile(r"^下一页")
        fileCnt=0
        postString = []
        for i in range(1,self.pageCnt+1):

            nextPostPage=self.pages[i-1]
            lastPostPage=None
            while True:
                if nextPostPage==lastPostPage or nextPostPage is None:
                    break
                cursor.execute("insert into postUrl(id,url) values(%s,%s)",[self.postIdx,nextPostPage])
                conn.commit()
                self.postIdx=self.postIdx+1
                lastPostPage=nextPostPage
                rq=requests.get(self.preurl+nextPostPage)
                print("next Page start:"+nextPostPage)
                tSoup=BeautifulSoup(rq.content,"html.parser")
                alldiv=tSoup.find_all("div")
                print(len(alldiv))
                for j in alldiv:
                    allcs=j.attrs

                    try:
                        #print(allcs["id"])
                        #print(j.string)
                        if re.match(postRe,allcs["id"]):
                            #print(allcs["id"])
                            #postString.append(j.strings)
                            #for str in j.strings:
                            #   print(str)
                            tcontent=str("")
                            for sstr in j.strings:
                                tcontent=tcontent+sstr
                                #print(tcontent)
                            postData=j.parent.parent.parent.parent
                            pData=postData["data-field"]
                            cursor.execute("insert into post(id,content,pdata) values(%s,%s,%s)",[self.spostIdx,tcontent,pData])
                            self.spostIdx=self.spostIdx+1
                            conn.commit()
#{"author":{"user_id":911602112,"user_name":"\u788e\u5f97\u50cf\u7eb8\u5c51","name_u":"%E7%A2%8E%E5%BE%97%E5%83%8F%E7%BA%B8%E5%B1%91&ie=utf-8","user_sex":1,"portrait":"c0f1e7a28ee5be97e5838fe7bab8e5b1915536","is_like":1,"level_id":8,"level_name":"\u901a\u7f09\u72af","cur_score":898,"bawu":0,"props":null},"content":{"post_id":95833572120,"is_anonym":false,"open_id":"tbclient","open_type":"apple","date":"2016-08-11 16:24","vote_crypt":"","post_no":2,"type":"0","comment_num":8,"ptype":"0","is_saveface":false,"props":null,"post_index":1,"pb_tpoint":null}}

                    except:
                        pass
                alla=tSoup.find_all("a")
                for j in alla:
                    allcs=j.attrs
                    try:
                        #print(j.string)
                        if re.match(postNextRe,j.string):
                            nextPostPage=allcs["href"]
                            print(allcs["href"])
                    except:
                        pass
            #postFile=open("%d.txt"%fileCnt,"w")
            #for j in postString:
            #    if j is None:
            #        continue
            #    postFile.write(j)
            #postFile.close()
            postString=[]
            fileCnt=fileCnt+1
        conn.close()



if __name__=="__main__":
    mSpider=TiebaSpider(url=r"http://tieba.baidu.com/f?ie=utf-8&kw=%E5%8D%97%E5%B1%B1%E4%B8%AD%E5%AD%A6")
    mSpider.setMaxPage(50)
    mSpider.start()
