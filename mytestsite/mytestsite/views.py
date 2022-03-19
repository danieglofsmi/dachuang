from datetime import datetime
from time import sleep
from django.shortcuts import render
from wikidata.client import Client
import json as simplejson
import ssl
import urllib.request
import os
import threading

#防止10060错误
ssl._create_default_https_context = ssl._create_unverified_context

def index_out(request):

    data = {"mention_data": [{"offset": "19", "mention": "nasa", "kb_id": "Q23548", 
    "wikidata_url": "https://www.wikidata.org/wiki/Q23548", 
    "description": "independent agency of the United States Federal Government"}], 
    "text": "BrittaRiley _ 2011X 1 BrittaRiley _ 2011X 261.89 271.48 < NA > what we ' re doing"
    " is what nasa or a large corporation would call r & d < unk > or research and development "
    "but what we call it is r"}
    
    json_str = simplejson.dumps(data, ensure_ascii=False)
    json_dict = simplejson.loads(json_str)

    info_list=json_dict["mention_data"]
    info_dict=info_list[0]
    kb_id=info_dict["kb_id"]

    # if the entity can be found in WikiData, fetch the main image
    if kb_id != "NULL":
        prepareImage(kb_id)

    return render(request,'output.html',{"json_dict":json_dict,"kb_id":kb_id})


def prepareImage(kb_id):
    filepath = 'static\images\\' + kb_id + '.jpg'
    if os.path.isfile(filepath):
        return None
    else:
        downloadingThread = myThreadClass()
        downloadingThread.start(filepath,kb_id)


class myThreadClass():
    def __init__(self):
        self.finish = False

    def download(self,image_url,f):
        print("start: "+ str(datetime.now())+"\n")
        try:
            f.write(urllib.request.urlopen(image_url).read())
            f.close()  
            self.finish = True
            return None
        except Exception as e:
            # print(e)
            return None

    def start(self,filepath,kb_id):
        # list for threads
        threadslist=[]
        # get the url of the main image
        client = Client()  
        entity = client.get(kb_id)
        image_prop = client.get('P18')
        image = entity[image_prop]
        image_url = image.image_url
        # create the file
        f = open(filepath,'wb')
        # create multiple threads
        for i in range(0,5):
            newthread=threading.Thread(target=self.download,args=(image_url,f))
            threadslist.append(newthread)
            sleep(1)
        #start them
        for t in threadslist:
            t.start()
        #keep checking every 1 sec to see whether the procedure needs to be ended
        while True:
            sleep(1)
            if self.finish:
                break