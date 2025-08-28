import sqlite3
from time import sleep
from modules.log import log
from datetime import datetime

DB_URL = "database.db"

def load():
    secure_execute("CREATE TABLE IF NOT EXISTS temp (id INTEGER PRIMARY KEY AUTOINCREMENT,id_usuario INTEGER, entrada TEXT, id_message INTEGER)")
    secure_execute("CREATE TABLE IF NOT EXISTS calls (id INTEGER PRIMARY KEY AUTOINCREMENT,id_usuario INTEGER, data_entrada TEXT, hora_entrada TEXT, data_saida TEXT, hora_saida TEXT, permanencia REAL)")

def secure_execute(query:str, values:list=None, timeout:float=5, tentativas:int=3, return_value:bool=False):
    
    for tentativa in range(tentativas):
        try:
            with sqlite3.connect(DB_URL) as con:
                
                cur = con.cursor()
                if values:
                    cur.execute(query, values)
                else:
                    cur.execute(query)
                con.commit()

                if return_value:
                    return cur.fetchall()
                
                return True
        except sqlite3.Error as er:

            if str(er) == "database is locked":
                print("Database locked, aguardando . .")
            else:
                print(f"Erro inesperado com o sqlite [{er}], aguardando. .")
                log(er)

            sleep(timeout)

        except Exception as er:
            print(f"Erro inesperado {er}")
            return False
    return False

def user_connected(id_user, id_message):
    entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    QUERY_VALID = "SELECT id FROM temp WHERE id=?"
    QUERY_DELETE = "DELETE FROM temp WHERE id_usuario=?"
    QUERY_INSERT = "INSERT INTO temp (id_usuario, entrada, id_message) VALUES (?, ?, ?)"

    existe = secure_execute(query=QUERY_VALID, values=[id_user], return_value=True)
    if existe:
        secure_execute(query=QUERY_DELETE, values=[id_user])
        log(f"[{id_user}] conectou-se já com registro")

    secure_execute(query=QUERY_INSERT, values=[id_user, entrada, id_message])
    
def user_desconected(id_user):
    send_message:int = None
    QUERY_SELECT = "SELECT entrada, id_message FROM temp WHERE id_usuario=?"
    QUERY_DELETE = "DELETE FROM temp WHERE id_usuario=?"
    QUERY_INSERT = "INSERT INTO calls (id_usuario, data_entrada, hora_entrada, data_saida, hora_saida, permanencia) VALUES (?,?,?,?,?,?)"
    req = secure_execute(query=QUERY_SELECT, values=[id_user], return_value=True)
    if req:
        time_in_str = req[0][0]
        
        saida = datetime.now()    
        entrada = datetime.strptime(time_in_str, '%Y-%m-%d %H:%M:%S')
        permanencia = (saida - entrada).total_seconds()
        
        if permanencia>=60:
            values = [
                id_user,
                entrada.date().strftime('%Y-%m-%d'),
                entrada.time().strftime('%H:%M:%S'),
                saida.date().strftime('%Y-%m-%d'),
                saida.time().strftime('%H:%M:%S'),
                permanencia
            ]
            secure_execute(QUERY_INSERT, values=values)
        else:
            send_message = req[0][1]

        secure_execute(QUERY_DELETE, values=[id_user])
    else:
        log(f"[{id_user}] desconectou-se sem registro")
    return send_message
