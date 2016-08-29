from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from django.views.generic import TemplateView
from jira import JIRAError

from account.jira_util import get_jira
from booking.forms import BookingForm
from booking.models import Booking
from dashboard.models import Resource


def create_jira_ticket(user, booking):
    jira = get_jira(user)
    issue_dict = {
        'project': 'PHAROS',
        'summary': str(booking.resource) + ': Access Request',
        'description': booking.purpose,
        'issuetype': {'name': 'Task'},
        'components': [{'name': 'POD Access Request'}],
        'assignee': {'name': booking.resource.owner.username}
    }
    issue = jira.create_issue(fields=issue_dict)
    jira.add_attachment(issue, user.userprofile.pgp_public_key)
    jira.add_attachment(issue, user.userprofile.ssh_public_key)
    booking.jira_issue_id = issue.id
    booking.save()


class BookingFormView(LoginRequiredMixin, FormView):
    template_name = "booking/booking_calendar.html"
    form_class = BookingForm

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
        user = self.request.user
        if not user.userprofile.ssh_public_key or not user.userprofile.pgp_public_key:
            messages.add_message(self.request, messages.INFO,
                                 'Please upload your private keys before booking')
            return redirect('account:settings')
        booking = Booking(start=form.cleaned_data['start'], end=form.cleaned_data['end'],
                          purpose=form.cleaned_data['purpose'], resource=self.resource,
                          user=user)
        try:
            booking.save()
        except ValueError as err:
            messages.add_message(self.request, messages.ERROR, err)
            return super(BookingFormView, self).form_invalid(form)
        except PermissionError as err:
            messages.add_message(self.request, messages.ERROR, err)
            return super(BookingFormView, self).form_invalid(form)
        try:
            create_jira_ticket(user, booking)
        except JIRAError:
            messages.add_message(self.request, messages.ERROR, 'Failed to create Jira Ticket. '
                                                               'Please check your Jira '
                                                               'permissions.')
            booking.delete()
            return super(BookingFormView, self).form_invalid(form)
        messages.add_message(self.request, messages.SUCCESS, 'Booking saved')
        return super(BookingFormView, self).form_valid(form)


class BookingView(TemplateView):
    template_name = "booking/booking_detail.html"

    def get_context_data(self, **kwargs):
        booking = get_object_or_404(Booking, id=self.kwargs['booking_id'])
        jira_issue = booking.get_jira_issue()
        title = 'Booking Details'
        context = super(BookingView, self).get_context_data(**kwargs)
        context.update({'title': title, 'booking': booking, 'jira_issue': jira_issue})
        return context


class ResourceBookingsJSON(View):
    def get(self, request, *args, **kwargs):
        resource = get_object_or_404(Resource, id=self.kwargs['resource_id'])
        bookings = resource.booking_set.get_queryset().values('id', 'start', 'end', 'purpose')
        return JsonResponse({'bookings': list(bookings)})
