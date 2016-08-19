from django.utils import timezone
from django.views.generic import TemplateView

from booking.models import Booking
from dashboard.models import Resource
from jenkins import adapter as jenkins


class JenkinsSlavesView(TemplateView):
    template_name = "dashboard/jenkins_slaves.html"

    def get_context_data(self, **kwargs):
        slaves = jenkins.get_all_slaves()
        for slave in slaves:
            jenkins.parse_slave_data(slave, slave)

        context = super(JenkinsSlavesView, self).get_context_data(**kwargs)
        context.update({'title': "Jenkins Slaves", 'slaves': slaves})
        return context


class CIPodsView(TemplateView):
    template_name = "dashboard/ci_pods.html"

    def get_context_data(self, **kwargs):
        resources = Resource.objects.filter().values()  # get resources as a set of dicts
        ci_pods = []
        for resource in resources:
            if not jenkins.is_ci_slave(resource['slavename']):
                continue
            ci_slave = jenkins.get_slave(resource['slavename'])
            jenkins.parse_slave_data(resource, ci_slave)
            ci_pods.append(resource)

        context = super(CIPodsView, self).get_context_data(**kwargs)
        context.update({'title': "CI Pods", 'ci_pods': ci_pods})
        return context


class DevelopmentPodsView(TemplateView):
    template_name = "dashboard/dev_pods.html"

    def get_context_data(self, **kwargs):
        resources = Resource.objects.filter().values()  # get resources as a set of dicts
        dev_pods = []

        current_bookings = Booking.objects.filter(start__lte=timezone.now())
        current_bookings = current_bookings.filter(end__gt=timezone.now())

        for resource in resources:
            if not jenkins.is_dev_pod(resource['slavename']):
                continue
            dev_pod = jenkins.get_slave(resource['slavename'])
            jenkins.parse_slave_data(resource, dev_pod)
            for booking in current_bookings:
                if booking.resource.slavename == resource['slavename']:
                    resource['current_booking'] = booking
            dev_pods.append(resource)

        context = super(DevelopmentPodsView, self).get_context_data(**kwargs)
        context.update({'title': "Development Pods", 'dev_pods': dev_pods})
        return context
