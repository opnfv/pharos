.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.


.. _pharos_wiki:

*************************
Updating Pharos Documents
*************************

Details about each Community Lab is found in 3 places:

 - Summary of lab including location, contacts, status, etc.
   on the `Pharos Project Wiki page <https://wiki.opnfv.org/display/pharos>`_
 - Lab specific details are provided with dedicated Wiki pages,
   see this `Example Lab <https://wiki.opnfv.org/display/pharos/Intel+Hosting>`_
 - Pharos repo docs ...

    - docs/information/pharos.rst ... project information file
    - docs/labs/ ... Lab documents (includes lab specific capabilities, usages and policies;
      POD information)
    - docs/labs/images/ ... Lab and POD toplogies

Update Pharos repo
------------------

Clone the Pharos Git repository

 * Make the changes to Pharos project information file (docs/information/pharos.rst)
 * After code gets merged http://artifacts.opnfv.org/pharos/docs/information/pharos.html will
   contain your change


Update Pharos Wiki
------------------

Edit Wiki page

 * https://wiki.opnfv.org/pharos
 * Look for {{scrape>http://artifacts.opnfv.org/pharos/docs/information/pharos.html}}
 * Click "Preview" and see if your change is shown; if shown add a short "Edit summary" and click
   "Save" (Wiki does not auto update content)

You will see a section of code as shown below. Add your page to the bullet list with wiki link, nice
name, and location summary

Update the map info on the Pharos Project Page https://wiki.opnfv.org/pharos?&#community_labs

 * You will see a section of code as shown below. Add your lab infomation to the list with a comma
   separated list as follows:

    * longitude
    * latitude
    * .8 <- for size
    * marker color png ([[marker-green.png|marker-green.png]], [[marker-blue.png|marker-blue.png]],
      [[marker-red.png|marker-red.png]], [[marker-gold.png|marker-gold.png]])
    * Nice Format Lab Name
    * '';''
    * Location Summary
    * ''\\'' <-- for a new line
    * external link: <-- optional

.. MAP Code Example (see Wiki page for current version)::

MAP::

 <olmap id="olMapOne" width="877px" height="200px" lat="45.0" lon="0.0" zoom="3" statusbar="1" toolbar="1" controls="1"
 poihoverstyle="0" baselyr="OpenStreetMap" gpxfile="" kmlfile="">
 45.52,-122.67,60,.8,marker-red.png,Linux Foundation;Portland, Oregon \\ external link: [[http://www.test.com|test.com]]
 39.7392,-104.9902,60,.8,marker-red.png,Cable Labs;Denver, CA \\ external link: [[http://www.test.com|test.com]]
 37.333685,-121.891272,60,.6,marker-green.png,[[pharos/spirentvctlab|Spirent VCT Lab]] \\ San Jose, California
 39.90,116.35,60,.8,marker-red.png,China Mobile Labs;Beijing, China \\ external link: [[http://www.test.com|test.com]]
 37.413137,-121.977975,-180,.6,marker-red.png,Dell Labs;Santa Clara, California \\ link: [[https://wiki.opnfv.org/dell_hosting]]
 59.41,17.95,60,.8,marker-red.png,Enea Pharos Lab;Kista, Sweden \\ external link: [[http://www.enea.com/pharos-lab|ENEA pharos lab]]
 45.50,-73.66,60,.8,marker-blue.png,Ericsson Labs;Montreal, Canada \\ external link: [[http://www.test.com|test.com]]
 34.26,108.97,60,.8,marker-green.png, Huawei Labs;Xi an, China \\ external link: [[http://www.test.com|test.com]]
 37.373424,-121.964913,60,.8,marker-green.png, Huawei Labs;Santa Clara, USA \\ external link: [[http://www.test.com|test.com]]
 45.53,-122.97,60,.8,marker-green.png,Intel Labs;Hillsboro, Oregon \\ link: [[https://wiki.opnfv.org/get_started/intel_hosting|intel_hosting]]
 48.75867,-3.45196,60,.8,marker-gold.png,Orange Labs;Lannion, France \\ external link: [[http://www.test.com|test.com]]
 48.825786,2.274797,-60,.8,marker-gold.png,Orange Labs;Paris, France \\ external link: [[http://www.test.com|test.com]]
 31.97,118.79,60,.8,marker-red.png,ZTE Labs;Nan Jing, China \\ link:[[zte-nj-testlab|ZTE, Nan Jing]]
 [[http://test.com|test.com]] \\ internal link: [[::start]]\\ **DW Formatting**
 </olmap>
