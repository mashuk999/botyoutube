FROM wlserver1/ytupload:latest
COPY entrypoint.sh /entrypoint.sh
COPY bing.py /bing.py
COPY downloader.py /downloader.py
COPY makeVideos.py /makeVideos.py
COPY settings.py /settings.py
COPY upload.sh /upload.sh
COPY uploadfiletoheroku.py /uploadfiletoheroku.py
COPY views.py /views.py
ENTRYPOINT ["/entrypoint.sh"]