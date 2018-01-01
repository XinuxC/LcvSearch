#!/usr/bin/env python
# coding=utf8
# -*- coding: utf-8 -*-
# @File  : urls.py.py
# @Author: ChENMo
# @Contact:pishit2009@gmail.com
# @Date  : 2017/12/29
# @Desc  :

from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'search'
urlpatterns = [
    path('', TemplateView.as_view(template_name ='index.html'),name="index"),
    path('suggest', views.SearchSuggest.as_view(),name="suggest"),
    path('searchview', views.SearchView.as_view(),name="searchview"),
]
