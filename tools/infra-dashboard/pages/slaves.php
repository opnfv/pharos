<script type="text/javascript">
    $(document).ready(function() {
        $('#example').DataTable( {
            "order": [[ 2, "desc" ], [ 1, "desc" ]]
        } );
    } );
</script>

<?php
    include '../utils/jenkinsAdapter.php';
    $array = $SLAVES->xpath('computer');

    echo '<table id="example" class="table table-striped table-bordered" cellspacing="0" width="100%">';
    echo "<thead>";
    echo "<tr>";
    echo "<th>Slave name</th>";
    echo "<th>Status</th>";
    echo "<th>Current build</th>";
    echo "</tr>";
    echo "</thead>";
    echo "<tbody>";
    foreach ($array as &$value) {

        $slave = $value->displayName;
        $idle = $value->idle;
        $slave_url = getSlaveUrl($slave);
        $status = getSlaveStatus($slave);

        if ($status == "online" and $idle == "true") {
            $status = "online / idle";
            $color = "#C8D6C3";
        }
        else if ($status == "online") $color = "#BEFAAA";
        else $color = "#FAAAAB";

        $job_name = "";
        $job_url = "";
        $job_scenario = "";


        if ($status == 'online') {
            $job_params = getJJob($slave);
            $job_name = $job_params['name'];
            $job_url = $job_params['url'];
            $job_scenario = $job_params['scenario'];
        }

        echo "<tr>";
        echo "<th><a target='_blank' href='".$slave_url."'>".$slave."</a></th>";

        echo "<th style='background-color: ".$color.";'>".$status."</th>";
        echo "<th><a class='blink_me' style='font-size:12px;color:#33cc00;' target='_blank' href='".$job_url."'>".$job_name."</a></th>";

        echo "</tr>";
    }
    echo '</tbody>';
    echo '</table>';
?>
