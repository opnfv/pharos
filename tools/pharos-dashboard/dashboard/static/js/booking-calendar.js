function parseCalendarEvents(bookings) {
    var events = [];
    for (var i = 0; i < bookings.length; i++) {
        event = {
            id: bookings[i]['booking_id'],
            title: bookings[i]['purpose'],
            start: bookings[i]['start_date_time'],
            end: bookings[i]['end_date_time'],
            repeat_id: bookings[i]['repeat_booking__repeat_booking_id'],
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
        },
        failure: function (data) {
            alert('Error loading booking data');
        }
    });
}

$(document).ready(function () {
    $('#calendar').fullCalendar(calendarOptions);
    loadEvents(url_prefix + '/bookings');
    $('#starttimepicker').datetimepicker(timepickerOptions);
    $('#endtimepicker').datetimepicker(timepickerOptions);
    $('#repeatendtimepicker').datetimepicker(timepickerOptions);

    if ($("#id_repeat").is(':checked')) {
        $("#repeatform").removeClass('hidden');
    }

    $("#id_repeat").click(function () {
        $("#repeatform").toggleClass('hidden');
    });

    $("#bookingform").submit(function () {
        if (action === 'create') {
            if ($("#id_repeat").is(':checked')) {
                $('#bookingform').attr('action', url_prefix + '/repeat_booking/create');
            } else {
                $('#bookingform').attr('action', url_prefix + '/booking/create');
            }
        } else {
            $('#bookingform').attr('action', url_prefix + '/booking/' + booking_id + '/change');
        }
    });


    $('#bookingform').attr('action', url_prefix + '/booking/' + booking_id + '/change');

    // send Post request to delete url if button is clicked
    $("#deletebutton").click(function () {
        $.ajax({
            type: 'post',
            url: url_prefix + '/booking/' + +booking_id + '/delete',
            success: function () {
                location.reload();
            },
            failure: function () {
                alert('Deleting failed')
            }
        })
    });

    // send Post request to delete url if button is clicked
    $("#deleterepeatbutton").click(function () {
        $.ajax({
            type: 'post',
            url: url_prefix + '/repeat_booking/' + repeat_id + '/delete',
            success: function () {
                location.reload();
            },
            failure: function () {
                alert('Deleting failed')
            }
        })
    });
});