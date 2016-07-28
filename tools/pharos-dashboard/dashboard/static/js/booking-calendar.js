function parseDisabledTimeIntervals(bookings) {
    var timeIntervals = [];

    for (var i = 0; i < bookings.length; i++) {
        var interval = [
            moment(bookings[i]['start_date_time']),
            moment(bookings[i]['end_date_time'])
        ];
        timeIntervals.push(interval);
    }
    return timeIntervals;
}

function parseCalendarEvents(bookings) {
    var events = [];
    for (var i = 0; i < bookings.length; i++) {
        event = {
            id: bookings[i]['booking_id'],
            title: bookings[i]['purpose'],
            start: bookings[i]['start_date_time'],
            end: bookings[i]['end_date_time'],
            editable: true
        };
        events.push(event);
    }
    return events;
}

function loadEvents(bookings_url) {
    $.ajax({
        url: bookings_url,
        type: 'get',
        success: function (data) {
            $('#calendar').fullCalendar('addEventSource', parseCalendarEvents(data['bookings']));
            var intervals = parseDisabledTimeIntervals(data['bookings']);
            $('#starttimepicker').data("DateTimePicker").disabledTimeIntervals(intervals);
            $('#endtimepicker').data("DateTimePicker").disabledTimeIntervals(intervals);
        },
        failure: function (data) {
            alert('Error loading booking data');
        }
    });
}

$(document).ready(function () {
    $('#calendar').fullCalendar(calendarOptions);
    $('#starttimepicker').datetimepicker(timepickerOptions);
    $('#endtimepicker').datetimepicker(timepickerOptions);

    loadEvents(bookings_url);

    // send Post request to delete url if button is clicked
    $("#deletebutton").click(function () {
        var booking_id = $('#id_booking_id').val();
        $.ajax({
            type: 'post',
            url: '/booking/' + booking_id + '/delete',
            success: function () {
                $('#calendar').fullCalendar('removeEvents');
                loadEvents(bookings_url);
                $('#calendar').fullCalendar('rerenderEvents');
            },
            failure: function () {
                alert('Deleting failed')
            }
        })
    })
});