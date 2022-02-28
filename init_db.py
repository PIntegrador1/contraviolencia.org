import psycopg2
#Gerando conexão e bamco de dados padrão

connection = psycopg2.connect(dbname='postgres', user='root', password='postgres')
                          

cur = connection.cursor()

with open("tables.sql") as arquivo:
    cur.execute(arquivo.read())

print('Neste ponto: As tabelas REGISTROS e USERS foram criadas com sucesso.')

cur.execute ("insert into public.users (ref, usuario, senha) values ( now()::timestamp(0),'admin','admin')")
print('Usuario padrão admin criado com sucesso')

cur.execute("insert into public.registros (ref, nome, dt_nasc, endereco, grupo_violacao, observacoes) values ( now()::timestamp(0),'individuo','11-11-1900','local','classificação','comentarios e impressões')")
print('Amostra de cadastro em registros gravado com sucesso')

arquivo.close()
connection.commit()
connection.close()
