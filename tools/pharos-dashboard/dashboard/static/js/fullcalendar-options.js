// converts a moment to a readable fomat for the backend
function convertInputTime(time) {
    return moment(time).format('YYYY-MM-DD HH:00 ZZ');
}

function submitEventToForm(event) {
    action = 'change';

    var start = convertInputTime(event.start);
    var end = convertInputTime(event.end);
    $('#starttimepicker').data("DateTimePicker").date(start);
    $('#endtimepicker').data("DateTimePicker").date(end);

    $('#id_purpose').val(event.title);
    $("#deletebutton").removeClass('hidden');

    booking_id = event.id;
    repeat_id = event.repeat_id;

    if (repeat_id != null) {
        $("#deleterepeatbutton").removeClass('hidden');
    } else {
        $("#deleterepeatbutton").addClass('hidden');
    }
}

function editEvent(event) {
    submitEventToForm(event);
    $("#bookingform").trigger('submit');
}


var calendarOptions = {
    height: 600,
    header: {
        left: 'prev,next today',
        center: 'title',
        right: 'agendaWeek,month'
    },
    timezone: 'local',
    defaultView: 'agendaWeek',
    slotDuration: '00:60:00',
    slotLabelFormat: "HH:mm",
    firstDay: 1,
    allDaySlot: false,
    selectOverlap: false,
    eventOverlap: false,
    selectable: true,
    selectHelper: true,
    editable: false,
    eventLimit: true, // allow "more" link when too many events
    timeFormat: 'H(:mm)', // uppercase H for 24-hour clock
    unselectAuto: false,

    select: function (start, end) {
        action = 'create';

        var start = convertInputTime(start);
        var end = convertInputTime(end);

        $('#id_purpose').val('');
        $("#deletebutton").addClass('hidden'); // show delete button

        $('#starttimepicker').data("DateTimePicker").date(start);
        $('#endtimepicker').data("DateTimePicker").date(end);
    },

    eventClick: function (event, jsEvent, view) {
        $('#calendar').fullCalendar('unselect');
        submitEventToForm(event);
    },

    eventDrop: function (event) {
        $('#calendar').fullCalendar('unselect');
        editEvent(event);
    },

    eventResize: function (event) {
        $('#calendar').fullCalendar('unselect');
        editEvent(event);
    }
};