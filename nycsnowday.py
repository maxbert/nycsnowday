from flask import Flask, render_template, request, url_for,redirect,session
from datetime import datetime
import pyowm
import time, urllib2, json, random
from pytz import timezone
app = Flask(__name__)
print('hello')
def chance():
    timer = datetime.now(timezone('US/Eastern'))
    t = timer.strftime('%Y%m%d')
    print t
    key1 = '01c3a565d8bfd31d'
    key2 = '70c45a24ed3df2db'
    key3 = '7e093a11e58f2fce'
    key4 = 'b3e69313dedbe821'
    key5 = 'dbdf167060b3fc73'
    a = random.randint(1,3)
    b = random.randint(1,3)
    if (a == 1):
        keya = key1
    if (a == 2):
        keya = key2
    if (a == 3):
        keya = key3
    if (a ==4 ):
        keya = key4
    if(b == 1):
        keyb = key1
    if(b == 2):
        keyb = key2
    if(b ==3):
        keyb = key3
    if(b ==4):
        keyb = key4

    f = urllib2.urlopen('http://api.wunderground.com/api/' + keya + '/history_' + t + '/q/NY/nyc.json')
    j = json.loads(f.read())
    snowalready = float(j['history']['dailysummary'][0]['snowfalli'])
    f = urllib2.urlopen('http://api.wunderground.com/api/' + keyb + '/forecast/q/NY/nyc.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    snowtoday = parsed_json['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['in']
    snowtomorrow = parsed_json['forecast']['simpleforecast']['forecastday'][1]['snow_allday']['in']
    f.close()
    currsnow = False        
    tz = timezone('EST')
    owm = pyowm.OWM('ceb7be6f8da5256b6ec3ef530031eefd')
    f = owm.daily_forecast('nyc')
    time1 = pyowm.timeutils.tomorrow()
    f = f.get_weather_at(time1)
    s = f.get_snow()
    f2 = owm.weather_at_place('nyc')
    f2 = f2.get_weather()
    s3 = f.get_snow()
    chance = 60
    rand = random.randint(0,5)
    time.timezone =tz
    time2 = timer.strftime("%A %B %d")
    message = str(time2) + ": "
    addchance = 0
    if(f2.get_status() == "Snow"):
        currsnow = True
    else:
        currsnow = False

    c = snowtoday + snowtomorrow + snowalready
    print("snow tommorow - ")
    print(s)
    print("current conditions")
    print(f2)
    print("snow today")
    print(s3)
    if( currsnow == True):
        addchance = 15
        message += "It is snowing right now and "
    if(snowtoday + snowtomorrow + snowalready > 0):
        chance = chan(c * 25.4)['c'] + addchance + rand
        message += chan(c * 25.4)['m']
    else:
        chance = rand +addchance
        message += "no snow accumulation expected tomorrow"
    return {'c':chance,'m':message}
def chan(c):
    if c > 267:
        chance = 99
        message = "more than a foot of snow accumulation( " + str(c / 25.4) +" in) expected by tommorow"
    elif c > 200:
        chance = 80
        message = "almost a foot of snow accumulation ( " + str(c / 25.4) +" in) expected by tommorow"
    elif c > 150:
        chance = 65
        message = "half a foot of snow accumulation ( " + str(c / 25.4) +" in) expected by tommorow"
    elif c > 75:
        chance = 54
        message = "A decent amount of snow accumulation ( " + str(c / 25.4) +" in) expected by tommorow"
    elif c > 25.4:
        chance = 15
        message = "Some snow accumulation( " + str(c / 25.4) +" in) but not enough is expected by tommorow"
    else:
        chance = 10
        message = "Less than an inch of accumulation is expected by tommorow"
    return {'c':chance,'m':message}

@app.route("/home/")
def home():
    return render_template('home.html')
@app.route("/")
@app.route("/defaultsite/")
def calc():
    return render_template('calc.html', cnce = chance()['c'], messg = chance()['m'])

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)
	
