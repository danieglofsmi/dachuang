from django.shortcuts import render
import json as simplejson
 
def index_out(request):
    data = {
    'text' : 'it was printed in monterey',
    'mention_data':[{'offset':'18','mention':'monterey','wikidata_url':'https://www.wikidata.org/wiki/Q487315','description':'city in California, United States'}]
    }
    simplejson_str = simplejson.dumps(data, ensure_ascii=False)
    simplejson_list = simplejson.loads(simplejson_str, encoding='utf-8', strict=False)

    return render(request,'output.html',{"json_dict":simplejson_list})

