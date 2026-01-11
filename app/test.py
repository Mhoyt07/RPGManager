from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "change-me"  # needed for sessions

# temporary user for testing
DUMMY_USER = {"username": "gm", "password": "secret"}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == DUMMY_USER["username"] and password == DUMMY_USER["password"]:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            # later: flash a message
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"Welcome, {session['user']}! (RPG dashboard here)"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
