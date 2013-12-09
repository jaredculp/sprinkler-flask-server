from app import app
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for

@app.route('/')
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
    return render_template('dashboard.html', sprinklers=sprinklers)

@app.route('/request/<head>/<request>')
def do_request(head, request):
    flash("Sprinkler %s received request to %s" % (head, request))
    return redirect(url_for('show_dashboard'))
