<?php
    include '../../../../auth-db.php';
    date_default_timezone_set('UTC');
    function connectDB() {
        global $username;
        global $password;
        global $hostname;
        global $dbname;

        $dbhandle = mysql_connect($hostname, $username, $password)
            or die("Unable to connect to MySQL.".mysql_error());
        $selected = mysql_select_db($dbname,$dbhandle)
            or die("Could not select opnfv_pharos DB.");
    }

    function closeDB(){
        mysql_connect($dbhandle);
    }

?>
