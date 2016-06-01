<script type="text/javascript">
    $(document).ready(function() {
        $('#example').DataTable( {
            "order": [[ 3, "desc" ],[ 2, "desc" ]]
        } );
    } );
</script>

<?php
    include '../utils/jenkinsAdapter.php';
    include '../utils/database.php';

    connectDB();
    $result = mysql_query("SELECT * FROM resource, pod WHERE resource.resource_id=pod.resource_id;");
    closeDB();

    echo '<table id="example" class="table table-striped table-bordered" cellspacing="0" width="100%">';
    echo "<thead>";
    echo "<tr>";
    echo "<th>Name</th>";
    echo "<th>Slave Name</th>";
    echo "<th>Status</th>";
    echo "<th>Installer</th>";
    echo "<th>Scenario</th>";
    echo "<th>Branch</th>";
    echo "<th>Job</th>";
    echo "</tr>";
    echo "</thead>";
    echo "<tbody>";

    while ($row = mysql_fetch_array($result)) {
        $slave = $row{'slavename'};
        if (! isCiPod($slave)) continue;

        $slave_url = getSlaveUrl($slave);
        $status = getSlaveStatus($slave);

        $job_name = "";
        $job_installer = "";
        $job_branch = "";
        $job_url = "";
        $job_scenario = "";
        $job_type = "";

        if ($status == 'online'){
            $job_params = getJJob($slave);
            $job_name = $job_params['name'];
            $job_installer = $job_params['installer'];
            $job_branch = $job_params['branch'];
            $job_url = $job_params['url']."lastBuild/consoleFull";
            $job_scenario = $job_params['scenario'];
            $job_type = $job_params['type'];
        }

        echo "<tr>";
        echo "<th><a target='_blank' href='".$row{'link'}."'>".$row{'name'}."</a></th>";
        echo "<th><a target='_blank' href='".$slave_url."'>".$slave."</a></th>";
        if ($status == "online") $color = "#BEFAAA";
        else $color = "#FAAAAB";
        echo "<th style='background-color: ".$color.";'>".$status."</th>";
        if ($job_type == "0") $class = "blink_me";
        else $class="";
        echo "<th class='".$class."'>".$job_installer."</th>";
        echo "<th class='".$class."'>".$job_scenario."</th>";
        echo "<th class='".$class."'>".$job_branch."</th>";
  $green = '#33cc00';
  $grey = '#646F73';
  $red = '#FF5555';
  $orange = '#EDD62B';
        if ($job_type == "0") { // job running
            echo "<th><a class='blink_me' style='font-size:12px;color:".$grey.";' target='_blank' href='".$job_url."'>".$job_name."</a></th>";
        }
        else if ($job_type == "1") {// last job successful
            echo "<th><a style='font-size:12px;color:".$green.";' target='_blank' href='".$job_url."'>".$job_name."</a></th>";
        }
        else if ($job_type == "2") {// last job failed
            echo "<th><a style='font-size:12px;color:".$red."' target='_blank' href='".$job_url."'>".$job_name."</a></th>";
        }
        else if ($job_type == "3") {// last job is unstable
            echo "<th><a style='font-size:12px;color:".$orange."' target='_blank' href='".$job_url."'>".$job_name."</a></th>";
  }
        else {
            echo "<th><a style='font-size:12px;' target='_blank' href='".$job_url."'>".$job_name."</a></th>";
        }
        echo "</tr>";
    }
    echo '</tbody>';
    echo '</table>';


?>
