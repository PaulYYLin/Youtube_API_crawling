import requests
import datetime
import sys
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# From GCP YT API Key (需上GCP申請API KEY)
youtube_api_key = "AIzaSyA4CFlvP9dPOGLnlzjTG8exycj4qeV65dY"
video_id = 'Mb0w8xiwGQw'  # key in video id from video url(根據所需影片添加id)


# get videoTitle & PublishedTime
api_url_video_inform = 'https://www.googleapis.com/youtube/v3/videos?id=' + \
    video_id+'&key='+youtube_api_key+'&part=snippet,statistics'
r2 = requests.get(api_url_video_inform)
data2 = r2.json()
video_title = data2['items'][0]['snippet']['title'].replace(" ","")
video_publishedTime = data2['items'][0]['snippet']['publishedAt']
commentCount = data2['items'][0]['statistics']['commentCount']

print("影片名稱:"+video_title+"影片上傳時間"+video_publishedTime,"評論數:"+commentCount)  # 確認影片資訊


format = pd.DataFrame({'Comments': [], 'likeCount': [],
                      'PublishedTime': [],'Replies':[]})  # build format


api_url_review = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId=" + \
    video_id+"&maxResults=100"+"&key="+youtube_api_key
r = requests.get(api_url_review)
data = r.json()

for i in range(len(data['items'])):
    tmp=[]
    try:
        for s in data['items'][i]['replies']['comments']:
            reply = s['snippet']['textOriginal']
            name = s['snippet']['authorDisplayName']
            tmp.append(name+": "+reply)
            
    except:
        time.sleep(0)
    tmp = "\n".join(tmp)
    
        
    format = format.append({'Comments': data['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'], 'likeCount': data['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'],'PublishedTime': data['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'],'Replies':tmp}, ignore_index=True)
next_page_token = data.get('nextPageToken', '')

for num in range(1,int(commentCount)//100+1):
    
    api_url_review2 = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId=" + \
        video_id+"&maxResults=100"+"&pageToken="+next_page_token+"&key="+youtube_api_key
    r3 = requests.get(api_url_review2)
    data3 = r3.json()
    for i in range(len(data3['items'])):
        tmp3=[]
        try:
            for s in data3['items'][i]['replies']['comments']:
                reply = s['snippet']['textOriginal']
                name = s['snippet']['authorDisplayName']
                tmp3.append(name+": "+reply)
                
        except:
            time.sleep(0)
        tmp3 = "\n".join(tmp3)
        

        format = format.append({'Comments': data3['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'], 'likeCount': data3['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'],'PublishedTime': data3['items'][i]['snippet']['topLevelComment']['snippet']['publishedAt'],'Replies':tmp3}, ignore_index=True)
        
#print(data3['items'])
#print(format)
file_name = re.sub('\W+','',video_title).replace("_",'')

format.to_csv(file_name+'.csv')
