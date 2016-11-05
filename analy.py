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
cnt=0
timeline=[]
for i in alldata:
    jdata=json.loads(i[0])
    ttime=jdata["content"]["date"]
    timeline.append(time.strftime(ttime))
    cnt=cnt+1
print("total %d data"%cnt)

file1=open("time.csv","w")
sorted(timeline)
yester=None
days=[]
#print(timeline[0][:10]+"11111")
days.append(["1",0])
pos=0
for  i in timeline:
    #print(i)
    tday=i[:10]
    if tday != yester:
        yester=tday
        pos=pos+1
        days.append([tday,1])
    else:
        days[pos][1]=days[pos][1]+1
print(days[1])
for i in days:
    print(i[0])
    file1.write(str(",")+str(i[0]))
file1.write("\n")
for i in days:
    print(i[1])
    file1.write(str(i[1])+",")
file1.close()

