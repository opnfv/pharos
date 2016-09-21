##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


var tmpevent;

function sendEventToForm(event) {
    $('#starttimepicker').data("DateTimePicker").date(event.start);
    $('#endtimepicker').data("DateTimePicker").date(event.end);
}

var calendarOptions = {
    height: 600,
    header: {
        left: 'prev,next today',
        center: 'title',
        right: 'agendaWeek,month'
    },
    timezone: user_timezone, // set in booking_calendar.html
    defaultView: 'month',
    slotDuration: '00:60:00',
    slotLabelFormat: "HH:mm",
    firstDay: 1,
    allDaySlot: false,
    selectOverlap: false,
    eventOverlap: false,
    selectable: true,
    editable: false,
    eventLimit: true, // allow "more" link when too many events
    timeFormat: 'H(:mm)', // uppercase H for 24-hour clock
    unselectAuto: true,
    nowIndicator: true,

    // selectHelper is only working in the agendaWeek view, this is a workaround:
    // if an event is selected, the existing selection is removed and a temporary event is added
    // to the calendar
    select: function (start, end) {
        if (tmpevent != undefined) {
            $('#calendar').fullCalendar('removeEvents', tmpevent.id);
            $('#calendar').fullCalendar('rerenderEvents');
            tmpevent = undefined;
        }
        // the times need to be converted here to make them show up in the agendaWeek view if they
        // are created in the month view. If they are not converted, the tmpevent will only show
        // up in the (deactivated) allDaySlot
        start = moment(start);
        end = moment(end);

        tmpevent = {
            id: '537818f62bc63518ece15338fb86c8be',
            title: 'New Booking',
            start: start,
            end: end,
            editable: true
        };

        $('#calendar').fullCalendar('renderEvent', tmpevent, true);
        sendEventToForm(tmpevent);
    },

    eventClick: function (event) {
        if (tmpevent != undefined) {
            if (event.id != tmpevent.id) {
                $('#calendar').fullCalendar('removeEvents', tmpevent.id);
                $('#calendar').fullCalendar('rerenderEvents');
                tmpevent = undefined;
            }
        }

        // tmpevent is deleted if a real event is clicked, load event details
        if (tmpevent == undefined) {
            var booking_detail_url = booking_detail_prefix + event.id;

            $.ajax({
                url: booking_detail_url,
                type: 'get',
                success: function (data) {
                    $('#booking_detail_content').html(data);
                },
                failure: function (data) {
                    alert('Error loading booking details');
                }
            });
            $('#booking_detail_modal').modal('show');
        }
    },

    eventDrop: function (event) {
        sendEventToForm(event);
    },

    eventResize: function (event) {
        sendEventToForm(event);
    }
};