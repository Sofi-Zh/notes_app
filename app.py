import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super secret key"
DB = "notes.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            time TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/notes')
def all_notes():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY time DESC  ").fetchall()
    conn.close()
    return render_template("notes_list.html", notes=notes)


@app.route('/notes/<int:id>')
def note_details(id):
    conn = get_db()
    note_details = conn.execute("SELECT * FROM notes WHERE id = ?", (id,)).fetchone()
    conn.close()
    if note_details is None:
        return "Note not found", 404
    return render_template("note_details.html", note_details=note_details)

@app.route('/notes/add', methods=['GET', 'POST'])
def new_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not title or not content:
            flash ("Please fill all fields")
            return redirect(url_for("new_note"))
        conn = get_db()
        conn.execute('''
            INSERT INTO notes (title, content, time) VALUES (?, ?, ?) ''', (title, content, time))
        conn.commit()
        conn.close()
        flash ("Note added successfully")
        return redirect(url_for("all_notes"))

    return render_template("notes_add.html", note = None)

@app.route('/notes/edit/<int:id>', methods=["GET", "POST"])
def edit_note(id):
    conn = get_db()
    note = conn.execute("SELECT * FROM notes WHERE id =?", (id,)).fetchone()

    if note is None:
        conn.close()
        return "Note not found", 404

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not title or not content:
            conn.close()
            flash ("Please fill all fields")
            return redirect(url_for("edit_note", id=id))
        conn.execute('''
            UPDATE notes SET title = ?, content = ?, time = ? WHERE id = ?
            ''', (title, content, time, id))
        conn.commit()
        conn.close()
        flash ("Note updated successfully")
        return redirect(url_for("note_details", id=id))

    conn.close()
    return render_template("notes_add.html", note = note)

@app.route('/notes/delete/<int:id>', methods=["POST"])
def delete_note(id):
    conn = get_db()
    conn.execute('''
        DELETE FROM notes WHERE id = ?
    ''', (id,))
    conn.commit()
    conn.close()
    flash (f"Note deleted successfully")
    return redirect(url_for("all_notes"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)