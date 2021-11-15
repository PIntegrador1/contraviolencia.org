import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM registros WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'banco'


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM registros').fetchall()
    if posts is None:
        flash('Nenhum registro encontrado!')
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        dt_nasc = request.form['dt_nasc']
        endereco = request.form['endereco']
        grupo_violacao = request.form['grupo_violacao']
        observacoes = request.form['observacoes']

        if not nome:
            flash(' Nome da pessoa requerido!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO registros (nome, dt_nasc, endereco, grupo_violacao, observacoes) VALUES (?, ?, ?, ?, ?)',
                         (nome, dt_nasc, endereco, grupo_violacao, observacoes))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        nome = request.form['nome']
        dt_nasc = request.form['dt_nasc']
        endereco = request.form['endereco']
        grupo_violacao = request.form['grupo_violacao']
        observacoes = request.form['observacoes']

        if not nome:
            flash('Nome é requerido!')
             
        else:
            conn = get_db_connection()
            conn.execute('UPDATE registros SET nome = ?, dt_nasc = ?, endereco = ?, grupo_violacao =?, observacoes = ?'
                         ' WHERE id = ?',
                         (nome, dt_nasc, endereco, grupo_violacao, observaoes, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('GET','POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM registros WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" Foi deletado com sucesso!'.format(post['nome']))
    return redirect(url_for('index'))
