from pathlib import Path
import os
import sys
import urllib.request
import urllib
import imghdr
import posixpath
import re
import http.client
import httplib2
import random
import sys
import time
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import urllib.request
import xmltodict
from bs4 import BeautifulSoup
import cv2 
from PIL import Image 
# from django.conf import settings
import urllib.request
from gtts import gTTS,tts
import shutil
from moviepy.editor import AudioFileClip, VideoFileClip,CompositeAudioClip
# import os 
# from django.http import HttpResponse
# from django.conf import settings
from wsgiref.util import FileWrapper
# from . import uploadToYT
# from django.conf import settings
import shutil
import datetime
from gtts import gTTS
import datetime,random
from py_bing_search import PyBingWebSearch









def requestVideo(request):
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


    command = 'python uploadToYT.py --file="'+str(p)+'" --title="'+YTtitle+'" --description="'+(summary+'\n'+credit)+'" --keywords="'+keywords+',hour news,news" --category="25" --privacyStatus="public" --noauth_local_webserver '
    os.system(command) #comment this to stop uploading to youtube
    # shutil.rmtree(os.path.join(settings.BASE_DIR, r"dataset")) # comment this to stop removing the file from system
    obj = models.uploadedVideos(title = title,
    nextRandom=(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=random.randrange(245, 350))))
    obj.save()
    return HttpResponse('Success')



def findArticle():
    
    xmlFormat = getLatestXML()
    
    jsonFormat = (xmltodict.parse(xmlFormat))['rss']['channel']['item']

    jsonFormat = getUniqueArticle(jsonFormat)

    if jsonFormat is None:
        return 0,0,0,0

    url = jsonFormat['guid']['#text']
    
    web_page = getArticleWebpage(url)
    
    content = scrapArticle(web_page)
    YTtitle = getYoutubeTitle(url)

    

    return jsonFormat['title'], jsonFormat['description'], content, YTtitle

def getUniqueArticle(jsonFormat):
    for item in jsonFormat:
        if len(getYoutubeTitle(item['guid']['#text'])) <= 100:
            try:
                obj = models.uploadedVideos.objects.get(title=item['title'])
            except models.uploadedVideos.DoesNotExist:
                return item
    return None

def getLatestXML():

    req = urllib.request.Request(
    'https://www.amarujala.com/rss/etawah.xml',
    data=None,

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    }
    )

    return urllib.request.urlopen(req)

def getArticleWebpage(url):
    req = urllib.request.Request(
    url, 
    data=None, 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    }
    )

    return urllib.request.urlopen(req)

def scrapArticle(web_page):
    soup = BeautifulSoup(web_page, 'html.parser')
    content =  soup.find("div", {"class": "article-desc ul_styling",})
    contentn = content.find("div", {"class": "article-desc ul_styling",})
    if contentn is not None:
        content = contentn

    for divs in content.findAll("div"):
        divs.extract()
    for divs in content.findAll("blockquote"):
        divs.extract()

    return content.get_text()

def getYoutubeTitle(s):
    s = s.split('/')[-1]
    s = s.replace('-',' ')
    return str(re.sub(r"[A-Za-z]+('[A-Za-z]+)?",lambda mo: mo.group(0).capitalize(),s))




def makeAudio(name,content):
    try:
        os.chdir(os.path.join(settings.BASE_DIR, r"dataset/"+name))
        ttsG = gTTS(content, lang='hi')
        ttsG.save('audio.mp3')
    except tts.gTTSError as e:
        print(e)
        return False
    return True

def downloadImages(title):
    os.chdir(os.path.join(settings.BASE_DIR,''))
    download(title, limit=10,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=300)

def makeVideo(name,content):
    print(os.path.isdir(os.path.join(settings.BASE_DIR, r"dataset/"+name)))
    if os.path.isdir(os.path.join(settings.BASE_DIR, r"dataset/"+name)):
        shutil.rmtree(os.path.join(settings.BASE_DIR, r"dataset/"+name))
    downloadImages(name)
    status = makeAudio(name,content)
    if not status:
        return 'GTTS ERR'
       
    print(os.getcwd()) 

    os.chdir(os.path.join(settings.BASE_DIR, r"dataset/"+name)) 
    path = os.path.join(settings.BASE_DIR, r"dataset/"+name)

    mean_height = 720
    mean_width = 1280

    num_of_images = len(os.listdir('.')) 

    # for file in os.listdir('.'): 
    #     if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
    #         im = Image.open(os.path.join(path, file)) 
    #         width, height = im.size 
    #         mean_width += width 
    #         mean_height += height 

    # mean_width = int(mean_width / num_of_images) 
    # mean_height = int(mean_height / num_of_images) 

    for file in os.listdir('.'): 
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"): 
            # opening image using PIL Image 
            im = Image.open(os.path.join(path, file)).convert('RGB')

            # im.size includes the height and width of image 
            width, height = im.size 
            print(width, height) 

            # resizing 
            imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS) 
            imResize.save( file, 'JPEG', quality = 95) # setting quality 

    generate_video(name) 

    addAudioToVideo(name)
    
    return os.path.join(settings.BASE_DIR, r"dataset/"+name+r'/'+name+r'.mp4')


# Video Generating function 
def generate_video(name):
    image_folder = '.' # make sure to use your folder 
    video_name = 'mygeneratedvideo.mp4'
    os.chdir(os.path.join(settings.BASE_DIR, r"dataset/"+name))
    images = [img for img in os.listdir(image_folder) 
    if img.endswith(".jpg") or img.endswith(".jpeg") or img.endswith("png")]
 

    frame = cv2.imread(os.path.join(image_folder, images[0])) 

    height, width, layers = frame.shape
    frameRate=10
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height)) 
    audioLength = AudioFileClip('audio.mp3').duration

    videoToLoop = audioLength
    if videoToLoop <1:
        videoToLoop = 1

    # Appending the images to the video one by one 
    while videoToLoop > 0:
        for image in images:
            for i in range(frameRate):
                video.write(cv2.imread(os.path.join(image_folder, image)))
        videoToLoop-=(frameRate*len(images))
    # Deallocating memories taken for window creation 
    #cv2.destroyAllWindows() 
    video.release() # releasing the video generated 

def addAudioToVideo(name):
    os.chdir(os.path.join(settings.BASE_DIR, r"dataset/"+name))
    audiofile = AudioFileClip('audio.mp3')
    videoclip = VideoFileClip("mygeneratedvideo.mp4")
    #new_audioclip = CompositeAudioClip([audiofile])
    videoclip = videoclip.set_audio(audiofile)
    # videoclip.audio = new_audioclip
    videoclip = videoclip.subclip(0, audiofile.duration)
    videoclip = videoclip.speedx(factor=1.3)
    # videoclip = videoclip.fx(speedx, 1.3)
    videoclip.write_videofile(name+".mp4")





class Bing:
    def __init__(self, query, limit, output_dir, adult, timeout, filters=''):
        self.download_count = 0
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filters = filters
        self.originalQuery = query

        assert type(limit) == int, "limit must be integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'}
        self.page_counter = 0

    def save_image(self, link, file_path):
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        if not imghdr.what(None, image):
            print('[Error]Invalid image, not saving {}\n'.format(link))
            raise
        with open(file_path, 'wb') as f:
            f.write(image)

    def download_image(self, link):
        self.download_count += 1

        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() not in ["jpe", "jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
                file_type = "jpg"

            # Download the image
            print("[%] Downloading Image #{} from {}".format(self.download_count, link))

            self.save_image(link, "{}/{}/{}/".format(os.getcwd(), self.output_dir, self.query) + "Image_{}.{}".format(
                str(self.download_count), file_type))
            print("[%] File Downloaded !\n")
        except Exception as e:
            self.download_count -= 1
            print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))

    def run(self):
        while self.download_count < self.limit:
            print('\n\n[!!]Indexing page: {}\n'.format(self.page_counter + 1))
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.originalQuery) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + self.filters
            request = urllib.request.Request(request_url, None, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf8')
            links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)

            if len(links) == 0 or self.download_count >= len(links) or self.page_counter > 100:
                self.originalQuery = ' '.join(self.originalQuery.split()[:-1])
                print('Query Changed due to no more unique result to ' + self.originalQuery)
                if self.originalQuery == '':
                    self.originalQuery = 'Breaking News'
                continue


            print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
            print("\n===============================================\n")

            for link in links:
                if self.download_count < self.limit:
                    self.download_image(link)
                else:
                    print("\n\n[%] Done. Downloaded {} images.".format(self.download_count))
                    print("\n===============================================\n")
                    break

            self.page_counter += 1






def download(query, limit=100, output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60):

    # engine = 'bing'
    if adult_filter_off:
        adult = 'off'
    else:
        adult = 'on'

    cwd = os.getcwd()
    image_dir = os.path.join(cwd, output_dir, query)

    if force_replace:
        if os.path.isdir(image_dir):
            shutil.rmtree(image_dir)

    # check directory and create if necessary
    try:
        if not os.path.isdir("{}/{}/".format(cwd, output_dir)):
            os.makedirs("{}/{}/".format(cwd, output_dir))
    except:
        pass
    if not os.path.isdir("{}/{}/{}".format(cwd, output_dir, query)):
        os.makedirs("{}/{}/{}".format(cwd, output_dir, query))

    bing = Bing(query, limit, output_dir, adult, timeout)
    bing.run()


if __name__ == '__main__':
    download('abitabh', limit=10, timeout='1')


'''
Python api to download image form Bing.
Author: Guru Prasad (g.gaurav541@gmail.com)
'''







#!/usr/bin/python

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
  http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_UPLOAD_SCOPE,
    access_type='offline',
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
  tags = None
  if options.keywords:
    tags = options.keywords.split(",")

  body=dict(
    snippet=dict(
      title=options.title,
      description=options.description,
      tags=tags,
      categoryId=options.category
    ),
    status=dict(
      privacyStatus=options.privacyStatus
    )
  )

  # Call the API's videos.insert method to create and upload the video.
  insert_request = youtube.videos().insert(
    part=",".join(list(body.keys())),
    body=body,
    # The chunksize parameter specifies the size of each chunk of data, in
    # bytes, that will be uploaded at a time. Set a higher value for
    # reliable connections as fewer chunks lead to faster uploads. Set a lower
    # value for better recovery on less reliable connections.
    #
    # Setting "chunksize" equal to -1 in the code below means that the entire
    # file will be uploaded in a single HTTP request. (If the upload fails,
    # it will still be retried where it left off.) This is usually a best
    # practice, but if you're using Python older than 2.6 or if you're
    # running on App Engine, you should set the chunksize to something like
    # 1024 * 1024 (1 megabyte).
    media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
  )

  resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print("Video id '%s' was successfully uploaded." % response['id'])
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)

if __name__ == '__main__':
  argparser.add_argument("--file", required=True, help="Video file to upload")
  argparser.add_argument("--title", help="Video title", default="Test Title")
  argparser.add_argument("--description", help="Video description",
    default="Test Description")
  argparser.add_argument("--category", default="22",
    help="Numeric video category. " +
      "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
  argparser.add_argument("--keywords", help="Video keywords, comma separated",
    default="")
  argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
    default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
  args = argparser.parse_args()

  if not os.path.exists(args.file):
    exit("Please specify a valid file using the --file= parameter.")

  youtube = get_authenticated_service(args)
  try:
    initialize_upload(youtube, args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))