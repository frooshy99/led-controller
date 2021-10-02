# Super Awesome LED Controller
some change

Custom website to control magic and lifx leds without needing the internet. 


This will allow you to put the un-trusted LED controllers on a LAN only VLAN to prevent external internet access and only allow inbound connections from the one controller. 


### Building

`docker build -t led-controller .`


#### Running

`docker run --rm -p 8080:8080 led-controller:latest`

### Usage

Go to `http://localhost:8080` and use the webpage
