from dashboard.forms.booking_form import BookingForm
from dashboard.models import Resource, Booking
from dashboard.views.registration import BookingUserTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View


@method_decorator(login_required, name='dispatch')
class BookingCalendarView(BookingUserTestMixin, FormView):
    template_name = "dashboard/booking_calendar.html"
    form_class = BookingForm

    # set instance variables
    def dispatch(self, request, *args, **kwargs):
        self.foo = request.GET.get('foo', False)
        self.resource = get_object_or_404(Resource, resource_id=self.kwargs['resource_id'])
        return super(BookingCalendarView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.success_url = self.request.path
        booking = None
        # change existing booking
        if form.cleaned_data['booking_id'] is not None:
            booking = get_object_or_404(Booking, booking_id=form.cleaned_data['booking_id'])
        # create new booking
        else:
            booking = Booking()
            booking.resource = self.resource
            booking.user = self.request.user
        booking.start_date_time = form.cleaned_data['start_date_time']
        booking.end_date_time = form.cleaned_data['end_date_time']
        booking.purpose = form.cleaned_data['purpose']
        try:
            booking.save()
        except ValueError:
            messages.add_message(self.request, messages.ERROR,
                                 'This booking overlaps with another booking')
            return super(BookingCalendarView, self).form_invalid(form)
        messages.add_message(self.request, messages.SUCCESS,
                             'Booking saved')
        return super(BookingCalendarView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        title = 'Booking: ' + self.resource.name
        context = super(BookingCalendarView, self).get_context_data(**kwargs)
        context.update({'title': title, 'resource': self.resource})
        return context


@method_decorator(login_required, name='dispatch')
class ResourceBookingsView(BookingUserTestMixin, View):
    def get(self, request, *args, **kwargs):
        resource = Resource.objects.get(resource_id=self.kwargs['resource_id'])
        bookings = resource.booking_set.get_queryset().values(
            'booking_id', 'user__username', 'user__email',
            'start_date_time', 'end_date_time', 'purpose')
        return JsonResponse({'bookings': list(bookings)})


@method_decorator(login_required, name='dispatch')
class DeleteBookingView(BookingUserTestMixin, View):
    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, booking_id=self.kwargs['booking_id'])
        booking.delete()
        return JsonResponse({True: self.kwargs['booking_id']})
