from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def get_public_ip():
    # Get the public IP from API
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json().get('ip', 'Unable to fetch IP')

    # displays the html page for the app with the value of the IP address obtained from the API.
    return render_template("index.html", ip=ip)

@app.route('/health')
def health():
    return 'OK', 200
