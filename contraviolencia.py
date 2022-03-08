from typing import final
import numpy as np
from  matplotlib import pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, render_template, request, url_for, flash, redirect
import psycopg2
import pesquisa as ps 
import delete as dl

def get_db_conection():
    # Criando conexão no banco.
    global eng
    
    #Servidor Heroku.
    eng = create_engine("postgresql://gptmbrpnkclgjd:0dfbdfa12aa1d57939e7808873522f52184bb7d88142734618fa45b7bbbc187d@ec2-54-157-160-218.compute-1.amazonaws.com:5432/delep6os9o1a99")
    
    #Servidor local.
    #eng = create_engine("postgresql://root:postgres@localhost:5432/postgres")
    
    #Criação de Sessão no banco.
    global db
    db = scoped_session(sessionmaker(bind=eng))
            
    #Espelhando.
    return  eng

def get_id(post_id):
    #Abrir conexão.
    eng = get_db_conection()
    
        
    #Pegar ids do banco
    p =  eng.execute(f"select * from registros where id = '{post_id}';")
    post_id = p.fetchone()
      
    
    return post_id


#Função init_py Flask.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'banco'

 
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        
        #Abrir conexão
        eng = get_db_conection()
        
      
        #Recebe dados
        usuario = request.form['user']
        senha = request.form['password']
        
             
        #Realizar consulta(query).
        i = eng.execute(f"select id from users where usuario ='{usuario}'and senha = '{senha}';")
        id = i.fetchone()
        
        if id is None:
            flash('usuario ou senha não conferem! Por favor, redigite ou cadastre-se.')
            return render_template('index.html')
            
                       
        #Saida.
        return redirect(url_for('logged',usuario=usuario))
    return render_template('index.html')
    
@app.route('/login', methods=['GET','POST'])
def login():
    #Abrir conexão.
    if request.method == 'POST':
        eng = get_db_conection()
       
        #Entrada dados do usuário HTML.
        usuario = request.form['user']
        senha = request.form['password']

        #Enviar queries(consultas).
        eng.execute(f"insert into public.users (usuario, senha) VALUES ('{usuario}','{senha}');")
        
        
        #Escrever queries.
        db.commit()
       
        #Fechar conexão; 
        db.close()
        
        
        #Saida
        flash(f" {usuario} cadastrado com SUCESSO!")
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/<usuario>/logged', methods=['GET','POST'])
def logged(usuario):
    app.root_path + '/' + 'templates/result.html'
    #Saida.   
    return render_template('logged.html',usuario=usuario)

@app.route('/result')
def result():
    #Abrir conexão
    db = get_db_conection()
    
    #Lendo query           
    query = 'select * from registros;'     
    post = pd.read_sql(query,db).set_index('id')
    
               
    #Contar linhas
    n_linha=(len(post))
             
       
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
    try:
        pesquisa = ps.pesquisa()
        
                
    except ValueError as e:
        return render_template('admin.html',e)
    
    finally:
        delete =   dl.delete()
    
    return render_template('admin.html')
       
       
       

@app.route('/<post_id>/posts', methods=['GET','POST'])
def posts(post_id):
    posts = get_id(post_id)
    return render_template('posts.html',posts=posts)
   
      
@app.route('/tabela')
def tabela():
    #Abrir Conexão.
    eng = get_db_conection()
        
    
    #Iterado na tabela
    r = eng.execute("select * from registros;")
    posts = r.fetchall()
       
               
    #Contar linhas
    n_linha= (len(posts))
               
    #Saida.
    return render_template('tabela.html',posts=posts,n_linha=n_linha)

  

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
        eng = get_db_conection()
        
            
        #Entrada usuário
        valor = request.form['busca']
        
               
        #busca no banco de dados. 
        o = eng.execute(f"select * from registros where nome like '{valor}%%' or  endereco like '{valor}%%' or grupo_violacao like '{valor}%%' or observacoes like '{valor}%%';")
        obj = o.fetchall()
        
                         
        #Quantidade de linhas.
        n = (len(obj))
        
        #Excessões.
        if n < 1:
            flash(' Sua pesquisa não encontrou nenhum elemento.')
              
                                    
                       
        #Saida
        return render_template('busca.html',obj=obj,n=n)
    return render_template('busca.html')
        
    
       
    
@app.route('/create',methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        #Abrir Conexão.
        eng = get_db_conection()
       
       

        #Entrada dados do usuario HTML.
        nome = request.form['nome']
        dt_nasc = request.form['dt_nasc']
        endereco = request.form['endereco']
        grupo_violacao = request.form['grupo_violacao']
        observacoes = request.form['observacoes']
        
        
                   
        #Registro no Banco.
        eng.execute(f"insert into public.registros (nome, dt_nasc, endereco, grupo_violacao, observacoes) VALUES ('{nome}','{dt_nasc}','{endereco}','{grupo_violacao}','{observacoes}');")
        
        #Fechamento de conexão.
        db.commit()
        
        #Fechar sessão.
        db.close()
       
        
        #Exceções:
        grupo = [nome,  dt_nasc,  endereco,  grupo_violacao,  observacoes]
        if grupo is None:
            flash(f"Erro: Campos '{grupo}'  requerido.")
            return redirect(url_for('index'))

        #Saida.
        return redirect(url_for('tabela'))
    return render_template('create.html')

@app.route('/<post_id>/edit',methods=('GET', 'POST'))
def edit(post_id):
    #Busca de Ids
    post_id = get_id(post_id)
    
    #Entrada de usuario.
    if request.method == 'POST':
        #Abrir conexão.
        eng = get_db_conection()
        
        
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
             eng.execute(f"update registros set nome ='{nome}', dt_nasc = '{dt_nasc}' ,  endereco = '{endereco}' , grupo_violacao ='{grupo_violacao}' , observacoes = '{observacoes}' where id = '{post_id[0]}';")
            
             #Escrever tabela.
             db.commit()
             
             #Fechar conexão.
             db.close()
       
                        
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
        eng = get_db_conection()
        
                   
        #Buscar linha para deletar.
        eng.execute(f"delete from registros where id = '{post_id[0]}';")
        
        #Escrever tabela.
        db.commit()
        
        #Fechar conexão.
        db.close()

       
        #Saida
        flash(f"Registro '{post_id[0]}' DELETADO!!!")
        return redirect(url_for('tabela'))
    return render_template('tabela.html')
    
