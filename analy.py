import json
import mysql.connector
import time
import io

user="Spider"
passwd="123456"
conn = mysql.connector.connect(user=user,password=passwd,database="test")
cursor=conn.cursor()
cursor.execute("select pdata from post")
alldata=cursor.fetchall()

def time_anay():
    cnt=0
    timeline = []
    for i in alldata:
        jdata = json.loads(i[0])
        ttime = jdata["content"]["date"]
        timeline.append(time.strftime(ttime))
        cnt = cnt + 1
    print("totally %d data" % cnt)

    file1 = open("time.csv", "w")
    sorted(timeline)
    yester = None
    days = []
    print(timeline[0])
    print(timeline[0][11:13])
    xlen = len(timeline)
    print(xlen)
    clockCnt = []
    for i in range(0, 24):
        clockCnt.append(0)
    for i in range(0, xlen - 1):
        clockCnt[int(timeline[i][11:13])] = clockCnt[int(timeline[i][11:13])] + 1
    for i in range(0, 24):
        if i != 23:
            file1.write(str(i) + ",")
        else:
            file1.write(str(i) + "\n")
    for i in range(0, 24):
        if i != 24:
            file1.write(str(clockCnt[i]) + ",")
        else:
            file1.write(str(clockCnt[i]) + "\n")
#{"author":{"user_id":911602112,"user_name":"\u788e\u5f97\u50cf\u7eb8\u5c51","name_u":"%E7%A2%8E%E5%BE%97%E5%83%8F%E7%BA%B8%E5%B1%91&ie=utf-8","user_sex":1,"portrait":"c0f1e7a28ee5be97e5838fe7bab8e5b1915536","is_like":1,"level_id":8,"level_name":"\u901a\u7f09\u72af","cur_score":898,"bawu":0,"props":null},"content":{"post_id":95833572120,"is_anonym":false,"open_id":"tbclient","open_type":"apple","date":"2016-08-11 16:24","vote_crypt":"","post_no":2,"type":"0","comment_num":8,"ptype":"0","is_saveface":false,"props":null,"post_index":1,"pb_tpoint":null}}
def platform_anay():
#    jdata=json.loads(alldata[1][0])
#    print(jdata["content"]["open_type"])
#    return

    cnt=0
    plat = []
    anay={"apple":0,"android":0}
    for i in alldata:
        jdata = json.loads(i[0])
        cnt=cnt+1
        tkind = jdata["content"]["open_type"]
        if tkind=="" or tkind is None:
            continue
        if tkind in anay:
            anay[tkind]=anay[tkind]+1
        else:
            anay[tkind]=1
    print("totally %d data" % cnt)
    file2= open("platform.csv","w")
    for i in anay.keys():
        file2.write(str(i)+","+str(anay[i])+"\n")

platform_anay()