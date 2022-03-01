import psycopg
#Gerando conexão e bamco de dados padrão

connection = psycopg.connect(host='ec2-54-160-103-135.compute-1.amazonaws.com',
                            database='d1na4mcaapv3a9',
                            user='evtiqnayntanna',
                            password='8a0b54b5c8fc50e5d49d3cebfe198db1fac07a335b587db8b7f8c41b2e857b93',
                            port='5432' )
                          

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
