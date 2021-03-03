import os 
# from django.http import HttpResponse
# from django.conf import settings
from processArticle import *
from makeVideos import *
from wsgiref.util import FileWrapper
from uploadToYT import *
import os
from django.conf import settings
import shutil
import datetime
from gtts import gTTS
import datetime,random
import settings






def requestVideo():
    # objTime =/ models.uploadedVideos.objects.latest('id')

    # if objTime is None or objTime.nextRandom is None or objTime.nextRandom > datetime.datetime.now(datetime.timezone.utc):
    #     return HttpResponse('Time Error')
        
    title,summary,content,YTtitle = findArticle()

    title='google'

    if title == 0:
        return HttpResponse('No more Unique')


    p = makeVideo(YTtitle[:240]+' hd',content)

    if p =='GTTS ERR':
        shutil.rmtree(os.path.join(settings.BASE_DIR, r"dataset"))
        return HttpResponse('GTTS ERR')

    os.chdir(os.path.join(settings.BASE_DIR,''))

    credit = '''\nWe take DMCA very seriously. All the images are from Bing Images.Since all the contents are not moderated so If anyway we hurt anyone sentiment, send us an request with valid proof.
    '''
    keywords = ','.join(str(YTtitle).split())

    print(YTtitle)


    command = 'python ./bott/uploadToYT.py --file="'+str(p)+'" --title="'+YTtitle+'" --description="'+(summary+'\n'+credit)+'" --keywords="'+keywords+',hour news,news" --category="25" --privacyStatus="public" --noauth_local_webserver '
    os.system(command)
    # os.system(command) #comment this to stop uploading to youtube
    # shutil.rmtree(os.path.join(settings.BASE_DIR, r"dataset")) # comment this to stop removing the file from system
    # obj = models.uploadedVideos(title = title,
    # nextRandom=(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=random.randrange(245, 350))))
    print('Success')






requestVideo()