from dashboard.views.booking import BookingCalendarView, ResourceBookingsView, DeleteBooking, \
    DeleteRepeatBooking, BookingCreateView, BookingChangeView, RepeatBookingCreateView
from dashboard.views.registration import DashboardRegistrationView, AccountSettingsView
from dashboard.views.table_views import CIPodsView, DevelopmentPodsView, JenkinsSlavesView
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # registration
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/register/', DashboardRegistrationView.as_view(), name='registration'),
    url(r'^accounts/settings/', AccountSettingsView.as_view(), name='account_settings'),

    # Index
    url(r'^index/$', CIPodsView.as_view(), name='index'),
    url(r'^index/$', CIPodsView.as_view(), name='index'),
    url(r'^$', CIPodsView.as_view(), name=""),

    # Tables
    url(r'^ci_pods/$', CIPodsView.as_view(), name='ci_pods'),
    url(r'^dev_pods/$', DevelopmentPodsView.as_view(), name='dev_pods'),
    url(r'^jenkins_slaves/$', JenkinsSlavesView.as_view(), name='jenkins_slaves'),

    # Booking Calendar
    url(r'^resource/(?P<resource_id>[0-9]+)/booking/$',
        BookingCalendarView.as_view(), name='booking_calendar'),

    url(r'^resource/(?P<resource_id>[0-9]+)/booking/create',
        BookingCreateView.as_view(), name='booking_create'),
    url(r'^resource/(?P<resource_id>[0-9]+)/repeat_booking/create',
        RepeatBookingCreateView.as_view(), name='repeat_booking_create'),

    url(r'^resource/(?P<resource_id>[0-9]+)/booking/(?P<booking_id>[0-9]+)/change',
        BookingChangeView.as_view(), name='booking_change'),

    url(r'^^resource/(?P<resource_id>[0-9]+)/booking/(?P<booking_id>[0-9]+)/delete$',
        DeleteBooking.as_view(), name='delete_booking'),
    url(r'^^resource/(?P<resource_id>[0-9]+)/repeat_booking/(?P<repeat_booking_id>[0-9]+)/delete$',
        DeleteRepeatBooking.as_view(), name='delete_repeat_booking'),

    # AJAX urls
    url(r'^resource/(?P<resource_id>[0-9]+)/bookings/$',
        ResourceBookingsView.as_view(), name='resource_bookings'),
]
