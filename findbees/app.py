from datetime import timedelta
from flask import Flask, render_template, redirect, request, session, abort
from flask.helpers import url_for
from sheets import Worksheet, get_or_assign_pick

app = Flask(__name__)
app.secret_key = "There once was a man..."
app.permanent_session_lifetime = timedelta(minutes=5)

worksheet = Worksheet("The Hat")


@app.before_request
def before_request():
    session.permanent = True


@app.route("/")
def index():
    assigned = session["assignee"] if session.get("assignee") else None
    petitioner = session["petitioner"] if session.get("petitioner") else None

    if session.get("error"):
        error = True
        session.pop("error")
    else:
        error = False

    return render_template(
        "index.html", assigned=assigned, petitioner=petitioner, error=error
    )


@app.route("/", methods=["POST"])
def select():
    petitioner = request.form["petitioner"]

    if not petitioner or not petitioner in worksheet.names:
        session["error"] = True
    else:
        session["petitioner"] = petitioner
        session["assignee"] = get_or_assign_pick(worksheet, petitioner)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)