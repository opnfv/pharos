from datetime import timedelta
from django.utils import timezone
from django.views.generic import TemplateView

from booking.models import Booking
from dashboard.models import Resource
from jenkins.models import JenkinsSlave, JenkinsStatistic


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
            dev_pod = (resource, None)
            for booking in bookings:
                if booking.resource == resource:
                    dev_pod = (resource, booking)
            dev_pods.append(dev_pod)

        context = super(DevelopmentPodsView, self).get_context_data(**kwargs)
        context.update({'title': "Development Pods", 'dev_pods': dev_pods})
        return context


class LabOwnerView(TemplateView):
    template_name = "dashboard/lab_owner.html"

    def get_context_data(self, **kwargs):
        resources = Resource.objects.filter(slave__dev_pod=True)
        pods = []
        for resource in resources:
            utilization = {'idle': 0, 'online': 0, 'offline': 0}
            # query measurement points for the last week
            statistics = JenkinsStatistic.objects.filter(slave=resource.slave,
                                                         timestamp__gte=timezone.now() - timedelta(
                                                             days=7))

            utilization['idle'] = statistics.filter(idle=True).count()
            utilization['online'] = statistics.filter(online=True).count()
            utilization['offline'] = statistics.filter(offline=True).count()

            bookings = Booking.objects.filter(resource=resource, end__gt=timezone.now())

            pods.append((resource, utilization, bookings))
        context = super(LabOwnerView, self).get_context_data(**kwargs)
        context.update({'title': "Overview", 'pods': pods})
        return context
