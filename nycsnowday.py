from flask import Flask, render_template, request, url_for,redirect,session
import pyowm
from time import strftime
from pytz import timezone
app = Flask(__name__)
tz = timezone('EST')
owm = pyowm.OWM('ceb7be6f8da5256b6ec3ef530031eefd')
f = owm.three_hours_forecast('nyc')
time = pyowm.timeutils.tomorrow()
f = f.get_weather_at(time)
s = f.get_snow()
chance = 60
time2 = time.strftime("%A %B %d")
message = str(time2) + ": "
def chan(c):
    chance = 0
    if c > 267:
        chance = 99
        message = "more than a foot of snow expected"
    elif c > 200:
        chance = 80
        message = "almost a foot of snow expected"
    elif c > 150:
        chance = 65
        message = "half a foot of snow expected"
    elif c > 75:
        chance = 54
        message = "a decent amount of snow expected"
    elif c > 20:
        chance = 15
        message = "some snow but not enough is expected"
    else:
        chance = 10
    return {'c':chance,'m':message}

if( 'all' not in s.keys() and '1h' not in s.keys() and '3h' not in s.keys()):
    chance = 5
    message += "no snow expected tomorrow"
elif ('all' in s.keys()):
    chance = chan(s['all'])['c']
    message += chan(s['all'])['m']
elif ('3h' in s.keys()):
    chance = chan(s['3h'])['c']
    message += chan(s['3h'])['m']
elif ('1h' in s.keys()):
    chance = chan(s['1h'])['c']
    message += chan(s['1h'])['m']

@app.route("/home/")
def home():
    return render_template('home.html')
@app.route("/")
def calc():
    return render_template('calc.html', cnce = chance, messg = message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
	
