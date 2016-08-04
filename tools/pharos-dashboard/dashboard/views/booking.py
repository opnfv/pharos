from dashboard import eventlog
from dashboard.forms.booking_form import BookingForm
from dashboard.models import Resource, Booking, RepeatBooking, BookingEventLog
from dashboard.views.registration import BookingUserTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View
from datetime import timedelta
from django.utils import timezone


class BookingCalendarView(FormView):
    template_name = "booking/booking_calendar.html"
    form_class = BookingForm

    def dispatch(self, request, *args, **kwargs):
        self.success_url = '/resource/' + self.kwargs['resource_id'] + '/booking/'
        self.resource = get_object_or_404(Resource, resource_id=self.kwargs['resource_id'])
        return super(BookingCalendarView, self).dispatch(request, kwargs)

    def get_context_data(self, **kwargs):
        events = BookingEventLog.objects.filter(resource=self.resource)[:20]
        title = 'Booking: ' + self.resource.name
        context = super(BookingCalendarView, self).get_context_data(**kwargs)
        context.update({'title': title, 'resource': self.resource, 'events': events})
        return context

    def save_booking(self, booking, action):
        try:
            booking.save()
        except ValueError as err:
            messages.add_message(self.request, messages.ERROR, err)
            return False
        messages.add_message(self.request, messages.SUCCESS,
                             'Booking saved')
        eventlog.log_booking_action(booking, action)
        return True


@method_decorator(login_required, name='dispatch')
class BookingCreateView(BookingUserTestMixin, BookingCalendarView):
    form_class = BookingForm

    def form_valid(self, form):
        booking = Booking(resource=self.resource, user=self.request.user,
                          start_date_time=form.cleaned_data['start_date_time'],
                          end_date_time=form.cleaned_data['end_date_time'],
                          purpose=form.cleaned_data['purpose'])
        if self.save_booking(booking, 'create') == False:
            return super(BookingCreateView, self).form_invalid(form)
        return super(BookingCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class BookingChangeView(BookingUserTestMixin, BookingCalendarView):
    form_class = BookingForm

    def form_valid(self, form):
        booking = get_object_or_404(Booking, booking_id=self.kwargs['booking_id'])
        booking.start_date_time = form.cleaned_data['start_date_time']
        booking.end_date_time = form.cleaned_data['end_date_time']
        booking.purpose = form.cleaned_data['purpose']
        if self.save_booking(booking, 'change') == False:
            return super(BookingChangeView, self).form_invalid(form)
        return super(BookingChangeView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class RepeatBookingCreateView(BookingUserTestMixin, BookingCalendarView):
    form_class = BookingForm

    def form_invalid(self, form):
        return super(RepeatBookingCreateView, self).form_invalid(form)

    def form_valid(self, form):
        if form.cleaned_data['repeat_end'] - timezone.now() > timedelta(days=365):
            return super(RepeatBookingCreateView, self).form_invalid(form)
        repeat_booking = RepeatBooking(user=self.request.user,
                                       repeat_end=form.cleaned_data['repeat_end'],
                                       resource=self.resource)
        repeat_booking.save()
        interval = timedelta(days=1)
        if form.cleaned_data['repeat_interval'] == '1':  # daily
            interval = timedelta(days=1)
        if form.cleaned_data['repeat_interval'] == '2':  # weekly
            interval = timedelta(weeks=1)
        if form.cleaned_data['repeat_interval'] == '3':  # monthly
            interval = timedelta(weeks=4)  # stays on the same weekday
        booking_start = form.cleaned_data['start_date_time']
        booking_end = form.cleaned_data['end_date_time']
        cnt = 0
        while booking_start < repeat_booking.repeat_end and booking_end < repeat_booking.repeat_end:
            booking = Booking(resource=self.resource, user=self.request.user, start_date_time=booking_start,
                              end_date_time=booking_end, purpose=form.cleaned_data['purpose'],
                              repeat_booking=repeat_booking)
            try:
                booking.save()
            except ValueError:
                repeat_booking.delete()  # this deletes all bookings in this series
                messages.add_message(self.request, messages.ERROR,
                                     'Error saving repeat booking: There may be an overlapping booking')
                return super(RepeatBookingCreateView, self).form_invalid(form)
            booking_start += interval
            booking_end += interval
            cnt += 1
        eventlog.log_repeat_booking_action(repeat_booking, 'create')
        messages.add_message(self.request, messages.SUCCESS,
                             'saved ' + str(cnt) + ' Bookings')
        return super(RepeatBookingCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ResourceBookingsView(BookingUserTestMixin, View):
    def get(self, request, *args, **kwargs):
        resource = get_object_or_404(Resource, resource_id=self.kwargs['resource_id'])
        bookings = resource.booking_set.filter(deleted=False)
        bookings = bookings.values(
            'booking_id', 'user__username', 'user__email',
            'start_date_time', 'end_date_time', 'purpose', 'repeat_booking__repeat_booking_id')
        return JsonResponse({'bookings': list(bookings)})


@method_decorator(login_required, name='dispatch')
class DeleteBooking(BookingUserTestMixin, View):
    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, booking_id=self.kwargs['booking_id'])
        booking.logical_delete()
        eventlog.log_booking_action(booking, 'delete')
        messages.add_message(self.request, messages.SUCCESS,
                             'Booking deleted')
        return JsonResponse({True: self.kwargs['booking_id']})


@method_decorator(login_required, name='dispatch')
class DeleteRepeatBooking(BookingUserTestMixin, View):
    def post(self, request, *args, **kwargs):
        repeat_booking = get_object_or_404(RepeatBooking, repeat_booking_id=self.kwargs['repeat_booking_id'])
        count = repeat_booking.booking_set.count()
        repeat_booking.logical_delete()
        eventlog.log_repeat_booking_action(repeat_booking, 'delete')
        messages.add_message(self.request, messages.SUCCESS,
                             str(count) + ' Bookings deleted')
        return JsonResponse({True: self.kwargs['repeat_booking_id']})
