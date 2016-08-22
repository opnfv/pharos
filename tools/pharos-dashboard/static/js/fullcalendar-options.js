var tmpevent;

// converts a moment to a readable fomat for the backend
function convertInputTime(time) {
    return time;
    //return moment(time).format('YYYY-MM-DD HH:00 ZZ');
}

function sendEventToForm(event) {
    $('#starttimepicker').data("DateTimePicker").date(convertInputTime(event.start));
    $('#endtimepicker').data("DateTimePicker").date(convertInputTime(event.end));
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
        }
        // the times need to be converted here to make them show up in the agendaWeek view if they
        // are created in the month view. If they are not converted, the tmpevent will only show
        // up in the (deactivated) allDaySlot
        start = convertInputTime(start);
        end = convertInputTime(end);

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
            }
        }
    },

    eventDrop: function (event) {
        sendEventToForm(event);
    },

    eventResize: function (event) {
        sendEventToForm(event);
    }
};