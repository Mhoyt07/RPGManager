import functools
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "change-me"  # needed for sessions

# temporary user for testing
DUMMY_USER = {"username": "gm", "password": "secret"}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            # optional: remember where to go back to
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        next_url = request.form.get("next")

        if username == DUMMY_USER["username"] and password == DUMMY_USER["password"]:
            session["user"] = username
            session["logged_in"] = True
            if next_url:
                return redirect(next_url)
            return redirect(url_for("dashboard"))
        else:
            # later: flash a message
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
   print("Rendering dashboard")
   return render_template("dashboard.html", active_tab='dashboard')  # uses base_app

@app.route("/characters")
@login_required
def characters():
    return render_template("character.html", active_tab='characters')

@app.route("/campaigns")
@login_required
def campaigns():
    return "Campaigns Page - Under Construction"

@app.route("/settings")
@login_required
def settings():
    return "Settings Page - Under Construction"

@app.route("/logout")
def logout():
    print("Logging out user")
    session.pop("user", None)
    session.pop("logged_in", None)
    print(f"Session data: {session}")
    return redirect(url_for("login"))
