<?php
    // trick for the calendar object, if we use always the same id name, it doesn't work properly
    $random = time();
    $calendar_id = "calendar_".$random;
?>


<script type="text/javascript">
    $(document).ready(function() {
        $('#example').DataTable( {
            "order": [[ 2, "desc" ],[ 5, "desc"]]
        } );
        var date = new Date();
        var d = date.getDate();
        var m = date.getMonth();
        var y = date.getFullYear();
    } );

    $(function() {
        var dialog, form,

        // From http://www.whatwg.org/specs/web-apps/current-work/multipage/states-of-the-type-attribute.html#e-mail-state-%28type=email%29
        emailRegex = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
        email = $( "#email" ),
        password = $( "#password" ),
        allFields = $( [] ).add( email ).add( password ),
        tips = $( ".validateTips" );

        function updateTips( t ) {
          tips
            .text( t )
            .addClass( "ui-state-highlight" );
          setTimeout(function() {
            tips.removeClass( "ui-state-highlight", 1500 );
          }, 500 );
        }

        function checkLength( o, n, min, max ) {
          if ( o.val().length > max || o.val().length < min ) {
            o.addClass( "ui-state-error" );
            updateTips( "Length of " + n + " must be between " +
              min + " and " + max + "." );
            return false;
          } else {
            return true;
          }
        }

        function checkRegexp( o, regexp, n ) {
          if ( !( regexp.test( o.val() ) ) ) {
            o.addClass( "ui-state-error" );
            updateTips( n );
            return false;
          } else {
            return true;
          }
        }

        function bookResource() {
            var user_id = $('#hd_user_id').val();
            if (user_id == "") {
                alert ("Only registered users can book.");
                return;
            }
            var resource_id = $('#resource_id').val();
            var resource_name = $('#resource_name').val();
            var purpose = $('#purpose').val();
            var starttime = $('#starttime').val();
            var endtime = $('#endtime').val();
            $.ajax({
                type: 'POST',
                url: "utils/book.php",
                data: {action: 'book', resource_id: resource_id, resource_name: resource_name, user_id: user_id, start: starttime, end: endtime, purpose: purpose, start: starttime, end: endtime},
                success: function(data){
                    if (data == "1") alert("Booking not possible (your account is not associated with a role). Please contact the administrator.");
                    else if (data == "2") alert("You are not allowed to book this resource.");
                    else {
                        alert(data)
                        //location.reload();
                        var href = document.location.protocol +"//"+ document.location.hostname + document.location.pathname
                        location.href = href + "?page=devpods"
                    }
                },
                errpr: function(data){
                    alert("error")
                }

            });

            dialog.dialog( "close" );
            return true;
        }

        dialog = $( "#dialog-form" ).dialog({
            autoOpen: false,
            height: 800,
            width: 900,
            modal: true,
            resizable:false,
            buttons: {
                "Book": bookResource,
                Cancel: function() {
                    dialog.dialog( "close" );
                    $('#starttime').attr('value', "");
                    $('#endtime').attr('value', "");
                    $('#purpose').attr('value', "");
                    $(".ui-dialog-buttonpane button:contains('Book')").attr("disabled", true)
                                              .addClass("ui-state-disabled");
                }
            },
            close: function() {
                form[ 0 ].reset();
                allFields.removeClass( "ui-state-error" );
            }
        });

        form = dialog.find( "form" ).on( "submit", function( event ) {
            event.preventDefault();
            bookResource();
        });

        $(".ui-dialog-buttonpane button:contains('Book')").attr("disabled", true)
                                              .addClass("ui-state-disabled");
        dialog_event = $( "#dialog_event" ).dialog({
            autoOpen: false,
            height: 400,
            width: 420,
            modal: true,
            resizable:false,
            buttons: {
                Close: function() {
                    dialog_event.dialog( "close" );
                },
                "Release": function() {
                    alert("Not working yet.");
                }
            },
        });


        $( ".btn-book" ).button().on( "click", function() {
            var resource_id = $(this).attr('id');
            var resource_name = $(this).attr('value');
            $('#resource_id').attr('value', resource_id);
            $('#resource_name').attr('value', resource_name);
            var title = "Book resource: ".concat(resource_name);
            var calendar_id = '<?=$calendar_id?>';
            $('#<?=$calendar_id?>').fullCalendar( 'destroy' );
            $.ajax({
                type: 'POST',
                url: "utils/book.php",
                data: {action: 'getBookedDates', resource_id: resource_id},

                success: function(data){
                    //if (data != "") {
                        var calendarOptions = {
                            height: 660,
                            header: {
                                left: 'prev,next today',
                                center: 'title',
                                right: 'agendaWeek,month'
                            },
                            defaultView: 'agendaWeek',
                            slotDuration: '00:60:00',
                            slotLabelFormat:"HH:mm",
                            firstDay: 1,
                            nowIndicator: true,
                            allDaySlot: false,
                            selectOverlap: false,
                            selectable: true,
                            selectHelper: true,
                            editable: false,
                            timezone: 'UTC',
                            eventStartEditable: false,
                            eventDurationEditable: false,
                            events: jQuery.parseJSON( data ),
                            select: function(start, end) {
                                var view = $('#<?=$calendar_id?>').fullCalendar('getView');
                                if (view.name == "month") return
                                var title = prompt('Purpose of this booking:');
                                var eventData;
                                var provisional_id = "537818F62BC63518ECE15338FB86C8BE";
                                if (title) {
                                    $('#<?=$calendar_id?>').fullCalendar('removeEvents',provisional_id);
                                    eventData = {
                                        id: provisional_id,
                                        title: title,
                                        start: start,
                                        end: end
                                    };
                                    start=moment(start).format('YYYY-MM-DD HH:mm:ss');
                                    end=moment(end).format('YYYY-MM-DD HH:mm:ss');
                                    $('#<?=$calendar_id?>').fullCalendar('renderEvent', eventData, true); // stick? = true
                                    $('#starttime').attr('value', start);
                                    $('#endtime').attr('value', end);
                                    $('#purpose').attr('value', title);
                                    $(".ui-dialog-buttonpane button:contains('Book')").attr("disabled", false)
                                                              .removeClass("ui-state-disabled");
                                }
                                $('#<?=$calendar_id?>').fullCalendar('unselect');

                            },
                            eventLimit: true, // allow "more" link when too many events
                            timeFormat: 'H(:mm)', // uppercase H for 24-hour clock
                            eventClick: function(event) {
                                $('#dg-start').text(event.start);
                                $('#dg-end').text(event.end);
                                $('#dg-booker-email').text(event.booker_email);
                                $('#dg-purpose').text(event.title);
                                dialog_event.dialog( "open" );
                            }
                        }
                        $('#<?=$calendar_id?>').fullCalendar(calendarOptions);
                        $('#<?=$calendar_id?>').fullCalendar('render');
                    //}
                    //else {
                        // if first time (it has never been booked)
                    //    $('#<?=$calendar_id?>').fullCalendar('removeEventSource');
                    //}
                },
                error: function(data){
                    alert("error getting booked dates.");
                }

            });
            dialog.dialog( 'option', 'title', title);
            dialog.dialog( "open" );
            ///$('#<?=$calendar_id?>').fullCalendar( 'rerenderEvents' )
        });
    });
</script>

<style>
    .fc-divider {
        display:none !important;
    }
</style>

<?php

    include '../utils/jenkinsAdapter.php';
    include '../utils/database.php';

    connectDB();
    //$q = "select r.ID,r.NAME,r.LINK,r.DESCR,r.ACTIVE,b.BOOKEDBY,b.BOOKEDFROM,b.BOOKEDUNTIL,b.PURPOSE from resource r left join booking b on r.ID = b.RES_Id and now() between b.BOOKEDFROM and b.BOOKEDUNTIL  where r.TYPE=2;";
    $q = "SELECT r.resource_id,r.name as resname,r.slavename, r.link,u.user_id,u.name as username,u.email,b.starttime,b.endtime,b.purpose from resource r LEFT JOIN pod p LEFT JOIN booking b INNER JOIN user u ON u.user_id = b.user_id ON b.resource_id = p.resource_id AND now() > b.starttime AND now() <= b.endtime ON r.resource_id = p.resource_id;";
    $result = mysql_query($q);

    //SELECT r.name as resname,r.slavename, r.link, r.resource_id,u.user_id,u.name as username,u.email,b.starttime,b.endtime,b.purpose from resource r LEFT JOIN pod p LEFT JOIN booking b INNER JOIN user u ON u.user_id = b.user_id ON b.resource_id = p.resource_id AND now() > b.starttime AND now() <= b.endtime ON r.resource_id = p.resource_id WHERE type_id=2;
    closeDB();

    echo '<table id="example" class="table table-striped table-bordered" cellspacing="0" width="100%">';
    echo "<thead>";
    echo "<tr>";
    echo "<th>Name</th>";
    echo "<th>Slave Name</th>";
    echo "<th>Booked by</th>";
    echo "<th>Booked until</th>";
    echo "<th>Purpose</th>";
    echo "<th>Status</th>";
    echo "<th></th>";
    echo "</tr>";
    echo "</thead>";
    echo "<tbody>";

    while ($row = mysql_fetch_array($result)) {
        $slave = $row{'slavename'};
        if (! isDevPod($slave)) continue;

        $slave_url = getSlaveUrl($slave);
        $status = getSlaveStatus($slave);
        echo "<tr>";
        echo "<th><a target='_blank' href='".$row{'link'}."'>".$row{'resname'}."</a></th>";
        echo "<th><a target='_blank' href='".$slave_url."'>".$slave."</a></th>";
        if ($row{'username'} != "")  $booker = $row{'username'};
        else $booker="-";
        echo "<th>".$booker."</th>";

        if ($row{'endtime'} != "")  {
            $until = strtotime($row{'endtime'});
            echo "<th>".date('d/M/Y', $until)."</th>";
            //$until = $row{'endtime'};
        } else {
            $until="-";
            echo "<th>".$until."</th>";
        }
        if ($row{'purpose'} != "")  $purpose = $row{'purpose'};
        else $purpose="-";
        echo "<th>".$purpose."</th>";
        $active = 'true';
        if ($status == "online") $color = "#BEFAAA";
        else $color = "#FAAAAB";
        echo "<th style='background-color: ".$color.";'>".$status."</th>";

        echo "<th><button id='".$row{'resource_id'}."' value='".$row{'slavename'}."' class='btn-book' type='button'>Book</button></th>";
        echo "</tr>";
    }
    echo '</tbody>';
    echo '</table>';
?>


<div id="dialog-form" title="Book resource">
    <form>
        <div id='<?=$calendar_id?>' style="margin-top:10px"></div>
        <input type="submit" tabindex="-1" style="position:absolute; top:-100px"/>
    </form>
</div>


<div id="dialog_event" title="event">
    <table>
        <tr>
            <td style="width:100px">Booked by:</td>
            <td><p id="dg-booker-email"></p></td>
        </tr>
        <tr>
            <td>Start:</td>
            <td><p id="dg-start"></p></td>
        </tr>
        <tr>
            <td>End:</td>
            <td><p id="dg-end"></p></td>
        </tr>
        <tr>
            <td>Purpose:</td>
            <td><p id="dg-purpose"></p></td>
        </tr>
    <table>
</div>



<input type="hidden" id="resource_id" name="resource_id" value="10"/>
<input type="hidden" id="resource_name" name="resource_name"/>
<input type="hidden" id="starttime" value=""/>
<input type="hidden" id="endtime" value=""/>
<input type="hidden" id="purpose" value=""/>
<input type="hidden" id="event_id" value=""/>



