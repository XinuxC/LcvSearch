from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View
from search.models import JobboleDoc
from django.http import HttpResponse
import json
from elasticsearch import Elasticsearch

client = Elasticsearch(hosts=['127.0.0.1'])


# Create your views here.
class SearchSuggest(View):
    def get(self,request):
        key_word = request.GET.get('s', '')
        re_datas = []
        if key_word:
            s = JobboleDoc.search()
            s = s.suggest('my_suggest', key_word, completion={
                "field": "suggest",
                "fuzzy": {
                    "fuzziness": 2
                },
                "size": 5
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_datas.append(source['title'])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    def get(self,request):
        key_word = request.GET.get('q', '')
        start_time = datetime.now()
        response = client.search(
            index='jobbole',
            body={
                "query": {
                    "multi_match": {
                        "query": key_word,
                        "fields":['title', 'category']
                    }
                },
                "highlight": {  # 结果高亮显示
                    "pre_tags": ["<span class='KeyWord'>"],
                    "post_tags": ["</span>"],
                    "fields": {
                        "title": {},
                        "category": {}
                    }
                },
                "from": 0,
                "size": 10
            }
        )
        end_time = datetime.now()
        seconds = (start_time - end_time).total_seconds()
        hits_num = response['hits']['total']
        hit_list = []
        for hit in response['hits']['hits']:
            hit_data = {}
            if 'title' in hit['highlight']:
                hit_data['title'] = ''.join(hit['highlight']['title'])
            else:
                hit_data['title'] = hit['_source']['title']
            if 'category' in hit['highlight']:
                hit_data['category'] = ''.join(hit['highlight']['category'])
            else:
                hit_data['category'] = hit['_source']['category']
            hit_data['link'] = hit['_source']['link']
            hit_data['score'] = hit['_score']
            hit_list.append(hit_data)

        return render(request, 'search/result.html', {'hit_list': hit_list,'hits_num': hits_num, 'key_word': key_word})
