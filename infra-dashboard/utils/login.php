<?php

    include 'database.php';


    function login(){
        $email = $_POST['email'];
        $password = $_POST['password'];

        $query = "SELECT * FROM user where EMAIL='".$email."';";
        $result = mysql_query($query);

        $user = array();
        if(mysql_num_rows($result) > 0) {
            $query = "SELECT * FROM user where email='".$email."' and password='".$password."';";
            $result = mysql_query($query);
            if(mysql_num_rows($result) > 0) {
                while($row = mysql_fetch_assoc($result)) {
                    $user = $row;
                    $user["result"] = 0;

                    $_SESSION['user_id'] = $user['user_id'];
                    $_SESSION['user_name'] = $user['name'];
                    $_SESSION['user_email'] = $user['email'];
                }
            } else {
                $user["result"] = 1; //wrong password
            }
        } else {
            $user["result"] = 2; //user not registered
        }
        echo json_encode($user);

    }


    $action = $_POST['action'];

    connectDB();
    session_start();

    if ($action == "login") {
        login();
    } else if ($action == "logout") {
        unset($_SESSION['user_id']);
        unset($_SESSION['user_name']);
        unset($_SESSION['user_email']);
        session_destroy();
    } else {
        echo "Invalid POST action.";
    }
    closeDB();

?>


