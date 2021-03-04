from pathlib import Path
import os
import sys
import urllib.request
import urllib
import imghdr
import posixpath
import re
import settings


'''
Python api to download image form Bing.
Author: Guru Prasad (g.gaurav541@gmail.com)
'''


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
        try:
            request = urllib.request.Request(link, None, self.headers)
            image = urllib.request.urlopen(request, timeout=self.timeout).read()
            if not imghdr.what(None, image):
                print('[Error]Invalid image, not saving {}\n'.format(link))
                raise
            with open(file_path, 'wb') as f:
                f.write(image)
        except:
            print('bing saveimage')

    def download_image(self, link):
        try:
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
        except:
            print('bing downlaodimage')

    def run(self):
        try:
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
        except:
            print('bing run')
