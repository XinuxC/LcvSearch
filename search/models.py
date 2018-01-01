from django.db import models
from datetime import datetime
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Date, Nested, Boolean, analyzer, InnerObjectWrapper, Completion, Keyword, Text
# 解决suggest使用analyzer报错问题
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# Create your models here.
# 连接es服务
connections.create_connection(hosts=['localhost'])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class JobboleDoc(DocType):
    company = Text(analyzer="ik_smart")
    title = Text(analyzer="ik_max_word")
    salary = Text()
    job_tags = Text()
    job_desc = Text()
    suggest = Completion(analyzer=ik_analyzer)

    class Meta:
        index = 'jobbole'
        doc_type = 'articles'


if __name__ == '__main__':
    JobboleDoc.init()
