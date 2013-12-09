import json
import time
import urllib2

from app import app
from app import db
from models import Sprinkler 
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for
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
    updated_at = time.strftime("%c")
    sprinklers_list = []

    sprinklers = Sprinkler.query.all()
    for sprinkler in sprinklers:
        sprinklers_list.append(sprinkler)

    weather = False

    if request.method == "POST":
        weather = show_weather(request.form['location'])

    return render_template('dashboard.html', sprinklers=sprinklers_list,
                                             weather=weather,
                                             updated_at=updated_at)

@app.route('/add', methods=['POST'])
def add_sprinkler():
    if request.method == "POST":
        name = request.form['name']
        status = request.form['status']
        sprinkler = Sprinkler(name=name, status=status, flow='0', moisture='0')
        db.session.add(sprinkler)
        db.session.commit()
        flash("Sprinkler %s was created and set to %s" % (name, status))
        return redirect(url_for('show_dashboard'))

@app.route('/delete/<head>')
def delete_sprinkler(head):
    sprinkler = Sprinkler.query.get(head)
    db.session.delete(sprinkler)
    db.session.commit()
    flash("Sprinkler %s was deleted" % sprinkler.name)
    return redirect(url_for('show_dashboard'))

@app.route('/deleteAll')
def delete_all_sprinklers():
    sprinklers = Sprinkler.query.all()
    for sprinkler in sprinklers:
        db.session.delete(sprinkler)

    db.session.commit()
    flash("All sprinklers deleted")
    return redirect(url_for('show_dashboard'))


@app.route('/request/<head>/<request>')
def do_request(head, request):
    s = Sprinkler.query.get(head)
    if request.lower() == "on":
        s.turn_on()
    elif request.lower() == "off":
        s.turn_off()
    elif request.status() == "status":
        s.get_status()
    flash("Sprinkler %s received request to %s" % (s.name, request))
    return redirect(url_for('show_dashboard'))
