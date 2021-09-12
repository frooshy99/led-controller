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


<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">

    <title>LED Controller</title>
  </head>
  <body>

  <!--
      <div class="container">
          <h1>RGB LED Settings</h1>



        <div class="card text-center">
          <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs" id="pills3-tab" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" id="led1-power" data-bs-toggle="pill" data-bs-target="#led1-power-content" type="button" role="tab" aria-controls="led1-power-content" aria-selected="true">Power</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="led1-color" data-bs-toggle="pill" data-bs-target="#led1-color-content" type="button" role="tab" aria-controls="led1-color-content" aria-selected="false">Color</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="led1-effect" data-bs-toggle="pill" data-bs-target="#led1-effect-content" type="button" role="tab" aria-controls="led1-effect-content" aria-selected="false">Efects</button>
              </li>
            </ul>
          </div>

          <div class="card-body tab-content" id="pills3-tabContent">

              <div class="tab-pane fade show active" id="led1-power-content" role="tabpanel" aria-labelledby="led1-power">
                  <form action="/api.php" method="post">
                      <input type="hidden" id="command" name="command" value="status">
                      <input type="hidden" id="powerState" name="powerState" value="<?php echo $isOn ? "0" : "1"; ?>">
                      <input type="hidden" id="deviceName" name="deviceName" value="rgb">

                    <button type="submit" class="btn btn-primary">Turn <?php echo $isOn ? "OFF" : "ON"; ?></button>
                  </form>
                </div>

              <div class="tab-pane fade" id="led1-color-content" role="tabpanel" aria-labelledby="led1-color">
                  cde
              </div>

              <div class="tab-pane fade" id="led1-effect-content" role="tabpanel" aria-labelledby="led1-effect">
                  <form action="/api.php" method="post">
                      <input type="hidden" id="command" name="command" value="mode">
                      <input type="hidden" id="deviceName" name="deviceName" value="rgb">

                      <input type="range" min="1" max="16" value="<?php echo "$speed"; ?>" class="slider" id="speed" name="speed">

                    <button type="submit" name="effect" value="SEVEN_COLOR_FADE" class="btn btn-primary">SEVEN_COLOR_FADE</button>
                    <button type="submit" name="effect" value="RED_GRADUAL" class="btn btn-primary">RED_GRADUAL</button>
                    <button type="submit" name="effect" value="rgb" class="btn btn-primary">Effect A</button>

                  </form>
                </div>
              </div>

          </div>
        </div>
    </div>
-->

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








    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
  </body>
</html>
