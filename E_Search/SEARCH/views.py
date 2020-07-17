
import json
from django.shortcuts import render
from django.views.generic.base import View
from SEARCH.models import ArticleType

from django.http import HttpResponse
from elasticsearch import Elasticsearch
from datetime import datetime

client = Elasticsearch(hosts=["127.0.0.1"])

s = ArticleType.search()
s = s.suggest(
    'my_suggest',
    "九州",
    completion={
        "field": "suggest",
        "fuzzy": {
            "fuzziness": 2
        },
        "size": 10
    }
)
# 调用 execute_suggest 方法
# suggestions = s.execute_suggest()
suggestions = s.execute().to_dict()
re_datas = []
# result = suggestions["suggest"]["my_suggest"][0]["options"]
for match in suggestions["suggest"]["my_suggest"][0]["options"]:
    source = match["_source"]
    re_datas.append(source["project_name"])
print("#" * 50)
print(re_datas)
print("#" * 50)



class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s','')
        re_datas = []
        if key_words:
            s = ArticleType.search()
            s = s.suggest(
                'my_suggest',
                key_words,
                completion={
                    "field":"suggest",
                    "fuzzy":{
                        "fuzziness":2
                        },
                "size": 10
                }
            )
            # 调用 execute_suggest 方法
            # suggestions = s.execute_suggest()
            suggestions = s.execute()
            for match in suggestions["suggest"]["my_suggest"][0]["options"]:
                source = match["_source"]
                re_datas.append(source["project_name"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    def get(self,request):
        key_words = request.GET.get('q','')
        page = request.GET.get('p','1')
        try:
            page = int(page)
        except:
            page = 1

        start_time = datetime.now()
        response = client.search(
            index = "luanyushou",
            body = {
                "query":{
                    "multi_match":{
                        "query":key_words,
                        "fields":["project_name","position","position_enviroment"]
                    }
                },
                "from":(page-1)*10,
                "size":10,
                "highlight":{
                    "pre_tags" : ["<span class='keyWord'>"],
                    "post_tags":["</span>"],
                    "fields":{
                        "project_name":{},
                        "position":{},
                        "position_enviroment":{},
                    }
                }
            }
        )
        end_time = datetime.now()
        last_seconds = (end_time-start_time).total_seconds()

        total_nums = response["hits"]["total"]["value"]
        print("=" * 50)
        print(response)
        print("=" * 50)

        if (page%10) > 0:
            page_nums = total_nums/10 +1
        else:
            page_nums = total_nums/10
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "project_name" in hit["highlight"]:
                hit_dict["project_name"] =''.join(hit["highlight"]["project_name"])
            else:
                hit_dict['project_name'] =''.join(hit["_source"]["project_name"])
            if "position" in hit["highlight"]:
                hit_dict["position"] =''.join(hit["highlight"]["position"][:200])
            else:
                hit_dict["position"] =''.join(hit["_source"]["position"][:200])
            if "position_enviroment" in hit["highlight"]:
                hit_dict["position_enviroment"] =''.join(hit["highlight"]["position_enviroment"])
            else:
                hit_dict["position_enviroment"] =''.join(hit["_source"]["position_enviroment"])

            try:
                hit_dict["presale"] = hit["_source"]["presale"]
            except:
                hit_dict["presale"] = ""
            try:
                hit_dict["presale_area"] = hit["_source"]["presale_area"]
            except:
                hit_dict["presale_area"] = ""
            try:
                hit_dict["presale_num"] = hit["_source"]["presale_num"]
            except:
                hit_dict["presale_num"] = ""
            try:
                hit_dict["permit_date"] = hit["_source"]["permit_date"]
            except:
                hit_dict["permit_date"] = ""
            try:
                hit_dict["constrution_designer"] = hit["_source"]["constrution_designer"]
            except:
                hit_dict["constrution_designer"] = ""
            try:
                hit_dict["green_designer"] = hit["_source"]["green_designer"]
            except:
                hit_dict["green_designer"] = ""
            try:
                hit_dict["land_number"] = hit["_source"]["land_number"]
            except:
                hit_dict["land_number"] = ""
            try:
                hit_dict["invest_permit"] = hit["_source"]["invest_permit"]
            except:
                hit_dict["invest_permit"] = ""
                # hit_dict["book_size"] = hit["_source"]["book_size"]
            # hit_dict["kindle_name"] = hit["_source"]["kindle_name"]
            # hit_dict["kindle_author"] = hit["_source"]["kindle_author"]
            # hit_dict["kindle_score"] = hit["_source"]["kindle_score"]
            # hit_dict["kindle_intro"] = hit["_source"]["kindle_intro"]
            # hit_dict["kindle_url"] = hit["_source"]["kindle_url"]
            # hit_dict["kindle_type"] = hit["_source"]["kindle_type"]
            # hit_dict["kindle_id"] = hit["_source"]["kindle_id"]

            hit_list.append(hit_dict)

        return render(request,"result.html",{"page":page,
                                             "all_hits":hit_list,
                                             "key_words":key_words,
                                             "total_nums":total_nums,
                                             "page_nums":page_nums,
                                             "last_seconds":last_seconds,
                                             })

