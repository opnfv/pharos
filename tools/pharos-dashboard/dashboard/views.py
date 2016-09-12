from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from booking.models import Booking
from dashboard.models import Resource
from jenkins.models import JenkinsSlave


class JenkinsSlavesView(TemplateView):
    template_name = "dashboard/jenkins_slaves.html"

    def get_context_data(self, **kwargs):
        slaves = JenkinsSlave.objects.all()
        context = super(JenkinsSlavesView, self).get_context_data(**kwargs)
        context.update({'title': "Jenkins Slaves", 'slaves': slaves})
        return context


class CIPodsView(TemplateView):
    template_name = "dashboard/ci_pods.html"

    def get_context_data(self, **kwargs):
        ci_pods = Resource.objects.filter(slave__ci_slave=True)
        context = super(CIPodsView, self).get_context_data(**kwargs)
        context.update({'title': "CI Pods", 'ci_pods': ci_pods})
        return context


class DevelopmentPodsView(TemplateView):
    template_name = "dashboard/dev_pods.html"

    def get_context_data(self, **kwargs):
        resources = Resource.objects.filter(slave__dev_pod=True)

        bookings = Booking.objects.filter(start__lte=timezone.now())
        bookings = bookings.filter(end__gt=timezone.now())

        dev_pods = []
        for resource in resources:
            booking_utilization = resource.get_booking_utilization(weeks=4)
            total = booking_utilization['booked_seconds'] + booking_utilization['available_seconds']
            try:
               utilization_percentage =  "%d%%" % (float(booking_utilization['booked_seconds']) /
                                                   total * 100)
            except (ValueError, ZeroDivisionError):
                return ""

            dev_pod = (resource, None, utilization_percentage)
            for booking in bookings:
                if booking.resource == resource:
                    dev_pod = (resource, booking, utilization_percentage)
            dev_pods.append(dev_pod)

        context = super(DevelopmentPodsView, self).get_context_data(**kwargs)
        context.update({'title': "Development Pods", 'dev_pods': dev_pods})
        return context


class ResourceView(TemplateView):
    template_name = "dashboard/resource.html"

    def get_context_data(self, **kwargs):
        resource = get_object_or_404(Resource, id=self.kwargs['resource_id'])
        utilization = resource.slave.get_utilization(timedelta(days=7))
        bookings = Booking.objects.filter(resource=resource, end__gt=timezone.now())
        context = super(ResourceView, self).get_context_data(**kwargs)
        context.update({'title': str(resource), 'resource': resource, 'utilization': utilization,
                        'bookings': bookings})
        return context


class LabOwnerView(TemplateView):
    template_name = "dashboard/resource_all.html"

    def get_context_data(self, **kwargs):
        resources = Resource.objects.filter(slave__dev_pod=True)
        pods = []
        for resource in resources:
            utilization = resource.slave.get_utilization(timedelta(days=7))
            bookings = Booking.objects.filter(resource=resource, end__gt=timezone.now())
            pods.append((resource, utilization, bookings))
        context = super(LabOwnerView, self).get_context_data(**kwargs)
        context.update({'title': "Overview", 'pods': pods})
        return context


class BookingUtilizationJSON(View):
    def get(self, request, *args, **kwargs):
        resource = get_object_or_404(Resource, id=kwargs['resource_id'])
        utilization = resource.get_booking_utilization(int(kwargs['weeks']))
        utilization = [
            {
                'label': 'Booked',
                'data': utilization['booked_seconds'],
                'color': '#d9534f'
            },
            {
                'label': 'Available',
                'data': utilization['available_seconds'],
                'color': '#5cb85c'
            },
        ]
        return JsonResponse({'data': utilization})


class JenkinsUtilizationJSON(View):
    def get(self, request, *args, **kwargs):
        resource = get_object_or_404(Resource, id=kwargs['resource_id'])
        weeks = int(kwargs['weeks'])
        utilization = resource.slave.get_utilization(timedelta(weeks=weeks))
        utilization = [
            {
                'label': 'Offline',
                'data': utilization['offline'],
                'color': '#d9534f'
            },
            {
                'label': 'Online',
                'data': utilization['online'],
                'color': '#5cb85c'
            },
            {
                'label': 'Idle',
                'data': utilization['idle'],
                'color': '#5bc0de'
            },
        ]
        return JsonResponse({'data': utilization})
