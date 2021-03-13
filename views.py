import os 
from processArticle import *
from makeVideos import *
from wsgiref.util import FileWrapper
from uploadToYT import *
import os
from django.conf import settings
import shutil
from gtts import gTTS
import random
import settings
import requests, json, datetime 
from uploadfiletoheroku import *



def checktime():
    # fetchdata=requests.get('http:/ytserver.eu-gb.cf.appdomain.cloud/entertainx/')
    fetchdata=requests.get('https://ytserver.eu-gb.cf.appdomain.cloud/entertainx/')
    data=fetchdata.json()
    # print(data['nextrandom'])
    nextran= datetime.datetime.strptime(data['nextrandom'],"%Y-%m-%dT%H:%M:%SZ")
    print(nextran)
    # print(nextran)
    # print(type(nextran))
    # print(datetime.now)
    datime=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(datime)
    dateee=datetime.datetime.strptime(datime,"%Y-%m-%d %H:%M:%S")

    if nextran < dateee:
       print("We will post video")
       requestVideo()
    else:
        print("We will wait for minutes since it is time error")




def requestVideo():
    try:       
        r=requests.get('https://ytserver.eu-gb.cf.appdomain.cloud/gettitle/')
        print(r)

        title=(r.json()['title'])
        YTtitle=(r.json()['Ytitle'])
        content=(r.json()['content'])
        summary=(r.json()['summary'])
        if title == 0 or title is None or content is None or content == '':
            print("Content or title is either blank or incorrect")
            exit()
        
        # #Replacing space with hiphens to resolve filepath issue in linux
        # if title is not None:
        #     title.replace(' ','-')

        newYTtitle = YTtitle
        # newYTtitle = newYTtitle.replace(' ','-')
        p = makeVideo(newYTtitle+' hd',content)

        if p =='GTTS ERR':
            shutil.rmtree(os.path.join(settings.BASE_DIR, r"dataset"))
            return HttpResponse('GTTS ERR')

        os.chdir(os.path.join(settings.BASE_DIR,''))

        credit = '''\nWe take DMCA very seriously. All the images are from Bing Images.Since all the contents are not moderated so If anyway we hurt anyone sentiment, send us a request with valid proof.
        '''
        keywords = ','.join(str(YTtitle).split())

        print(YTtitle)

        command = 'python ./bott/uploadToYT.py --file="'+str(p)+'" --title="'+YTtitle+'" --description="'+(summary+'\n'+credit)+'" --keywords="'+keywords+',hour news,news" --category="24" --privacyStatus="public" --noauth_local_webserver ' 
        uploadvideotoheroku(p,YTtitle)
        
        # os.system(command) #comment this to stop uploading to youtube
        # shutil.rmtree(os.path.join(settings.BASE_DIR, r"dataset")) # comment this to stop removing the file from system
        print('Success')


    except Exception as e:
        print('views function')
        print(e)

    




checktime()