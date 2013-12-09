from app import app
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for
import urllib2, json
from flask import request

def show_weather(location):
    apikey = 'ab5c827e4a90cf97' #apikey, won't change
    url = 'http://api.wunderground.com/api/' + apikey + '/conditions/q/' + location + '.json'
    r = urllib2.urlopen(url)

    json_string = r.read()
    parsed_json = json.loads(json_string)
    weather = parsed_json['current_observation']['weather']
    temp_f = parsed_json['current_observation']['temp_f']
    relative_humidity = parsed_json['current_observation']['relative_humidity']
    precip_today_in = parsed_json['current_observation']['precip_today_in']
    zipcode = parsed_json['current_observation']['display_location']['zip']

    r.close();

    weather = {
        "zipcode" : zipcode,
        "weather" : weather,
        "temp" : temp_f,
        "humidity" : relative_humidity,
        "precipitation" : precip_today_in
    }
    return weather


@app.route('/', methods=['GET', 'POST'])
def show_dashboard():
    sprinklers = []
    sprinkler1 = {
        'name': 'Rear Lawn',
        'status': 'ON',
        'moisture': '80',
        'flow': '100'
    }
    sprinkler2= {
        'name': 'By Deck',
        'status': 'OFF',
        'moisture': '33',
        'flow': '50'
    }
    sprinklers.append(sprinkler1)
    sprinklers.append(sprinkler2)

    weather = False

    if request.method == "POST":
        weather = show_weather(request.form['location'])

    return render_template('dashboard.html', sprinklers=sprinklers, weather=weather)

@app.route('/request/<head>/<request>')
def do_request(head, request):
    flash("Sprinkler %s received request to %s" % (head, request))
    return redirect(url_for('show_dashboard'))
