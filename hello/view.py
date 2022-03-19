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

def showResult(request):
    # data = {
    # "语音识别结果" : "it was printed in monterey",
    # "实体信息": [{"offset":"18","mention":"monterey","kb_id": "Q487315",
    # "wikidata_url":"https://www.wikidata.org/wiki/Q487315",
    # "description":"city in California, United States"}]
    # }

    # data = {"mention_data": [{"offset": "46", "mention": "monsanto", "kb_id": "Q207983",
    # "wikidata_url": "https://www.wikidata.org/wiki/Q207983", 
    # "description": "American multinational agricultural biotechnology, seed, and agrochemical company"}], 
    # "text": "BrittaRiley _ 2011X 1 BrittaRiley _ 2011X 183.53 197.88 < NA > and i really wanted it to be an"
    # "open project because hydroponics is one of the fastest growing areas of patenting in the united states"
    # "right now and could possibly become another area like monsanto where we have a lot of corporate"
    # }

    # data = {"mention_data": [{"offset": "36", "mention": "strawberries", "kb_id": "Q745", 
    # "wikidata_url": "https://www.wikidata.org/wiki/Q745", "description": "genus of plants"}], 
    # "text": "BrittaRiley _ 2011X 1 BrittaRiley _ 2011X 289.38 303.82 < NA > tony in chicago has been taking " 
    # "on growing experiments like lots of other window farmers and he's been able to get his strawberries to "
    # "fruit for nine months of the year in low light conditions by simply changing out the organic nutrients"
    # }

    # data = {"mention_data": [{"offset": "37", "mention": "new york city", "kb_id": "Q60",
    #  "wikidata_url": "https://www.wikidata.org/wiki/Q60", 
    #  "description": "largest city in the United States"}], 
    #  "text": "BrittaRiley _ 2011X 1 BrittaRiley _ 2011X 210.87 218.77 < NA > the first few "
    #  "systems that we created they kind of worked we were actually able to grow about a salad "
    #  "a week in a typical new york city apartment window < unk >"}

    data = {"mention_data": [{"offset": "16", "mention": "eleen", "kb_id": "NULL", 
        "wikidata_url": "NULL", "description": "NULL"}], 
        "text": "BrittaRiley _ 2011X 1 BrittaRiley _ 2011X 395.62 403.11 < NA > but i think"
        " that eleen expresses best what we really get out of this which is the actual joy of "
        "collaboration"}
    
    json_str = simplejson.dumps(data, ensure_ascii=False)
    json_dict = simplejson.loads(json_str)

    info_list=json_dict["mention_data"]
    info_dict=info_list[0]
    kb_id=info_dict["kb_id"]

    # if the entity can be found in WikiData, fetch the main image
    if kb_id != "NULL":
        prepareImage(kb_id)
        print("Download complete.")

    return render(request,'result.html',{"json_dict":json_dict,"kb_id":kb_id})

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
            print("finish")
            self.finish = True
            return None
        except Exception as e:
            print(e)
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
            print(i, str(datetime.now())+"\n")
            sleep(1)
        #start them
        for t in threadslist:
            t.start()
        #keep checking every 3 secs to see whether the procedure needs to be ended
        while True:
            sleep(3)
            if self.finish:
                break
        


    




        # save the image to our target directory
        # threadslist=[]
        # f = open(filepath,'wb')
        # for i in range(0,5):
        #     newthread=threading.Thread(target=download,args=(threadslist,kb_id,f))
        #     # newthread.start()
        #     threadslist.append(newthread)
        #     print(i, str(datetime.now())+"\n")
        #     sleep(1)
        # for t in threadslist:
        #     t.start()



# WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

# def get_wiki_image(search_term):
#     try:
#         result = wikipedia.search(search_term, results = 1)
#         wikipedia.set_lang('en')
#         wkpage = wikipedia.WikipediaPage(title = result[0])
#         title = wkpage.title
#         response  = requests.get(WIKI_REQUEST+title)
#         json_data = simplejson.loads(response.text)
#         img_link = list(json_data['query']['pages'].values())[0]['original']['source']
#         return img_link        
#     except:
#         return 0
