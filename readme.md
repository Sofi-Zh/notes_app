# This is a study project of a simple CRUD notebook built with Flask.

## Features:
-Add, edit and delete notes in a notebook.
-Store notes in SQLite3 database.
-Reuse one HTML template for  creating and editing notes.

## Technologies used:
-Python 3.11
-Flask 3.0
-SQLite

## Functions:
-`get_db()` – creates a connection to the SQLite database
-`init_db()` – creates the database table
-`index()` – displays the home page
-`all_notes()` – displays all notes
-`new_note()` – creates a new note
-`note_details(id)` – displays the details of a note
-`edit_note(id)` – edits an existing note
-`delete_note(id)` – deletes a note

## Link to open:
http://127.0.0.1:5000

## To run an application:
```bash
git clone https://github.com/USERNAME/notes_app.git
cd notes_app
pip install -r requirements.txt
python app.py
```
## Author
Sofiya Zhyvalkouskaya, IT Step, 2026
