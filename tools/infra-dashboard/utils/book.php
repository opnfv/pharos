<?php

    include 'database.php';

    function book() {
        $resource_id = $_POST['resource_id'];
        $resource_name = $_POST['resource_name'];
        $user_id = $_POST['user_id'];
        $start = $_POST['start'];
        $end = $_POST['end'];
        $purpose = $_POST['purpose'];

        $query = "select role.name as rolename from user, role, user_role where user.user_id = ".$user_id." and role.role_id=user_role.role_id and user_role.user_id=user.user_id;";
        $result = mysql_query($query);

        if(mysql_num_rows($result) == 0) {
            echo "1"; //return a code instead of a meesage. Display the message later in javascript according to the returned code.
            //echo "Booking not possible (your account is not associated with a role). Please contact the administrator.";
            exit;
        }
        $is_only_lab_owner = true;
        while ($row = mysql_fetch_array($result)) {
            $rolename = $row['rolename'];
            if ($rolename != "lab_owner") $is_only_lab_owner = false;
        }
        if ($is_only_lab_owner) {
            $query = "select * from user u inner join user_resource r on r.user_id=u.user_id and u.user_id=".$user_id." and r.resource_id=".$resource_id.";";
            $result = mysql_query($query);
            if(mysql_num_rows($result) == 0) {
                echo "2";
                //echo "You are not allowed to book this resource. ";
                exit;
            }
        }
        $query = "INSERT INTO booking (resource_id, user_id, starttime, endtime, purpose) VALUES (".$resource_id.",".$user_id.",'".$start."','".$end."', '".$purpose."');";
        $result = mysql_query($query);
        if(mysql_insert_id()>0){
            echo "Booking successful. The resource '".$resource_name."' is booked from ".$start." to ".$end.".";
        }
        else{
            echo "Mysql Error : ".mysql_error().". Query = ".$query;
        }

    }

    function getBookedDates() {
        $resource_id = $_POST['resource_id'];
        $query = "SELECT b.booking_id, b.resource_id,u.name as username,u.email,b.starttime,b.endtime,b.creation,b.purpose FROM booking as b,user as u WHERE b.resource_id=".$resource_id." AND b.user_id=u.user_id;";
        $result = mysql_query($query);

        $events = array();
        while ($row = mysql_fetch_array($result)) {
            $e = array();
            $e['id'] = $row['booking_id'];
            $e['booker_name'] = $row['username'];
            $e['booker_email'] = $row['email'];
            $e['title'] = $row['purpose'];
            $e['start'] = $row['starttime'];
            $e['end'] = $row['endtime'];
            $e['bookdate'] = $row['creation'];

            // Merge the event array into the return array
            array_push($events, $e);
        }

        echo json_encode($events);
    }



    $action = $_POST['action'];

    connectDB();
    if ($action == "book") {
        book();
    } elseif ($action == "getBookedDates" ) {
        getBookedDates();
    } else {
        echo "Invalid POST action.";
    }
    closeDB();
?>
