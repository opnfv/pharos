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

from booking.views import *

urlpatterns = [
    url(r'^(?P<resource_id>[0-9]+)/$', BookingFormView.as_view(), name='create'),
    url(r'^(?P<resource_id>[0-9]+)/bookings_json/$', ResourceBookingsJSON.as_view(),
        name='bookings_json'),

    url(r'^detail/$', BookingView.as_view(), name='detail_prefix'),
    url(r'^detail/(?P<booking_id>[0-9]+)/$', BookingView.as_view(), name='detail'),
]
