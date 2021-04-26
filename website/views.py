from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from website import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')

@views.route('/todos', methods=['GET', 'POST'])
@login_required
def todos():
  if request.method == 'POST':
    note = request.form.get('note')
    print(note)
    new_todo = Note(data=note, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    flash('Todo added!', category='success-todo')
  return render_template('todos.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
  note = json.loads(request.data)
  noteId = note['noteId']
  note = Note.query.get(noteId)
  if note:
    if note.user_id == current_user.id:
      db.session.delete(note)
      db.session.commit()

  return jsonify({})