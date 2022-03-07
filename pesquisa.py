from flask import flash,request,render_template
import contraviolencia as cv
import psycopg2

def pesquisa():
    #Abrir conexão.
    eng = cv.get_db_conection()
    
    #busca no banco de dados. 
    u = eng.execute("select * from users;")
    buser = u.fetchall()
    print(buser)
    
                                
    #Quantidade de linhas.
    bn = (len(buser))
    print(bn)

    #Excessões.
    if bn < 1:
        flash(' Sua pesquisa não encontrou nenhum elemento.')
        
        
    #Saida.
    return render_template('admin.html',buser=buser,bn=bn) 
   
