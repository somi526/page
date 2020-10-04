import sys, os
from flask import Flask
from api import get_students, get_problems
from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    if request.method == 'POST':
        data = request.get_json()
        session["user"] = request.form["nm"]
        print(data)

    if session.get('user', '') == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('main'))

@app.route("/admin", methods=["POST", "GET"])
def admin():
    return render_template("admin.html", students=get_students(to_html=True, name=request.form["nm"]))

@app.route("/main", methods=["POST", "GET"])
def main():
    return render_template("main.html", problems=get_problems(to_html=True, student=session.get("user", None)))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "user" in session:
        del session["user"]
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run()