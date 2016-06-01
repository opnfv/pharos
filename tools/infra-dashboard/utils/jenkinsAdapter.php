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

    function parseJobString($str) {
        $scenario = '';
        $installer = '';
        $branch = '';
        $installers = array("fuel", "joid", "apex", "compass");
        $branches = array("master","arno", "brahmaputra", "colorado");
        $arr = split ('[ -]', $str);
        for($x = 0; $x < count($arr); $x++) {
            if (strcmp($arr[$x],"os") == 0)  //all the scenarios start with 'os'
                $scenario = $arr[$x].'-'.$arr[$x+1].'-'.$arr[$x+2].'-'.$arr[$x+3];
            else if (in_array($arr[$x], $installers))
                $installer = $arr[$x];
            else if (in_array($arr[$x], $branches))
                $branch = $arr[$x];
        }
        $arr2 = explode(' ', $str);
        $jobname = $arr2[0]; //take first word as job name

        return array(
            "jobname"=>$jobname,
            "installer"=>$installer,
            "branch"=>$branch,
            "scenario"=>$scenario
        );
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

                $params = parseJobString($fullDisplayName);

                $type = 0; // type=0 means the job is running
                $job_params = array(
                    "name"=>$params['jobname'],
                    "url"=>$url,
                    "scenario"=>$params['scenario'],
                    "installer"=>$params['installer'],
                    "branch"=>$params['branch'],
                    "type"=>$type
                );
                //print_r($job_params);
                return $job_params;

            }
            else { // there are NO active builds for this slave, we take the latest build
                //echo "NO Active builds";
                $builds = $ALL_BUILDS->xpath('job[lastBuild/building="false"][lastBuild/builtOn="'.$slave.'"]');
                $last_job  = simplexml_import_dom($builds[0]);
                //print_r($last_job);
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

                $params = parseJobString($fullDisplayName);

                $type = 3;
                if ($result == "SUCCESS") $type = 1; // type=1 means it's the last job and it succeded
                if ($result == "FAILURE") $type = 2; // type=2 means it's the last job and it failed
                if ($result == "UNSTABLE") $type = 3; // type=3 means it's the last job is unstable

                $job_params = array(
                    "name"=>$params['jobname'],
                    "url"=>$url,
                    "scenario"=>$params['scenario'],
                    "installer"=>$params['installer'],
                    "branch"=>$params['branch'],
                    "type"=>$type
                );

                return $job_params;
                //print_r($job_params);
            }

        }
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
