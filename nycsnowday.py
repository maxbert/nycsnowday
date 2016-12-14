from flask import Flask, render_template, request, url_for,redirect,session
import pyowm
import time
from pytz import timezone
app = Flask(__name__)
def chance():
    tz = timezone('EST')
    owm = pyowm.OWM('ceb7be6f8da5256b6ec3ef530031eefd')
    f = owm.daily_forecast('nyc')
    time1 = pyowm.timeutils.tomorrow()
    f = f.get_weather_at(time1)
    s = f.get_snow()
    time3 = pyowm.timeutils.now()
    f2 = owm.weather_at_place('nyc')
    f2 = f2.get_weather()
    s2 = f.get_snow()
    f3 = owm.daily_forecast('nyc')
    f3 = f3.get_weather_at(time3)
    s3 = f3.get_snow()
    chance = 60
    time.timezone =tz
    time2 = time.strftime("%A %B %d")
    message = str(time2) + ": "
    addchance = 0
    
    if( f2.get_status() == "Snow"):
        addchance = 15
        message += "It is snowing right now and "
        
    if('all' in s.keys() and 'all' in s3.keys()):
        chance = chan((s['all'] + s3['all']))['c'] + addchance
        message += chan((s['all'] + s3['all']))['m']
        return {'c':chance,'m':message}
    elif('all' in s.keys()):
        chance = chan(s['all'] )['c'] + addchance
        message += chan(s['all'] )['m']
        return {'c':chance,'m':message}
    elif('all' in s3.keys()):
        chance = chan(s3['all'])['c'] + addchance
        message += chan(s['all'] )['m']
        return {'c':chance,'m':message}
    else:
        chance = 5 +addchance
        message += "no snow accumulation expected tomorrow"
        return {'c':chance,'m':message}
def chan(c):
    if c > 267:
        chance = 99
        message = "more than a foot of snow accumulation( " + c +" mm) expected by tommorow"
    elif c > 200:
        chance = 80
        message = "almost a foot of snow accumulation ( " + c +" mm) expected by tommorow"
    elif c > 150:
        chance = 65
        message = "half a foot of snow accumulation ( " + c +" mm) expected by tommorow"
    elif c > 75:
        chance = 54
        message = "a decent amount of snow accumulation ( " + c +" mm) expected by tommorow"
    elif c > 20:
        chance = 15
        message = "some snow accumulation( " + c +" mm) but not enough is expected by tommorow"
    else:
        chance = 10
        message = "less than an inch of accumulation is expected by tommorow"
    return {'c':chance,'m':message}

@app.route("/home/")
def home():
    return render_template('home.html')
@app.route("/")
@app.route("/defaultsite/")
def calc():
    return render_template('calc.html', cnce = chance()['c'], messg = chance()['m'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
	
