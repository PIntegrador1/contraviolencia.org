from flask import flash,request,render_template,redirect,url_for
import contraviolencia as cv
import psycopg2



def delete():
    if request.method == 'POST':
        #Abrir Conexão
        eng = cv.get_db_conection()
        
        #Entrada usuario.
        tabela = request.form['table']
        
        #Resetar dados da tabela requerida.
        eng.execute(f"delete from {tabela};")
        
        #Escrever mudanças.
        cv.db.commit()
        
        #Fechar conexão.
        cv.db.close()
        
            
        #Saida
        flash(f"Os registros foram TOTALMENTE apagados na tabela {tabela}.")
        return redirect(url_for('tabela'))
    return render_template('admin.html')