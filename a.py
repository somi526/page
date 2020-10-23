import requests
import json
import os
import sqlite3
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from users import User

GOOGLE_CLIENT_ID = "576471339248-pjaq07ir9esv1ql5hiaci66qoivgcm6r.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET ="mTMTs9KRoAvSQ55Eqe636Irz"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)



def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def login():
    # Find out what URL to hit for Google login
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

login()