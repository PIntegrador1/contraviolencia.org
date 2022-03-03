#Bibliotecas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

#Gerando conexão e bamco de dados padrão
def get_db_conection():
    # Criando conexão no banco.
    global eng
    eng =create_engine("postgres://gptmbrpnkclgjd:0dfbdfa12aa1d57939e7808873522f52184bb7d88142734618fa45b7bbbc187d@ec2-54-157-160-218.compute-1.amazonaws.com:5432/delep6os9o1a99")
    
    #Criação de Sessão no banco.
    global db
    db = scoped_session(sessionmaker(bind=eng))
            
    #Espelhando.
    return  eng

#Ler cnfigurações de tabela padrão.
with open("tables.sql") as arquivo:
    eng.execute(arquivo.read())

#Criar tabela USERS
eng.execute ("insert into public.users (ref, usuario, senha) values ( now()::timestamp(0),'admin','admin')")

#Criar tabela REGISTROS
eng.execute("insert into public.registros (ref, nome, dt_nasc, endereco, grupo_violacao, observacoes) values ( now()::timestamp(0),'individuo','11-11-1900','local','classificação','comentarios e impressões')")

#Fechar configurações de tabela.
arquivo.close()

#escrever no Bnaco de dados.
db.commit()

#Fechar conexão.
db.close()
