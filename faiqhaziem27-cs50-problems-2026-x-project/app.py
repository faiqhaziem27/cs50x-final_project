import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, session, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///study.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    categories = []

    category_rows = db.execute("SELECT DISTINCT category FROM entries WHERE user_id=?", user_id)
    for row in category_rows:
        categories.append(row["category"])

    selected_category = request.args.get("category")

    if selected_category and selected_category != "All":
        entries = db.execute("SELECT category, metric_value, date FROM entries WHERE user_id=? AND category=? ORDER BY date ASC", user_id, selected_category)
    else:
        entries = db.execute("SELECT category, metric_value, date FROM entries WHERE user_id =? ORDER BY date ASC", user_id)

    if not entries:
        return render_template("index.html",categories=categories, total_entries = 0, total_metric_value = 0, top_category = "None", dates = [], values = [], selected_category=selected_category)

    total_entries = len(entries)
    total_metric_value = 0
    values = []
    labels = []

    for row in entries:
        total_metric_value += row["metric_value"]
        values.append(row["metric_value"])

        labels.append(f"{row['category']} ({row['date']})")


    top_category_row = db.execute("SELECT category, SUM(metric_value) as total_value FROM entries WHERE user_id=? GROUP BY category ORDER BY total_value DESC LIMIT 1", user_id)

    if top_category_row:
        top_category = top_category_row[0]["category"]
    else:
        top_category = "None"

    return render_template("index.html", entries=entries, total_entries=total_entries, total_metric_value=total_metric_value, top_category=top_category, values=values, labels=labels, categories=categories, selected_category=selected_category)

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]

    entries = db.execute("SELECT id, category, metric_value, unit, date FROM entries WHERE user_id=?", user_id)
    return render_template("history.html", entries=entries)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Username is required", 403)

        elif not password:
            return apology("password is required", 403)

        rows = db.execute("SELECT * FROM users WHERE username=?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Password does not match", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("All fields are required", 403)

        if password != confirmation:
            return apology("password does not match", 403)

        existing_user = db.execute("SELECT * FROM users WHERE username=?", username)

        if len(existing_user) > 0:
            return apology("Username is already taken", 403)

        password_hash = generate_password_hash(password)

        try:
            user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
            session["user_id"] = user_id

        except Exception:
            return apology("Username already taken", 403)

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user_id = session["user_id"]
    if request.method == "POST":

        category = request.form.get("category")
        metric_value = request.form.get("metric_value")
        unit = request.form.get("unit")
        date = request.form.get("date")

        if not category or not metric_value or not date:
            return apology("All fields are required", 403)

        try:
            metric_value_int = int(metric_value)
            if metric_value_int < 0:
                return apology("Invalid number! Please provide a positive integer", 403)
        except ValueError:
            return apology("Metric value must be a valid number", 403)

        db.execute("INSERT INTO entries (user_id, category, metric_value, unit, date) VALUES (?, ?, ?, ?, ?)", user_id, category, metric_value, unit, date)

        return redirect("/")

    else:
        rows = db.execute("SELECT DISTINCT category FROM entries WHERE user_id=?", user_id)
        categories = []

        for row in rows:
            categories.append(row["category"])

        return render_template("add.html", categories=categories)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    user_id = session["user_id"]
    entry_id = request.form.get("id")

    if entry_id:
        db.execute("DELETE FROM entries WHERE id=? AND user_id=?", entry_id, user_id)

    return redirect("/history")

@app.route("/edit/<int:id>", methods=["POST", "GET"])
@login_required
def edit(id):
    user_id = session["user_id"]
    if request.method == "POST":
        category = request.form.get("category")
        date = request.form.get("date")
        metric_value = request.form.get("metric_value")
        unit = request.form.get("unit")

        db.execute("UPDATE entries SET category=?, date=?, metric_value=?, unit=? WHERE id=? AND user_id=?", category, date, metric_value, unit, id, user_id)

        return redirect("/")

    else:
        entries = db.execute("SELECT * FROM entries WHERE id=? AND user_id=?", id, user_id)

        if not entries:
            return apology("Entry not found", 403)

        entry = entries[0]

        return render_template("edit.html", entry=entry)

@app.route("/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    user_id = session["user_id"]

    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not current_password or not new_password or not confirmation:
            return apology("All fields are required", 403)

        if new_password != confirmation:
            return apology("Password does not match", 403)

        rows = db.execute("SELECT hash FROM users WHERE id=?", user_id)

        if not check_password_hash(rows[0]["hash"], current_password):
            return apology("Invalid current password", 403)

        new_hash = generate_password_hash(new_password)

        db.execute("UPDATE users SET hash=? WHERE id=?", new_hash, user_id)

        flash("Password updated successfully")

        return redirect("/")

    else:
        return render_template("change_password.html")
