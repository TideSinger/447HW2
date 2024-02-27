from flask import (
    Blueprint, flash, g, redirect, render_template, url_for
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
        title = request.form['title']
        body = request.form['body']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO scores (id, plname, points)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('player.index'))

    return render_template('player/create.html')

def get_player(id):
    post = get_db().execute(
        'SELECT p.id, plname, points'
        ' FROM player p JOIN plname u ON p.id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if id is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    player = get_player(id)

    if request.method == 'POST':
        #title = request.form['title']
        #body = request.form['body']
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