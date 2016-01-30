How to update the lab info on this wiki
========================================


Details about Hosted Community OPNFV Test Labs are located in 3 different places:

 - Summarized on the OPNFV wiki [[start#opnfv_community_labs|Start Page]]
 - Overview with additional details on the [[pharos#opnfv_test_labs|Pharos Test Bed Governance Project Page]]
 - With Project specific information on each project page


How to update the Start Page
-----------------------------

* Clone the Pharos Git repository and make the changes::

 git clone ssh://<lfid>@gerrit.opnfv.org:29418/pharos

 vi docs/pharos.rst
 # use the below guide for MAP

 git add docs/pharos.rst

 git commit --signoff
 # use the proper commit message & include JIRA id

 git review -v
 # go to gerrit web and add reviewers, wait to have it merged
 # after code gets merged http://artifacts.opnfv.org/pharos/docs/pharos.html will contain your change

 # edit Wiki page https://wiki.opnfv.org/pharos and look for {{scrape>http://artifacts.opnfv.org/pharos/docs/pharos.html}}
 # click "Preview" and see if your change is shown; if shown add a short "Edit summary" and click "Save"
 # This must be done as Wiki does not auto update content for now

* You will see a section of code as shown below. Add your page to the bullet list with wiki link, nice name, and location summary


How to update the map info on the Pharos Project Page
------------------------------------------------------

  * Login and edit the OPNFV wiki [[pharos#opnfv_test_labs|Pharos Project Page]]
  * You will see a section of code as shown below. Add your page to the list with a comma separated list as follows:
    * longitude
    * latitude
    * .8 <- for size
    * marker color png ([[marker-green.png|marker-green.png]], [[marker-blue.png|marker-blue.png]], [[marker-red.png|marker-red.png]], [[marker-gold.png|marker-gold.png]])
    * Nice Format Lab Name
    * '';''
    * Location Summary
    * ''\\'' <-- for a new line
    * external link: <-- optional

MAP::

 <olmap id="olMapOne" width="800px" height="200px" lat="45.0" lon="0.0" zoom="3" statusbar="1" toolbar="1" controls="1" poihoverstyle="0" baselyr="OpenStreetMap" gpxfile="" kmlfile="">
 50.0117,5.1287,-90,.8,marker-green.png,Pont de Barbouillons; Daverdisse \\ external link:
 39.90,116.35,60,.8,marker-red.png,China Mobile Labs;Beijing \\ external link:
 45.50,-73.66,60,.8,marker-blue.png,Ericsson Labs;Montreal \\
 34.26,108.97,60,.8,marker-green.png, Huawei Labs;Xi an \\
 45.53,-122.97,60,.8,marker-green.png,Intel Labs;Hillsboro \\
 48.75867,-3.45196,60,.8,marker-gold.png,Orange Labs;Lannion \\
 48.82,2.27,60,.8,marker-gold.png,Orange Labs;Paris \\
 [[http://test.com|test.com]] \\ internal link: [[::start]]\\ **DW Formatting**
 </olmap>


**Documentation tracking**

Revision: _sha1_

Build date:  _date_

