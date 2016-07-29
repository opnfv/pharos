// converts a moment to a readable fomat for the backend
function convertInputTime(time) {
    return moment(time).format('YYYY-MM-DD HH:00 ZZ');
}

function sendEventToForm(event) {
    var start = convertInputTime(event.start);
    var end = convertInputTime(event.end);
    $('#starttimepicker').data("DateTimePicker").date(start);
    $('#endtimepicker').data("DateTimePicker").date(end);
    $('#submitform').html("Change Booking");
    $('#purposefield').val(event.title);
    $('#id_booking_id').val(event.id); // create a new booking
    $("#deletebutton").removeClass('hidden'); // show delete button
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
        var start = convertInputTime(start);
        var end = convertInputTime(end);

        $('#starttimepicker').data("DateTimePicker").date(start);
        $('#endtimepicker').data("DateTimePicker").date(end);
        $('#submitform').html("Book Pod");
        $('#purposefield').val('');
        $('#id_booking_id').val(''); // create a new booking
        $("#deletebutton").addClass('hidden'); // hide delete button
    },

    eventClick: function (event, jsEvent, view) {
        $('#calendar').fullCalendar('unselect');
        sendEventToForm(event);
    },

    eventDrop: function (event) {
        $('#calendar').fullCalendar('unselect');
        sendEventToForm(event);
    },

    eventResize: function (event) {
        $('#calendar').fullCalendar('unselect');
        sendEventToForm(event);
    }
};