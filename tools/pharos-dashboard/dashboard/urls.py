from dashboard.views.booking import BookingCalendarView, ResourceBookingsView, DeleteBookingView
from dashboard.views.table_views import CIPodsView, DevelopmentPodsView, JenkinsSlavesView
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    # registration
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),

    # Index
    url(r'^index/$', CIPodsView.as_view(), name='index'),
    url(r'^index/$', CIPodsView.as_view(), name='index'),
    url(r'^$', CIPodsView.as_view(), name=""),

    # Tables
    url(r'^ci_pods/$', CIPodsView.as_view(), name='ci_pods'),
    url(r'^dev_pods/$', DevelopmentPodsView.as_view(), name='dev_pods'),
    url(r'^jenkins_slaves/$', JenkinsSlavesView.as_view(), name='jenkins_slaves'),

    # Booking Calendar
    url(r'^booking_calendar/$', DevelopmentPodsView.as_view(),
        name='booking_calendar'),
    url(r'^booking_calendar/(?P<resource_id>[0-9]+)/$',
        BookingCalendarView.as_view(), name='booking_calendar'),
    url(r'^booking_calendar/(?P<resource_id>[0-9]+)/(?P<booking_id>[0-9]+)/$',
        BookingCalendarView.as_view(), name='booking_calendar'),

    # AJAX urls
    url(r'^resource/(?P<resource_id>[0-9]+)/bookings/$',
        ResourceBookingsView.as_view(), name='resource_bookings'),
    url(r'^booking/(?P<booking_id>[0-9]+)/delete$',
        DeleteBookingView.as_view(), name='delete_booking'),
]
