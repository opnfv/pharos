/*****************************************************************************
* Copyright (c) 2016 Max Breitenfeldt and others.
*
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Apache License, Version 2.0
* which accompanies this distribution, and is available at
* http://www.apache.org/licenses/LICENSE-2.0
*****************************************************************************/


function parseCalendarEvents(bookings) {
    var events = [];
    for (var i = 0; i < bookings.length; i++) {
        // convert ISO 8601 timestring to moment, needed for timezone handling
        start = moment(bookings[i]['start']);
        end = moment(bookings[i]['end']);
        event = {
            id: bookings[i]['id'],
            title: bookings[i]['purpose'],
            start: start,
            end: end,
        };
        events.push(event);
    }
    return events;
}

function loadEvents(url) {
    $.ajax({
        url: url,
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
    loadEvents(bookings_url);
    $('#starttimepicker').datetimepicker(timepickerOptions);
    $('#endtimepicker').datetimepicker(timepickerOptions);
});
