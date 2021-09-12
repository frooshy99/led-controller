
<?php
    $red = ($color & 0xFF0000 )>> 16;
    $green = ($color & 0x00FF00 ) >> 8;
    $blue = $color & 0x0000FF ;


    if ($_SERVER["REQUEST_METHOD"] == "POST")
    {
        $command = $_POST["command"];
        $device = $_POST["device"];


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

            $status = $_POST["status"] == "on" ? "on" : "off";

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
    }
?>

<?php

    $results = exec("./magic.py -H 192.168.107.7 status --json");
    $a = json_decode($results);
    $color=65497;


    $command = $a->{"device_mode"};

    $isOn = $a->{"is_on"};

    $red = $a->{"color"}[0];
    $green = $a->{"color"}[1];
    $blue = $a->{"color"}[2];

    $mode = $a->{"device_mode"};
    $speed = $a->{"speed"};

   $color = ($red << 16) + ($green << 8) + $blue;


   # lifx
    $results = exec("./lifx.py -H '192.168.107.9' -M 'd0:73:d5:3d:00:92' status --json");
    $lifx_status = json_decode($results);

    $brightness = $lifx_status->{"brightness"};
    $temp = $lifx_status->{"temp"};
    $power = $lifx_status->{"device_power"};

?>

<!DOCTYPE html>
<html>
<head>
    <title>LED Controller</title>
</head>
<body>


 <h1>RGB LED Settings</h1>

 <h2>Status: <?php echo $isOn ? "ON" : "OFF"; ?></h2>
 <h2>Current mode: <?php echo $mode == "0x61" ? "Solid Color" : "Preset"; ?></h2>

<form action="/index.php" method="post">
  <input type="hidden" id="device" name="device" value="rgb">

  <select id="command" name="command">
    <option value="other">Select Command</option>
    <option value="color">color</option>
    <option value="status">status</option>
    <option value="mode">mode</option>
  </select>

  <select id="status" name="status">
    <option value="on">on</option>
    <option value="off">off</option>
    <option value="other">test</option>
  </select>

  <select id="mode" name="mode">
    <option value="0x25">SEVEN_COLOR_FADE</option>
    <option value="0x26">RED_GRADUAL</option>
    <option value="0x27">GREEN_GRADUAL</option>
    <option value="0x28">BLUE_GRADUAL</option>
    <option value="0x2C">WHITE_GRADUAL</option>
    <option value="0x2D">RED_GREEN_FADE</option>
    <option value="0x2E">RED_BLUE_FADE</option>
    <option value="0x2F">GREEN_BLUE_FADE</option>
    <option value="0x30">SEVEN_COLOR_STROBE</option>
    <option value="0x31">RED_STROBE</option>
    <option value="0x32">GREEN_STROBE</option>
    <option value="0x33">BLUE_STROBE</option>
    <option value="0x37">WHITE_STROBE</option>
    <option value="0x38">SEVEN_COLOR_JUMP</option>
  </select>
  <label for="color">Select color for the LED's:</label>
  <input type="color" id="color" name="color" value="#<?php printf ('%06s', dechex($color)); ?>"><br><br>


  <div class="slidecontainer">
  <label for="speed">Speed for the animation</label>
  <input type="range" min="1" max="16" value="<?php echo "$speed"; ?>" class="slider" id="speed" name="speed">
</div>

  <input type="submit">

</form>


<h1>LIFX LED Settings</h1>
<h2>Status: <?php echo $power; ?></h2>

<form action="/index.php" method="post">

  <input type="hidden" id="device" name="device" value="lifx">

  <select id="command" name="command">
    <option value="color">color</option>
    <option value="status">status</option>
  </select>

  <select id="status" name="status">
    <option value="on">on</option>
    <option value="off">off</option>
  </select>

  <div class="slidecontainer">
    <label for="brightness">brightness for the light</label>
    <input type="range" min="0" max="65535" value="<?php echo "$brightness"; ?>" class="slider" id="brightness" name="brightness">
  </div>

  <div class="slidecontainer">
    <label for="temp">color temp for the light</label>
    <input type="range" min="2500" max="9000" value="<?php echo "$temp"; ?>" class="slider" id="temp" name="temp">
  </div>

  <input type="submit">
</form>




</body>
