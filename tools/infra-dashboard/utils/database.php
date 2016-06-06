<?php

    date_default_timezone_set('UTC');
    function connectDB() {
        $username = "pharos";
        $password = "";
        $hostname = "173.194.87.85";
        $dbhandle = mysql_connect($hostname, $username, $password)
            or die("Unable to connect to MySQL.".mysql_error());
        $selected = mysql_select_db("opnfv_pharos",$dbhandle)
            or die("Could not select opnfv_pharos DB.");
    }

    function closeDB(){
        mysql_connect($dbhandle);
    }

?>
