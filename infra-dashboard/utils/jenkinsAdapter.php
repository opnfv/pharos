<?php

    function getSlaves() {
        $query="https://build.opnfv.org/ci/computer/api/xml?tree=computer[displayName,offline,idle]";
        $output =  file_get_contents($query);
        $xml = simplexml_load_string($output);
        if ($xml) return $xml;
        else return "";
    }

    function getCiSlaves(){
        $query="https://build.opnfv.org/ci/label/ci-pod/api/xml?xpath=labelAtom/node[nodeName]&wrapper=nodes";
        $output =  file_get_contents($query);
        $xml = simplexml_load_string($output);
        if ($xml) return $xml;
        else return "";
    }

    function getAllBuilds(){
        $query="https://build.opnfv.org/ci/api/xml?tree=jobs[displayName,url,lastBuild[fullDisplayName,building,builtOn,timestamp,result]]";
        $output =  file_get_contents($query);
        $xml = simplexml_load_string($output);
        if ($xml) return $xml;
        else return "";
    }

    $SLAVES = getSlaves();
    $CI_PODS = getCiSlaves();
    $ALL_BUILDS = getAllBuilds();

    function getActiveBuilds() {
        global $ALL_BUILDS;
        //$query="https://build.opnfv.org/ci/api/xml?tree=jobs[displayName,url,lastBuild[fullDisplayName,building,builtOn,timestamp]]&xpath=hudson/job[lastBuild/building=%27true%27]&wrapper=hudson";
        $xml = $ALL_BUILDS->xpath('job[lastBuild/building="true"]');
        if ($xml) return $xml;
        else return "";
    }

    $ACTIVE_BUILDS = getActiveBuilds();

    function slaveExists($slave) {
        global $SLAVES;
        $slave = $SLAVES->xpath('computer[displayName="'.$slave.'"]');
        if ($slave) return true;
        else return false;
    }

    function getSlaveStatus($slave) {
        global $SLAVES;
        $status = "unknown";
        if (!slaveExists($slave)) return $status;
        $slave = $SLAVES->xpath('computer[displayName="'.$slave.'"]');
        $offline = $slave[0]->offline;

        if ($offline == "true") $status = "offline";
        else $status = "online";
        return $status;
    }

    function getSlaveUrl($slave) {
        if (slaveExists($slave)) return "https://build.opnfv.org/ci/computer/".$slave;
        else return "";
    }


    function isCiPod($slave) {
        global $CI_PODS;
        $result = $CI_PODS->xpath('node[nodeName="'.$slave.'"]');
        if ($result) return true;
        else return false;
    }

    function isDevPod($slave) {
        global $CI_PODS;
        if (isCiPod($slave)) return false;
        else if (strpos($slave, 'pod') !== false)  return true;
        else return false;
    }


    function getJJob($slave) {
        global $ALL_BUILDS;
        if (!slaveExists($slave)) return "";

        //$builds = $ALL_BUILDS;
        //$xml = $ALL_BUILDS->xpath('job[lastBuild/building="true"][lastBuild/builtOn="'.$slave.'"]');
        $builds = $ALL_BUILDS->xpath('job[lastBuild/builtOn="'.$slave.'"]');
        if (! $builds) { //the slave does not have jobs in building state
            //echo "NO JOBS FOUND";
            return "";
        }
        else {
            //is there any active build?
            $builds = $ALL_BUILDS->xpath('job[lastBuild/building="true"][lastBuild/builtOn="'.$slave.'"]');
            if ($builds) { // there are active builds for this slave
                //print_r($builds);

                $child_job  = simplexml_import_dom($builds[0]);
                foreach ($builds as &$build) {
                    $int1 = intval($build->lastBuild->timestamp);
                    $int2 = intval($child_job->lastBuild->timestamp);
                    if ($int1 > $int2) {
                        $child_job  = simplexml_import_dom($build);
                    }
                }
                $url = strval($child_job->url);
                $fullDisplayName = $child_job->lastBuild->fullDisplayName;
                //echo $fullDisplayName."<br>";
                $arr = explode(' ', $fullDisplayName);
                $name = $arr[0];
                $scenario = array_pop($arr);
                if (strlen($scenario) < 10) $scenario = "?";

                $arr2 = explode('-', $name);
                $installer = "?";
                $branch = "?";
                $installers = array("fuel", "joid", "apex", "compass");
                $branches = array("master","arno", "brahmaputra", "colorado");

                foreach ($arr2 as &$element) {
                    if (in_array($element, $installers)) $installer = $element;
                }

                foreach ($arr2 as &$element) {
                    if (in_array($element, $branches)) $branch = $element;
                }

                $type = 0; // type=0 means the job is running
                $job_params = array(
                    "name"=>$name,
                    "url"=>$url,
                    "scenario"=>$scenario,
                    "installer"=>$installer,
                    "branch"=>$branch,
                    "type"=>$type
                );
                //print_r($job_params);
                return $job_params;

            }
            else { // there are NO active builds for this slave, we take the latest build
                //echo "NO Active builds";
                $builds = $ALL_BUILDS->xpath('job[lastBuild/building="false"][lastBuild/builtOn="'.$slave.'"]');
                //print_r($builds_slave);
                $last_job  = simplexml_import_dom($builds[0]);

                foreach ($builds as &$build) {
                    $int1 = intval($build->lastBuild->timestamp);
                    $int2 = intval($last_job->lastBuild->timestamp);
                    if ($int1 > $int2) {
                        $last_job  = simplexml_import_dom($build);
                    }
                }

                $url = strval($last_job->url);
                $result = strval($last_job->lastBuild->result);
                $fullDisplayName = $last_job->lastBuild->fullDisplayName;

                //echo $fullDisplayName."<br>";
                $arr = explode(' ', $fullDisplayName);
                $name = $arr[0];
                $scenario = array_pop($arr);
                if (strlen($scenario) < 10) $scenario = "?";

                $arr2 = explode('-', $name);
                $installer = "?";
                $branch = "?";
                $installers = array("fuel", "joid", "apex", "compass");
                $branches = array("master","arno", "brahmaputra", "colorado");

                foreach ($arr2 as &$element) {
                    if (in_array($element, $installers)) $installer = $element;
                }

                foreach ($arr2 as &$element) {
                    if (in_array($element, $branches)) $branch = $element;
                }

                $type = 3;
                if ($result == "SUCCESS") $type = 1; // type=1 means it's the last job and it succeded
                if ($result == "FAILURE") $type = 2; // type=2 means it's the last job and it failed
                if ($result == "UNSTABLE") $type = 3; // type=3 means it's the last job is unstable

                $job_params = array(
                    "name"=>$name,
                    "url"=>$url,
                    "scenario"=>$scenario,
                    "installer"=>$installer,
                    "branch"=>$branch,
                    "type"=>$type
                );
                return $job_params;
                //print_r($job_params);
            }

        }
    }


    function getJJob2($slave) {
        global $ACTIVE_BUILDS;
        if (!slaveExists($slave)) return "";
        /*
        else {
            $job_params = array(
                "name"=>"test",
                "url"=>"test",
                "scenario"=>"test",
                "installer"=>"test",
                "branch"=>"test"
            );

            return $job_params;
        }
        */

        $builds = $ACTIVE_BUILDS;

        $index1 = 0;
        $index2 = 0;
        $timestamp = 0;
        $hasActivebuild=false;
        foreach ($builds as &$build) {
            /*
            echo "<br>";
            echo "<br>";
            echo "index1= ".$index1."<br>";
            */
            $builtOn = $build->lastBuild->builtOn;
            //echo "builtOn= ".$builtOn."<br>";
            if (strcmp ($builtOn , $slave) == 0) {
                $hasActivebuild=true;
                //echo "Timestamp=".$build->lastBuild->timestamp."<br>";
                if (intval($build->lastBuild->timestamp) > intval($timestamp)) {
                    //the job with the higher timestamp will be the child
                    $timestamp = $build->lastBuild->timestamp;
                    $index2 = $index1;
                }
            }
            $index1 += 1;
        }
        /*
        echo "<br><br><br>";
        echo "index1= ".$index1."<br>";
        echo "index2= ".$index2."<br>";
        echo "<br><br><br>";
        */

        if ($hasActivebuild) {
            $url = $builds[$index2]->url;
            $fullDisplayName = $builds[$index2]->lastBuild->fullDisplayName;

            $arr = explode(' ', $fullDisplayName);
            $name = $arr[0];
            $scenario = array_pop($arr);

            $arr2 = explode('-', $name);
            $installer = $arr2[0];
            $installers = array("fuel", "joid", "apex", "compass");
            if (! in_array($installer, $installers)) {
                $installer = $arr2[1];
            }
            $branch = array_pop($arr2);

            $job_params = array(
                "name"=>$name,
                "url"=>$url,
                "scenario"=>$scenario,
                "installer"=>$installer,
                "branch"=>$branch
            );

            return $job_params;

        } else return "";
    }

    /*
    $slave = "lf-pod2";
    $job_params = getJJob($slave);

    $status = getSlaveStatus($slave);
    echo "Status slave ".$slave.": ".$status."<br>";
    echo "Job: ".$job_params['name']."<br>";
    echo "URL: ".$job_params['url']."<br>";
    echo "Scenario: ".$job_params['scenario']."<br>";
    echo "Installer: ".$job_params['installer']."<br>";
    echo "Branch: ".$job_params['branch']."<br>";
    echo "Type: ".$job_params['type']."<br>";
    */

?>
