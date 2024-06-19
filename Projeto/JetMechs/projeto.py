from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'jet'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
       SGBD = 'mysql+mysqlconnector',
       usuario = 'root',
       senha = 'teste1234',
       servidor = 'localhost',
       database = 'jet'
)


db = SQLAlchemy(app)

class clientes(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(100), nullable=True)
    cpf_cliente = db.Column(db.String(11), nullable=True)
    telefone_cliente = db.Column(db.String(15), nullable=True)
    email_cliente = db.Column(db.String(100), nullable=True)
    veiculo_cliente = db.Column(db.String(50), nullable=True)
    placa_veiculo = db.Column(db.String(50), nullable=True)
    tipo_servico = db.Column(db.String(50), nullable=True)
    data_agendamento = db.Column(db.String(50), nullable=True)
    hora_agendamento = db.Column(db.String(50), nullable=True)

    def __repr__(self) -> str:
        return '<Name %r' % self.name

#criando uma rota
@app.route("/index")
def tela_principal():
    return render_template("index.html")

#rota cliente
@app.route("/clientes")
def cad_cliente():
    return render_template("clientes.html")

#rota empresa
@app.route("/empresa")
def cad_empresa():
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect('/login')
    return render_template("empresa.html")

#rota historico
@app.route("/historico")
def ver_historico():
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect('/login')
    return render_template("historico.html")

# rota voltada para adicionar clientes no \clientes
@app.route("/adicionar", methods=["POST",])
def cadastrar_cliente():

    nome_recebido = request.form["txtNome"]
    cpf_recebido = request.form["txtCPF"]
    telefone_recebido = request.form["txtTel"]
    email_recebido = request.form["txtEmail"]
    veiculo_recebido = request.form["txtVel"]
    placa_recebido = request.form['txtPlaca']
    servico_recebido = request.form['txtServ']
    data_recebido = request.form['txtData']
    hora_recebido = request.form['txtHora']


    add_clientes = clientes(nome_cliente=nome_recebido, cpf_cliente=cpf_recebido, telefone_cliente=telefone_recebido, email_cliente=email_recebido, veiculo_cliente=veiculo_recebido, 
                             placa_veiculo=placa_recebido, tipo_servico=servico_recebido, data_agendamento=data_recebido, hora_agendamento=hora_recebido)

    db.session.add(add_clientes)
    db.session.commit()
    # Adiciona mensagem flash de sucesso
    flash("Agendamento adicionado com sucesso!", "success")

    # Redireciona para a página inicial
    return redirect("/index")

# rota para mostrar a lista de clientes ja cadastrados, a parta agendamentos.html em conjunto com a estrutura.html 
@app.route("/agendamentos")
def agendamentos_servicos():
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        falha_autenticacao = True
        return render_template("agendamentos.html", descricao_agendamento='Aqui estão todos os agendamentos',todos_agendamentos = agend_servicos, falha_autenticacao=falha_autenticacao)
    falha_autenticacao = False
    agend_servicos = clientes.query.order_by(clientes.id_cliente)
    return render_template("agendamentos.html", descricao_agendamento='Aqui estão todos os agendamentos',todos_agendamentos = agend_servicos, falha_autenticacao=falha_autenticacao)

#rota para editar
@app.route("/editar/<int:id>")
def editar_agendamento(id):
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect('/login')
    cliente_selecionado = clientes.query.filter_by(id_cliente=id).first()
    return render_template("editar.html", clientes=cliente_selecionado)

#rota para atualizar
@app.route("/atualizar", methods=['POST', ])
def atualizar():

    cliente_selecionado = clientes.query.filter_by(id_cliente=request.form['txtId']).first()

    cliente_selecionado.nome_cliente = request.form['txtNome']
    cliente_selecionado.cpf_cliente = request.form['txtCPF']
    cliente_selecionado.telefone_cliente = request.form['txtTel']
    cliente_selecionado.email_cliente = request.form['txtEmail']
    cliente_selecionado.veiculo_cliente = request.form['txtVel']
    cliente_selecionado.placa_veiculo = request.form['txtPlaca']
    cliente_selecionado.tipo_servico = request.form['txtServ']
    cliente_selecionado.data_agendamento = request.form['txtData']
    cliente_selecionado.hora_agendamento = request.form['txtHora']

    db.session.add(cliente_selecionado)
    db.session.commit()

    return redirect("/agendamentos")

#rota para exluir 
@app.route('/excluir/<int:id>')
def excluir_agendamento(id):
    cliente_selecionado = clientes.query.filter_by(id_cliente=id).first()
    if cliente_selecionado:
        db.session.delete(cliente_selecionado)
        db.session.commit()
        flash('Agendamento excluído com sucesso!', 'success')
    else:
        flash('Agendamento não encontrado.', 'danger')

    return redirect('/agendamentos')

#rota para login
@app.route("/login")
def login():
    return render_template("login.html")

#rota para autenticar usuario
@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    email = request.form['txtEmail']
    senha = request.form['txtSenha']
    if email == 'jetmechs@admin' and senha == 'admin':
        session['usuario_logado'] = email
        return redirect('/empresa')
    else:
        flash('Falha na autenticação. Verifique suas credenciais e tente novamente.', 'danger')
        return redirect('/login')

@app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect('/index')

app.run(port=5050)