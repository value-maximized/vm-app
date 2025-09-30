import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"  # for flash messages

# Store DB inside the Flask instance folder: ./instance/plans.sqlite3
DB_PATH = os.path.join(app.instance_path, "plans.sqlite3")
os.makedirs(app.instance_path, exist_ok=True)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()

# Initialize DB at startup
with app.app_context():
    init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        owner = request.form.get("owner", "").strip()
        start_date = request.form.get("start_date", "")
        end_date = request.form.get("end_date", "")

        # Simple validation
        if not all([name, owner, start_date, end_date]):
            flash("Please fill out all fields.", "error")
        else:
            db.execute(
                "INSERT INTO plans (name, owner, start_date, end_date) VALUES (?, ?, ?, ?)",
                (name, owner, start_date, end_date),
            )
            db.commit()
            flash("Plan created successfully!", "success")
        return redirect(url_for("index"))

    # GET: fetch all plans to display
    plans = db.execute("SELECT id, name, owner, start_date, end_date FROM plans ORDER BY id ASC").fetchall()
    return render_template("index.html", plans=plans)

if __name__ == "__main__":
    app.run(debug=True)
