import os
import scrapy
from celeb500k.items import Celeb500KItem
from PIL import Image
from io import BytesIO
import uuid
import json
import pickle

class Celeb500k(scrapy.Spider):
    name = 'celeb500k'
    
    def extract_urls(self, txt):
        try:
            pos1=0
            pos2=-6
            data = open(txt, 'rb')
            for line in data:
                line = line.decode('utf-8')
            urls = []
            while(pos1 != -1 and line!=[]):
                line = line[pos2+6:]
                try:
                    pos1 = line.index("\"ou\"")
                except ValueError:
                    break
                pos2 = line.index("\"ow\"")
                urls.append(line[pos1+6:pos2-2])
            return urls
        except:
            return []

    def start_requests(self):
        dirpath = os.getcwd()
        root_dir = os.path.join(dirpath, 'data/urls')
        folders = os.listdir(root_dir)
        out_dir = os.path.join(dirpath, 'data/images')
        self.downloaded_urls = set()
        self.redirect_map = {}
        for folder in folders:
            out_file = os.path.join(out_dir, folder+".jl")
            self.redirect_file = os.path.join(out_dir, folder+".pkl")
            if os.path.exists(self.redirect_file):
                self.redirect_map = pickle.load(open(self.redirect_file, "rb"))
            if os.path.exists(out_file):
                with open(out_file, "r") as f:
                    for line in f.readlines():
                        self.downloaded_urls.add(str(json.loads(line.strip())["url"]))
            current_dir = os.path.join(root_dir, folder)
            for filename in os.listdir(current_dir):
                full_path = os.path.join(current_dir, filename)
                urls = self.extract_urls(full_path)
                if len(urls) == 0:
                    continue
                current_out_dir = os.path.join(out_dir, folder, filename[:-6])
                for url in urls:
                    request = scrapy.Request(url, callback=self.parse)
                    url = request.url
                    if url in self.downloaded_urls or self.redirect_map.get(url, "") in self.downloaded_urls:
                        print("SKIP")
                        continue
                    request.meta['out_dir'] = current_out_dir
                    request.meta['log_file'] = out_file
                    request.meta['origin_url'] = url
                    yield request

    def parse(self, response):
        if response.request.url != response.request.meta['origin_url']:
            self.redirect_map[response.request.meta['origin_url']] = response.request.url
            with open(self.redirect_file, "wb") as f:
                pickle.dump(self.redirect_map, f)
        if response.request.url in self.downloaded_urls:
            return
        image = Image.open(BytesIO(response.body))
        
        out_dir = response.request.meta['out_dir']
        os.makedirs(out_dir, exist_ok=True)
        
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode == 'P':
            image = image.convert("RGBA")
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        image_path = os.path.join(out_dir, str(uuid.uuid4())+".jpg")
        image.save(image_path)
        with open(response.request.meta['log_file'], 'a+') as f:
            f.write(json.dumps({'image_dir': out_dir, 'url': response.request.url, 'name': image_path}) + "\n")    
                