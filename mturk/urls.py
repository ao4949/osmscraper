#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.http import HttpResponse
from api import views

urlpatterns = patterns('',
	# Category
    url(r'.*/?$', 'mturk.views.test'),
)