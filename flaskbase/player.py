from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, request
)

from flaskbase.db import get_db

bp = Blueprint('scores', __name__)

@bp.route('/')
def index():
    db = get_db()
    scores = db.execute(
        'SELECT p.id, p.plname, p.points'
        ' FROM scores p JOIN scores u ON p.id = u.id'
        ' ORDER BY p.id DESC'
    ).fetchall()
    return render_template('player/index.html', scores=scores)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        pid = request.form['id']
        plname = request.form['plname']
        points = request.form['points']
        error = None
        if get_player(pid) is not None:
            abort(400,f"Player id {id} already exists.")

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO scores (id, plname, points)'
                ' VALUES (?, ?, ?)',
                (pid, plname, points)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('player/create.html')

@bp.route('/<int:id>/read', methods=('GET', 'POST'))
def read(id):
    player = get_player(id)
    if request.method == 'POST':
        error = None

    if error is not None:
            flash(error)

    return render_template('player/read.html', scores=player)

def get_player(id):
    player = get_db().execute(
        'SELECT p.id, p.plname, p.points'
        ' FROM scores p JOIN scores u ON p.id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if id is None:
        abort(404, f"Player id {id} doesn't exist.")

    return player

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    player = get_player(id)

    if request.method == 'POST':
        error = None
        plname = request.form['plname']
        points = request.form['points']


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE player SET plname = ?, points = ?'
                ' WHERE id = ?',
                (id, plname, points)
            )
            db.commit()
            return redirect(url_for('player.index'))

    return render_template('player/update.html', scores=player)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_player(id)
    db = get_db()
    db.execute('DELETE FROM scores WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('player.index'))