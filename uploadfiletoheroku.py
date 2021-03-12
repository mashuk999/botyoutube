from django.http import HttpResponse, JsonResponse
import requests


def uploadvideotoheroku(filepath,YTtitle):
    try:
        print(filepath)
        myurl = 'http:/ytserver.eu-gb.cf.appdomain.cloud/videoupload/'
        video = {'video': open(filepath, 'rb')}
        title={'title':YTtitle}
        getdata = requests.post(myurl,data=title, files=video)
        print(getdata.text)  
        # r=requests.post('http://lit-sierra-15246.herokuapp.com/videoupload/')
    except Exception as e:
        print(e)
