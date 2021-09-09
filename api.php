<?php
    $red = ($color & 0xFF0000 )>> 16;
    $green = ($color & 0x00FF00 ) >> 8;
    $blue = $color & 0x0000FF ;


    if ($_SERVER["REQUEST_METHOD"] == "POST")
    {
        $command = $_POST["command"];
        $device = $_POST["deviceName"];


        if ($command == "color") {

            if ($device == "rgb") {
                $color = substr($_POST["color"], 1);
                $color = ctype_xdigit($color) ? intval($color, $base=16) : 0;

                $red = ($color & 0xFF0000)>> 16;
                $green = ($color & 0x00FF00) >> 8;
                $blue = $color & 0x0000FF;

                exec("./magic.py -H 192.168.107.7 color ${red} ${green} ${blue}");
            } elseif ($device == "lifx") {
                $brightness = $_POST["brightness"];
                $temp = $_POST["temp"];

                exec("./lifx.py -H '192.168.107.9' -M 'd0:73:d5:3d:00:92' color ${brightness} ${temp}");
            }


        } elseif ($command == "status") {

            $status = $_POST["powerState"] == "1" ? "on" : "off";

            if ($device == "rgb") {
                exec("./magic.py -H 192.168.107.7 ${status}");
            } elseif ($device == "lifx") {
                exec("./lifx.py -H '192.168.107.9' -M 'd0:73:d5:3d:00:92' ${status}");
            }

        } elseif($command == "mode"){
            $mode = $_POST["mode"];
            $speed = $_POST["speed"];
            exec("./magic.py -H 192.168.107.7 mode ${mode} ${speed}");
        }

        header('Location: /');
    } else {
        
    }
