import psycopg2
#Gerando conexão e bamco de dados padrão

connection =  psycopg2.connect(host='ec2-3-218-71-191.compute-1.amazonaws.com',
                            database='da6f4afhp535hl',
                            user='bwpvtmbqsdcvgi',
                            password='a61a16e4f46cb9cff6e672d0e23afeb53f4ae3a14af7198893b4efd4124708e8',
                            port='5432')
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
