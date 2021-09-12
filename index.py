from flask import Flask, render_template, request

from magic import ON, OFF, send_set_power, send_set_color, send_set_mode, send_get_status
from lifxlan import Light

app = Flask(__name__)


def getLifxStatus(mac, ip):
    try:
        light = Light(mac, ip)
        color = light.get_color()

        power = "off" if light.get_power() == 0 else "on"

        return {"type": 'lifx', "status":  power, "temp": color[3], "brightness": color[2]}
    except Exception:
         return {"type": 'lifx', "status":  "UNKNOWN", "temp": 0, "brightness": 0}

def getMagicStatus(ip):
    try:
        status = send_get_status(ip, 5577)

        modeDescription = "Solid Color" if status['mode'] == 0x61 else "Preset"
        color = '#' + ''.join('%02x'%i for i in [status['red'], status['green'], status['blue']])

        return {"type": 'magic', "status": status['power'], "sped": status['speed'], "color": color, "mode": modeDescription}
    except Exception:
        return {"type": 'magic', "status": "UNKNOWN", "sped": 0, "color": "#000000", "mode": "UNKOWN"}


def renderPage():
    ledObj1 = getLifxStatus('d0:73:d5:3d:00:92', '192.168.107.9')
    ledObj2 = getMagicStatus("192.168.107.7")

    leds = [ledObj1, ledObj2]

    return render_template('index.html', leds=leds)

@app.route("/")
def hello_world():
    return renderPage()


@app.route('/setLED', methods=['POST'])
def login():

    device = request.form['device']
    command = request.form['command']

    if command == "color":
        if device == "magic":
            color = int(request.form['color'][1:], base=16)

            red = (color & 0xFF0000)>> 16
            green = (color & 0x00FF00) >> 8
            blue = color & 0x0000FF

            send_set_color("192.168.107.7", 5577, (red, green, blue))

        elif device == "lifx":
            brightness = request.form['brightness']
            temp = int(request.form['temp'])

            light = Light('d0:73:d5:3d:00:92', '192.168.107.9')
            color = (0, 0, brightness, temp)
            light.set_color(color)


    elif command == "status":


        if device == "magic":
            status = ON if request.form['status'] == "on" else OFF
            send_set_power("192.168.107.7", 5577, status)
        elif device == "lifx":
            status = 65535 if request.form['status'] == "on" else 0

            light = Light('d0:73:d5:3d:00:92', '192.168.107.9')
            light.set_power(status)

    elif command == "mode":
        mode = int(request.form['mode'], base=16)
        speed = int(request.form['speed'])

        send_set_mode("192.168.107.7", 5577, mode, speed)

    return renderPage()
