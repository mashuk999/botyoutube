from django.http import HttpResponse, JsonResponse
import requests


def uploadvideotoheroku(filepath,YTtitle):
    try:
        print(filepath)
        filepath = str(filepath)
        # filepath = filepath.replace(' ','\ ')
        filepath="final.mp4"
        print(filepath)
        myurl = 'https://youtuberestframework.eu-gb.cf.appdomain.cloud/videouploadwithcloudinary/'
        video = {'video': open(filepath, 'rb')}
        title={'title':YTtitle}
        getdata = requests.post(myurl,data=title, files=video)
        print(getdata.text)  
        # r=requests.post('http://lit-sierra-15246.herokuapp.com/videoupload/')
    except Exception as e:
        print(e)