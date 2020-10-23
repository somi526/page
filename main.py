import requests
import json
import pyrebase
import sys, os
from flask import Flask
from oauthlib.oauth2 import WebApplicationClient
from api import get_students, get_problems
from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)
firebaseConfig = {
  "apiKey": "AIzaSyAIu3NQa8hdg_STYi65vGSIHkd3g-nkxp0",
  "authDomain": "seansdevnote-d14de.firebaseapp.com",
  "databaseURL": "https://seansdevnote-d14de.firebaseio.com",
  "projectId": "seansdevnote",
  "storageBucket": "seansdevnote.appspot.com",
  "messagingSenderId": "576471339248",
  "appId": "1:576471339248:web:9e28d0cc8815522a693235"
}
# fb = pyrebase.initialize_app(config = firebaseConfig)
#fb_auth = fb.auth()


GOOGLE_CLIENT_ID = "576471339248-pjaq07ir9esv1ql5hiaci66qoivgcm6r.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET ="mTMTs9KRoAvSQ55Eqe636Irz"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/", methods=["GET"])
def index():
    return render_template("home.html", posts={})
    
@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == 'POST':
        return render_template("admin.html", students=get_students(to_html=True, name=request.form["nm"]))
    else:
        return render_template("admin.html")

@app.route("/python", methods=["GET"])
def python():
    with open("data/python.json", "r") as read_file:
        data = json.load(read_file)
        posts = data["posts"]
    
    return render_template("home.html", posts=posts)

@app.route("/signin", methods=["POST", "GET"])
def signin():
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            fb_auth.sign_in_with_email_and_password(email, password)
            return redirect("/")
        except:
            return render_template("signup.html")
    else:
        return render_template("signin.html")
    """
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            fb_auth.create_user_with_email_and_password(email, password)
            return redirect("/")
        except:
            return render_template("signup.html")
    else:
        return render_template("signup.html")
    """
    return render_template("admin.html")

@app.route("/signout", methods=["POST", "GET"])
def signout():
    if "user" in session:
        del session["user"]
    return redirect(url_for("/"))

if __name__ == "__main__":
    #fb_auth.create_user_with_email_and_password("rbtmd1010@gmail.com", "Ghkdrb12@s")
    #fb_auth.sign_in_with_email_and_password("rbtmd1010@gmail.com", "Ghkdrb12@s")
    app.run(debug=True)