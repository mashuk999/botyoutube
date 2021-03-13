from downloader import *
import os 
import cv2 
from PIL import Image 
from django.conf import settings
import urllib.request
from gtts import gTTS,tts
import shutil
from moviepy.editor import AudioFileClip, VideoFileClip,CompositeAudioClip
import settings





def makeAudio(name,content):
    try:
        try:
            os.chdir(os.path.join(settings.BASE_DIR, r"dataset/"+name))
            ttsG = gTTS(content, lang='hi')
            ttsG.save('audio.mp3')
        except tts.gTTSError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False
        return True
    except Exception as e: 
        print('m.v. makeaudio')
        print(e)

def downloadImages(title):
    try:
        # title.replace(' ','-')
        os.chdir(os.path.join(settings.BASE_DIR,''))
        download(title, limit=10,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=300)
    except:
        print('m.v. downloadimages')


def makeVideo(name,content):
    try:
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

        print('Video Generated')

        addAudioToVideo(name)
        
        return os.path.join(settings.BASE_DIR, r"dataset/"+name+r'/'+name+r'.mp4')
    except Exception as e:
        print(e)


# Video Generating function 
def generate_video(name):
    try:
        image_folder = '.' # make sure to use your folder 
        video_name = 'mygeneratedvideo.mp4'
        os.chdir(os.path.join(settings.BASE_DIR, r"dataset/"+name))
        print(os.listdir())
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
        cv2.destroyAllWindows()
        video.release() # releasing the video generated 
        print(os.listdir())
    except Exception as e:
        print('m.v. generatevideo')
        print(e)
    
        
def addAudioToVideo(name):
    try:
        os.chdir(os.path.join(settings.BASE_DIR, r"dataset/"+name))
        print(os.listdir())
        audiofile = AudioFileClip('audio.mp3')
        videoclip = VideoFileClip("mygeneratedvideo.mp4")
        #new_audioclip = CompositeAudioClip([audiofile])
        videoclip = videoclip.set_audio(audiofile)
        # videoclip.audio = new_audioclip
        videoclip = videoclip.subclip(0, audiofile.duration)
        videoclip = videoclip.speedx(factor=1.1)
        # videoclip = videoclip.fx(speedx, 1.3)
        os.chdir(os.path.join(settings.BASE_DIR, ""))
        videoclip.write_videofile("final"+".mp4")
    except Exception as e:
        print('addaudioto video m.v.')
        print(e)