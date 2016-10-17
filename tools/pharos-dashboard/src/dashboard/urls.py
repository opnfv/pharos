##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


"""pharos_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from dashboard.views import *

urlpatterns = [
    url(r'^ci_pods/$', CIPodsView.as_view(), name='ci_pods'),
    url(r'^dev_pods/$', DevelopmentPodsView.as_view(), name='dev_pods'),
    url(r'^jenkins_slaves/$', JenkinsSlavesView.as_view(), name='jenkins_slaves'),
    url(r'^resource/all/$', LabOwnerView.as_view(), name='resources'),
    url(r'^resource/(?P<resource_id>[0-9]+)/$', ResourceView.as_view(), name='resource'),
    url(r'^resource/(?P<resource_id>[0-9]+)/booking_utilization/(?P<weeks>-?\d+)/$',
        BookingUtilizationJSON.as_view(), name='booking_utilization'),
    url(r'^resource/(?P<resource_id>[0-9]+)/jenkins_utilization/(?P<weeks>-?\d+)/$',
        JenkinsUtilizationJSON.as_view(), name='jenkins_utilization'),
    url(r'^$', DevelopmentPodsView.as_view(), name="index"),
]
