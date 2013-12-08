from flask import Flask

app = Flask(__name__)
app.secret_key = 'wahoowa'

from app import views
