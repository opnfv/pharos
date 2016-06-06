<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>OPNFV Pharos Dashboard | OPNFV</title>
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" type="text/css" />
        <link rel="stylesheet" href="./css/dataTables.bootstrap.min.css" type="text/css" />
        <script src="//code.jquery.com/jquery-1.10.2.js"></script>
        <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
        <script src="http://www.itsyndicate.ca/gssi/jquery/jquery.crypt.js"></script>
        <script src="https://cdn.datatables.net/1.10.11/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.10.11/js/dataTables.bootstrap.min.js"></script>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css"/>

        <link rel="stylesheet" href="./css/template.css" type="text/css" />
        <link rel="stylesheet" href="./css/theme.css" type="text/css" />
        <link rel="stylesheet" href="./css/opnfv.css" type="text/css" />

        <link href='./css/fullcalendar.css' rel='stylesheet' />
        <link href='./css/fullcalendar.print.css' rel='stylesheet' media='print' />
        <script src='./js/moment.min.js'></script>
        <script src='./js/fullcalendar.js'></script>


        <style>
            fieldset { padding:0; border:0; margin-top:15px; }
            input.text { margin-bottom:2px; width:90%; padding: .2em; font-size:14px; }
            input { display:block; font-size:14px; }
            label {font-size:14px;}
            .ui-dialog .ui-state-error { padding: .3em; }
            .validateTips { border: 1px solid transparent; padding: 0.3em; }
            .booked_day span {
                color: red !important; /* should only apply to may 6 and 8 */
            }
        </style>

        <script type="text/javascript">
            $(document).ready(function() {

                function getParameterByName(name, url) {
                    if (!url) url = window.location.href;
                    name = name.replace(/[\[\]]/g, "\\$&");
                    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                        results = regex.exec(url);
                    if (!results) return null;
                    if (!results[2]) return '';
                    return decodeURIComponent(results[2].replace(/\+/g, " "));
                }

                function selectTab(name) {
                    $("#container").empty();
                    var imgName = './media/ajax-loader.gif';
                    document.getElementById('container')
                        .innerHTML = '<img style="position: relative;left: 50%;" src="' + imgName + '" />';
                    if (name == "devpods") {
                        $( "#btn_cipods" ).addClass( "noselected" );
                        $( "#btn_devpods" ).removeClass( "noselected" );
                        $( "#btn_slaves" ).addClass( "noselected" );
                        var key = Math.random();
                        $("#container").load("pages/dev_pods.php?key="+key);
                        $('#hd_page').attr('value', "devpods");
                    }
                    else if (name == "slaves") {
                        $( "#btn_cipods" ).addClass( "noselected" );
                        $( "#btn_devpods" ).addClass( "noselected" );
                        $( "#btn_slaves" ).removeClass( "noselected" );
                        $("#container").load("pages/slaves.php");
                        $('#hd_page').attr('value', "slaves");
                    }
                    else {
                        $( "#btn_cipods" ).removeClass( "noselected" );
                        $( "#btn_devpods" ).addClass( "noselected" );
                        $( "#btn_slaves" ).addClass( "noselected" );
                        $("#container").load("pages/ci_pods.php");
                        $('#hd_page').attr('value', "cipods");
                    }
                }


                var page = getParameterByName('page');
                if      (page == "devpods")  selectTab("devpods");
                else if (page == "slaves")  selectTab("slaves");
                else                         selectTab("cipods");


                $( "#btn_cipods" ).click(function() {
                    selectTab("cipods");
                });
                $( "#btn_devpods" ).click(function() {
                    selectTab("devpods");
                });
                $( "#btn_slaves" ).click(function() {
                    selectTab("slaves");
                });
            } );



            $(function() {
                var dialog, form,
                login_email = $( "#login_email" ),
                login_password = $( "#login_password" ),
                allFields = $( [] ).add( login_email ).add( login_password ),
                emailRegex = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

                function checkLength( o, n, min, max ) {
                  if ( o.val().length > max || o.val().length < min ) {
                    o.addClass( "ui-state-error" );
                    return false;
                  } else {
                    return true;
                  }
                }

                function checkRegexp( o, regexp, n ) {
                  if ( !( regexp.test( o.val() ) ) ) {
                    o.addClass( "ui-state-error" );
                    return false;
                  } else {
                    return true;
                  }
                }


                function login() {
                    var valid = true;
                    email = $( "#login_email" );
                    password = $( "#login_password" );
                    allFields.removeClass( "ui-state-error" );

                    valid = valid && checkLength( email, "email", 6, 80 );
                    valid = valid && checkLength( password, "password", 5, 16 );

                    valid = valid && checkRegexp( email, emailRegex, "eg. ui@jquery.com" );
                    valid = valid && checkRegexp( password, /^([0-9a-zA-Z])+$/, "Password field only allow : a-z 0-9" );


                    if ( valid ) {
                        var email =  $('#login_email').val();
                        var password = $('#login_password').val();
                        var passwordMD5 = $().crypt({
                            method: "md5",
                            source: password
                        });
                        $.ajax({
                            type: 'POST',
                            url: "utils/login.php",
                            data: {action: 'login', email: email, password: passwordMD5},
                            success: function(data){
                                //alert(data);
                                json = JSON.parse(data);
                                if (json.result == 1) {
                                    alert("Wrong password.")
                                } else if (json.result == 2){
                                    alert("User not registered.")
                                } else {
                                    var page =  $('#hd_page').val();
                                    location.href = location.protocol + '//' + location.host + location.pathname + "?page=" + page;
                                }
                            },
                            error: function(data){
                                alert(data)
                            }
                        });

                    }
                }

                dialog_login = $( "#dialog-login" ).dialog({
                    autoOpen: false,
                    height: 225,
                    width: 400,
                    modal: true,
                    resizable:false,
                    buttons: {
                        "Login": login,
                        Cancel: function() {
                            dialog_login.dialog( "close" );
                        }
                    },
                    close: function() {
                        form[ 0 ].reset();
                        allFields.removeClass( "ui-state-error" );
                    }
                });

                form = dialog_login.find( "form" ).on( "submit", function( event ) {
                    event.preventDefault();
                    login();
                });


                $( "#login_text" ).on( "click", function() {
                    dialog_login.dialog( "open" );
                });

                $( "#logout" ).on( "click", function() {
                    $.ajax({
                        type: 'POST',
                        url: "utils/login.php",
                        data: {action: 'logout'},
                        success: function(data){
                            var page =  $('#hd_page').val();
                            location.href = location.protocol + '//' + location.host + location.pathname + "?page=" + page;
                        },
                        error: function(data){
                            alert(data)
                        }
                    });
                });
            });
        </script>
    </head>


    <body>

        <?php
            session_start();
        ?>

        <div class="collaborative-projects">
            <div class="gray-diagonal">
                <div class="container">
                    <a id="collaborative-projects-logo" href="http://collabprojects.linuxfoundation.org">Linux Foundation Collaborative Projects</a>
                </div>
            </div>
        </div>


        <div id="menu">
            <nav class="navbar navbar-default" role="navigation">
                <div class="container">
                    <div class="navbar-header">
                        <a class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
                            <span class="sr-only">Toggle navigation</span>
                        </a>
                        <a class="navbar-brand" href="https://www.opnfv.org/" title="OPNFV">
                            <img src="https://www.opnfv.org/sites/all/themes/opnfv/logo.png" alt="OPNFV" />
                        </a>
                    </div>
                    <div class="collapse navbar-collapse">
                        <div id="menu-container">
                            <div id="menu-second" class="hidden-xs">
                                <ul class="nav navbar-nav pull-right">

                                    <li class="item-112">
                                        <a target="_blank" href="https://www.opnfv.org/" >About Us</a>
                                    </li>
                                    <li class="item-113 deeper dropdown">
                                        <a target="_blank" href="#" class="dropdown-toggle" data-toggle="dropdown">Dodumentation
                                            <span class="toggle-arrow"></span>
                                        </a>
                                        <ul class="dropdown-menu" role="menu">
                                            <li class="item-121">
                                                <a target="_blank" href="http://artifacts.opnfv.org/pharos/docs/" >Pharos</a>
                                            </li>
                                            <li class="item-122">
                                                <a target="_blank" href="" >Releng</a>
                                            </li>
                                        </ul>
                                    </li>
                                    <li class="item-218">
                                        <a target="_blank" href="https://wiki.opnfv.org/" >OPNFV Wiki</a>
                                    </li>
                                    <li class="item-114">
                                        <a target="_blank" href="" >Contact</a>
                                    </li>
                                    <li class="item-112">
                                        <?php

                                            if (isset($_SESSION['user_id'])) {
                                                echo '<a style="cursor: pointer;" id="logout">Logout</a>';
                                            }
                                            else {
                                                echo '<a style="cursor: pointer;" id="login_text">Login</a>';
                                            }
                                        ?>

                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        </div>


        <div id="hs-component">
            <div class="container">
                <div id="wrap" class="sidebar-wrapper">
                    <div id="comp-menu" class="col-lg-12 col-md-12 col-sm-12 col-xs-12 hidden-xs">
                        <?php
                            if (isset($_SESSION['user_id'])) {
                                echo '<div style="float:right;text-align:right;top:0;margin-right:18px">';
                                echo 'current user: '.$_SESSION['user_name'];
                                echo '</div>';
                            }
                        ?>
                        <h2 class="demo-name">Pharos Infrastructure</h2>

                        <div class="btn-group theme">
                            <a id="btn_cipods" class="btn btn-theme noselected">CI PODs</a>
                            <a id="btn_devpods" class="btn btn-theme noselected">DEVELOPMENT PODs</a>
                            <a id="btn_slaves" class="btn btn-theme noselected">JENKINS SLAVES</a>
                        </div>

                        <div style="min-width: 310px; height: 2px; margin: 0 auto; background-color: #007E88"></div>
                        <div style="min-width: 310px; height: 20px; margin: 0 auto; background-color: #ffffff"></div>
                    </div>

                    <div id="container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
                </div>
            </div>
        </div>



        <div id="dialog-login" title="Login">
            <form>
                <table>
                    <tr>
                        <td><label for="login_email">Email</label></td>
                        <td><input type="text" label="Email" name="login_email" id="login_email" value="" size="30" class="text ui-widget-content ui-corner-all"/></td>
                    </tr>
                        <td><label for="login_password">Password</label></td>
                        <td><input type="password" name="login_password" id="login_password" size="30" value="" class="text ui-widget-content ui-corner-all"/></td>
                    <tr>
                    </tr>
                </table>
                <input type="submit" tabindex="-1" style="position:absolute; top:-100px"/>
            </form>
        </div>


        <div id="footer" style="float:bottom">
            <div class="container">
                <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                    <div id="zt-footer-copy">
                        Maintained by jose.lausuch@ericsson.com.
                    </div>
                </div>
            <div class="socials"></div>
        </div>

        <?php
            echo '<input type="hidden" id="hd_user_id" value="'.$_SESSION['user_id'].'"/>';
            echo '<input type="hidden" id="hd_user_email" value="'.$_SESSION['user_email'].'"/>';
            echo '<input type="hidden" id="hd_user_name" value="'.$_SESSION['user_name'].'"/>';
        ?>
        <input type="hidden" id="hd_page" value="cipods"/>

    </body>
</html>
