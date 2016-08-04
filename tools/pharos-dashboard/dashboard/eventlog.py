from dashboard.models import Booking, BookingEventLog


def log_repeat_booking_action(repeat_booking, action):
    event = BookingEventLog(user=repeat_booking.user, repeat_booking=repeat_booking, resource=repeat_booking.resource,
                            action=action)
    event.save()

def log_booking_action(booking, action):
    event = BookingEventLog(user=booking.user, booking=booking, resource=booking.resource,
                            action=action)
    event.save()