from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import login_required, login_manager, login_user, UserMixin, logout_user, LoginManager, current_user

import sqlite3


login_manager = LoginManager()
app = Flask(__name__)
login_manager.__init__(app)

app.secret_key = "segredo secreto muito secreto Lucas, Pedro Lucas"

def obter_conexao():
    conexao = sqlite3.connect('banco.db')
    conexao.row_factory = sqlite3.Row
    return conexao

class User(UserMixin):
    def __init__(self, id, nome, senha, email):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.email = email

    @classmethod
    def get(cls, id):
        conn = obter_conexao()
        sql = "select * from users where id = ?"
        resultado = conn.execute(sql, (id,)).fetchone()
        conn.close()
        if resultado:
            return cls(
                id=resultado['id'],
                nome=resultado['nome'],
                senha=resultado['senha'],
                email=resultado['email']
            )
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']


        conn = obter_conexao()
        cursor = conn.cursor()

        sql = "select * from users where nome = ? or email =?"
        cursor.execute(sql, (nome, email))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            flash('usuario cadastrado')
            return redirect(url_for('index'))

        sql = 'insert into users(nome, senha, email) values(?, ?, ?)'
        conn.execute(sql, (nome, senha, email,))
        conn.commit()
        conn.close() 
        
        # flash
        return redirect(url_for('index'))
    
    conn = obter_conexao()
    sql = 'select nome, email from users'
    lista = conn.execute(sql).fetchall()
    conn.close()

    return render_template('register.html', lista = lista)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']

        conn = obter_conexao()
        cursor = conn.cursor()

        sql = "select * from users where nome = ? and senha = ? and email = ?"
        cursor.execute(sql, (nome, senha, email))
        usuario_existente = cursor.fetchone()
        conn.close()

        if usuario_existente:
            user = User(
                id = usuario_existente['id'],
                nome = usuario_existente['nome'],
                senha = usuario_existente['senha'],
                email = usuario_existente['email']
            )
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('nao tem, faça o cadastro primeiro')
            return redirect(url_for('register'))                                                                                                           

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome = current_user.nome)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/page_del')
def page_del():
    return render_template('page_del.html')


@app.route('/delete_user', methods = ['POST'])
@login_required
def delete_user():
    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute("delete from users where id = ?", (current_user.id,))
    conn.commit()
    conn.close()

    logout_user()
    flash("Usuário deletado com sucesso.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)