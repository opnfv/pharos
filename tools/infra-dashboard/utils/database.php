<?php

    date_default_timezone_set('UTC');
    function connectDB() {
        $username = "root";
        $password = "opnfv";
        $hostname = "localhost";
        $dbhandle = mysql_connect($hostname, $username, $password)
            or die("Unable to connect to MySQL.");
        $selected = mysql_select_db("opnfv_pharos",$dbhandle)
            or die("Could not select opnfv_pharos DB.");
    }

    function closeDB(){
        mysql_connect($dbhandle);
    }

?>
