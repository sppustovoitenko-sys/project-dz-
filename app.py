from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/author")
def author():
    return render_template("author.html")


@app.route("/planner")
def planner():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("planner.html", tasks=tasks)


@app.route("/add_task", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, description, created_at) VALUES (?, ?, ?)",
        (title, description, created_at)
    )
    conn.commit()
    conn.close()

    return redirect("/planner")


@app.route("/delete/<int:id>")
def delete_task(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/planner")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
