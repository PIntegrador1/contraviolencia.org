import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO registros (nome, dt_nasc, endereco, grupo_violacao, observacoes) VALUES (?, ?, ?, ?, ?)",
            (' Novo Nome', 'Nova Data', 'Novo Endereço', 'Grupo de Violação', 'Observações')
            )

connection.commit()
connection.close()
