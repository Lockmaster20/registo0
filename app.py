from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


def herokudb():
    Host = 'ec2-18-203-62-227.eu-west-1.compute.amazonaws.com'
    Database = 'd493kefv8shc65'
    User = 'dyfepovpwicnty'
    Password = 'f7fa3c7a5ce9e03c2a7344173331c0db33d7370a90e4dc34cddb6c328aeeb178'
    return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')


def gravar(v1, v2, v3):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS instr (nome text, descri text, price text)")
    db.execute("INSERT INTO instr VALUES (%s, %s, %s)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()


def existe(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM instr WHERE nome = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor=None
    return valor


def log(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


def alterar(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("UPDATE instr SET price = %s WHERE nome = %s", (v2, v1))
    ficheiro.commit()
    ficheiro.close()


def apaga(v1):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("DELETE FROM instr WHERE nome = %s", (v1,))
    ficheiro.commit()
    ficheiro.close()


@app.route('/registo', methods=['GET', 'POST'])
def route():
    erro = None
    if request.method == 'POST':
        v1 = request.form['nome']
        v2 = request.form['desc']
        v3 = request.form['price']
        if existe(v1):
            erro = 'O Instrumento já existe.'
        else:
            gravar(v1, v2, v3)
            erro = 'Instrumento adicionado com sucesso.'
    return render_template('registo.html', erro=erro)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            erro = 'Bem-Vindo.'
    return render_template('login.html', erro=erro)


@app.route('/apagar', methods=['GET', 'POST'])
def apagar():
    erro = None
    if request.method == 'POST':
        v1 = request.form['nome']
        if not existe(v1):
            erro = 'O Instrumento não existe.'
        else:
            apaga(v1)
            erro = 'Instrumento Eliminado com Sucesso.'
    return render_template('apagar.html', erro=erro)


@app.route('/newpasse', methods=['GET', 'POST'])
def newpasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['nome']
        v2 = request.form['price']
        if not existe(v1):
            erro = 'O Instrumento não existe.'

        else:
            alterar(v1, v2)
            erro = 'Preço alterado com sucesso.'
    return render_template('newpasse.html', erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
