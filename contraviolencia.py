import numpy as np
from  matplotlib import pyplot as plt
import pandas as pd
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response
from datetime import timedelta
from werkzeug.exceptions import abort

def get_db_connection():
    # Criando conexão no banco.
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='root',
                            password='postgres')
    #Espelhando.
    return conn

def get_id(post_id):
    #Abrir conexão.
    conn = get_db_connection()
    cur = conn.cursor()
        
    
    #Pegar ids do banco
    cur.execute(f"select * from registros where id = '{post_id}';")
    post_id = cur.fetchone()
    
            
    #Fechar conexão.
    conn.close()
    
    return post_id


#Função init_py Flask.
app = Flask(__name__)
app.run(debug=True)
app.config['SECRET_KEY'] = 'banco'
app.permanent_session_lifetime = timedelta(seconds=10)

@app.route('/', methods=['GET','POST'])
def validar():
    if request.method == 'POST':
        
        #Abrir conexão
        conn = get_db_connection()
        cur = conn.cursor()
      
        #Recebe dados
        usuario = request.form['user']
        senha = request.form['password']
        
             
        #Realizar consulta(query).
        cur.execute(f"select id from users where usuario ='{usuario}'and senha = '{senha}';")
        id = cur.fetchone()
        
        if id is None:
            flash('usuario ou senha não conferem! Por favor, redigite ou cadastre-se.')
            return render_template('validar.html')
            
        #Fechar Conexão
        conn.close()
        
                  
        #identificar usuario e temporizar.
        user_id = []
        session[usuario] = user_id
        session.permanent = True
        
        #Saida.
        return redirect(url_for('logged',usuario=usuario))
    return render_template('validar.html')
    
@app.route('/login', methods=['GET','POST'])
def login():
    #Abrir conexão.
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
            
        #Entrada dados do usuário HTML.
        usuario = request.form['user']
        senha = request.form['password']

        #Enviar queries(consultas).
        cur.execute(f"insert into public.users (usuario, senha) VALUES ('{usuario}','{senha}');")

        #Escrever queries.
        conn.commit()
        conn.close()
        
        #Saida
        flash(f" {usuario} cadastrado com SUCESSO!")
        return redirect(url_for('validar'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()      
    return render_template('logout.html')

@app.route('/<usuario>/logged', methods=['GET','POST'])
def logged(usuario):
    app.root_path + '/' + 'templates/result.html'
    
    #Saida.   
    return render_template('logged.html',usuario=usuario)

@app.route('/result')
def result():
    #Abrir conexão
    conn = get_db_connection()
    
    #Lendo query           
    query = 'select * from registros;'     
    post = pd.read_sql(query,conn).set_index('id')
    
               
    #Contar linhas
    n_linha=(len(post))
             
    #Fechar conexão.
    conn.close()
    
    # Gerar Grafico
    global filter
    filter =  post.groupby(['grupo_violacao']).grupo_violacao.count()
    filter.plot(kind='line')
    plt.savefig("static/css/image/graf.png")
    plt.close()

        
    #Gerar Frequencia do gráfico.
    global legenda
    conj = pd.Series(post['grupo_violacao'])
    legenda = np.unique(conj,return_counts=True)
    print(legenda)
    
    
    #Mostrar página
    return render_template('result.html',n_linha=n_linha,legenda=legenda)

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        #Abrir Conexão
        conn = get_db_connection()
        cur = conn.cursor()
        

        tabela = request.form['table']
        

        #Resetar dados da tabela requerida.
        cur.execute(f"delete from {tabela};")
        
        #Escrever mudanças.
        conn.commit()       
        
        #Fechar conexão
        conn.close()
        
        #Saida
        flash(f"Os registros foram TOTALMENTE apagados na tabela {tabela}.")
        return redirect(url_for('validar'))
    return render_template('admin.html')

@app.route('/<post_id>/posts', methods=['GET','POST'])
def posts(post_id):
    posts = get_id(post_id)
    return render_template('posts.html',posts=posts)
   
      
@app.route('/index')
def index():
    #Abrir Conexão.
    conn = get_db_connection()
    cur = conn.cursor()
    
    #Iterado na tabela
    cur.execute("select * from registros;")
    posts = cur.fetchall()
    
               
    #Contar linhas
    n_linha=(len(posts))
        
     
    #Fechar Conexão.
    conn.close()       

           
    #Saida.
    return render_template('index.html',posts=posts,n_linha=n_linha)

  

@app.route('/sobre')
def sobre():
    #Mostrar página
    return render_template('sobre.html')



@app.route('/busca' ,methods=['GET','POST'])
def busca():
    global obj
    global n
    if request.method == 'POST':
        #Abrir Conexão.
        conn = get_db_connection()
        cur = conn.cursor()
            
        #Entrada usuário
        valor = request.form['busca']
        
               
        #busca no banco de dados. 
        cur.execute(f"select * from registros where nome like '{valor}%' or  endereco like '{valor}%' or grupo_violacao like '{valor}%' or observacoes like '{valor}%' ;")
        obj = cur.fetchall()
        
                         
        #Quantidade de linhas.
        n = (len(obj))
        
        #Excessões.
        if n < 1:
            flash(' Sua pesquisa não encontrou nenhum elemento.')
              
                                        
        #Fechar conexão.
        conn.close()
                
        #Saida
        return render_template('busca.html',obj=obj,n=n)
    return render_template('busca.html')
        
    
       
    
@app.route('/create',methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        #Abrir Conexão.
        conn = get_db_connection()
        cur = conn.cursor()
       

        #Entrada dados do usuario HTML.
        nome = request.form['nome']
        dt_nasc = request.form['dt_nasc']
        endereco = request.form['endereco']
        grupo_violacao = request.form['grupo_violacao']
        observacoes = request.form['observacoes']
        
        
                   
        #Registro no Banco.
        cur.execute(f"insert into public.registros (nome, dt_nasc, endereco, grupo_violacao, observacoes) VALUES ('{nome}','{dt_nasc}','{endereco}','{grupo_violacao}','{observacoes}');")
        
        #Fechamento de conexão.
        conn.commit()
        conn.close()
        
        #Exceções:
        grupo = [nome,  dt_nasc,  endereco,  grupo_violacao,  observacoes]
        if grupo is None:
            flash(f"Erro: Campos '{grupo}'  requerido.")
            return redirect(url_for('index'))

        #Saida.
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<post_id>/edit',methods=('GET', 'POST'))
def edit(post_id):
    #Busca de Ids
    post_id = get_id(post_id)
    
    #Entrada de usuario.
    if request.method == 'POST':
        #Abrir conexão.
        conn = get_db_connection()
        cur = conn.cursor()
        
        #Entrada de usuario.
        nome = request.form['nome'] or post_id[2]
        dt_nasc = request.form['dt_nasc'] or post_id[3]
        endereco = request.form['endereco'] or post_id[4]
        grupo_violacao = request.form['grupo_violacao'] or post_id[5]
        observacoes = request.form['observacoes'] or post_id[6]
        
        #Condições.
        lista = [nome,dt_nasc ,endereco,grupo_violacao ,observacoes]
        if lista == lista:
             #Executar mudanças.
             cur.execute(f"update registros set nome ='{nome}', dt_nasc = '{dt_nasc}' ,  endereco = '{endereco}' , grupo_violacao ='{grupo_violacao}' , observacoes = '{observacoes}' where id = '{post_id[0]}';")
            
             #escrever tabela.
             conn.commit()
       
             #Fechar conexão. 
             conn.close()
            
             #Saida.
             flash(f"Alterações ATUALIZADAS em '{post_id[2]}' com sucesso!")
             return redirect(url_for('index'))
        else:
            flash(f"Em '{post_id[2]}' NADA alterado!!!")
            return redirect(url_for('index'))
           
    return render_template('edit.html',post_id=post_id)
    

@app.route('/<post_id>/delete', methods=['GET','POST'])
def delete(post_id):
    #Buscar IDs.
    post_id = get_id(post_id)
    if request.method == 'POST':
        #Abrir conexão.
        conn = get_db_connection()
        cur = conn.cursor()
                   
        #Buscar linha para deletar.
        cur.execute(f"delete from registros where id = '{post_id[0]}';")
        
        #Escrever tabela.
        conn.commit()

        #Fechar conexão.
        conn.close()

        #Saida
        flash(f"Registro '{post_id[0]}' DELETADO!!!")
        return redirect(url_for('index'))
    return render_template('index.html')
    