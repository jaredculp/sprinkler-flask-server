from app import app
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for

@app.route('/')
def show_dashboard():
    sprinklers = []
    sprinkler1 = {
        'name': 'name',
        'status': 'ON',
        'moisture': '#',
        'flow': '#'
    }
    sprinkler2= {
        'name': 'name',
        'status': 'OFF',
        'moisture': '#',
        'flow': '#'
    }
    sprinklers.append(sprinkler1)
    sprinklers.append(sprinkler2)
    return render_template('dashboard.html', sprinklers=sprinklers)

@app.route('/request/<head>/<request>')
def do_request(head, request):
    flash("Sprinkler %s received request to %s" % (head, request))
    return redirect(url_for('show_dashboard'))
