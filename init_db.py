#Bibliotecas
import contraviolencia as cv
import psycopg2


#Criando conexão no banco.

#Servidor Heroku.
eng = cv.create_engine("postgresql://gptmbrpnkclgjd:0dfbdfa12aa1d57939e7808873522f52184bb7d88142734618fa45b7bbbc187d@ec2-54-157-160-218.compute-1.amazonaws.com:5432/delep6os9o1a99")

#Servidor local.
#eng = create_engine("postgresql://root:postgres@localhost:5432/postgres")


#Ler cnfigurações de tabela padrão.
with open("tables.sql") as arquivo:
    eng.execute(arquivo.read())
print("Tabelas USERS e REGISTROS Criadas.")
    
    
#Criar tabela USERS
eng.execute ("insert into public.users (ref, usuario, senha) values ( now()::timestamp(0),'admin','admin')")
print("USER pdrão criado.")

#Criar tabela REGISTROS
eng.execute("insert into public.registros (ref, nome, dt_nasc, endereco, grupo_violacao, observacoes) values ( now()::timestamp(0),'individuo','11-11-1900','local','classificação','comentarios e impressões')")
print("REGISTRO padrão criado.")

#Fechar configurações de tabela.
arquivo.close()

#escrever no Bnaco de dados.
cv.db.commit()

#Fechar conexão.
cv.db.close()
        
    
