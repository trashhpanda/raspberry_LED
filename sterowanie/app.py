from flask import Flask, request, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)
led_pin = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

red = 17
green = 27
blue = 22

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

freq = 100

RED = GPIO.PWM(red, freq)
GREEN = GPIO.PWM(green, freq)
BLUE = GPIO.PWM(blue, freq)


@app.route('/')
def index():
    RED.start(50)
    GREEN.start(50)
    BLUE.start(50)
    return render_template('index.html')


@app.route('/led/toggle')
def toggle_led():
    try:
        GPIO.output(led_pin, not GPIO.input(led_pin))
        status = 'On' if GPIO.input(led_pin) else 'Off'
        return {'success': True, 'status': status}
    except Exception as e:
        print('Error:', e)
        return {'success': False}


@app.route('/rgb', methods=['POST'])
def change_rgb():
    red = int(request.json['red'])
    green = int(request.json['green'])
    blue = int(request.json['blue'])
    
    try:
        RED.ChangeDutyCycle(red)
        GREEN.ChangeDutyCycle(green)
        BLUE.ChangeDutyCycle(blue)
    except Exception as e:
        print('Error:', e)
    
    return {"red": red, "green": green, "blue": blue}


if __name__ == '__main__':
    app.run(host='192.168.1.53', port=5000, debug=True)
