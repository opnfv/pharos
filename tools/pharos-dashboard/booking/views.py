from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from account.jira_util import get_jira
from booking.forms import BookingForm
from booking.models import Booking
from dashboard.models import Resource


class BookingFormView(LoginRequiredMixin, FormView):
    template_name = "booking/booking_calendar.html"
    form_class = BookingForm

    def open_jira_issue(self,booking):
        jira = get_jira(self.request.user)
        issue_dict = {
            'project': 'PHAROS',
            'summary': 'Booking: ' + str(self.resource),
            'description': str(booking),
            'issuetype': {'name': 'Task'},
        }
        jira.create_issue(fields=issue_dict)

    def dispatch(self, request, *args, **kwargs):
        self.resource = get_object_or_404(Resource, id=self.kwargs['resource_id'])
        return super(BookingFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        title = 'Booking: ' + self.resource.name
        context = super(BookingFormView, self).get_context_data(**kwargs)
        context.update({'title': title, 'resource': self.resource})
        return context

    def get_success_url(self):
        return reverse('booking:create', kwargs=self.kwargs)

    def form_valid(self, form):
        booking = Booking(start=form.cleaned_data['start'], end=form.cleaned_data['end'],
                          purpose=form.cleaned_data['purpose'], resource=self.resource,
                          user=self.request.user)
        try:
            booking.save()
        except ValueError as err:
            messages.add_message(self.request, messages.ERROR, err)
            return super(BookingFormView, self).form_invalid(form)
        except PermissionError as err:
            messages.add_message(self.request, messages.ERROR, err)
            return super(BookingFormView, self).form_invalid(form)
        self.open_jira_issue(booking)
        messages.add_message(self.request, messages.SUCCESS, 'Booking saved')
        return super(BookingFormView, self).form_valid(form)


class ResourceBookingsJSON(View):
    def get(self, request, *args, **kwargs):
        resource = get_object_or_404(Resource, id=self.kwargs['resource_id'])
        bookings = resource.booking_set.get_queryset().values('id', 'start', 'end', 'purpose')
        return JsonResponse({'bookings': list(bookings)})
