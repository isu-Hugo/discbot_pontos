import sqlite3
from time import sleep
from modules.log import log
from datetime import datetime
DB_URL = "database.db"

def load():
    secure_execute("CREATE TABLE IF NOT EXISTS temp (id_usuario INTEGER, entrada TEXT)")
    secure_execute("CREATE TABLE IF NOT EXISTS calls (id_usuario INTEGER, data_entrada TEXT, hora_entrada TEXT, data_saida TEXT, hora_saida TEXT, permanencia REAL)")

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

def user_connected(id_user):
    entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    QUERY = "INSERT INTO temp (id_usuario, entrada) VALUES (?, ?)"
    secure_execute(query=QUERY, values=[id_user, entrada])
    
def user_desconected(id_user):
    
    QUERY_SELECT = "SELECT entrada FROM temp WHERE id_usuario=?"
    QUERY_DELETE = "DELETE FROM temp WHERE id_usuario=?"
    QUERY_INSERT = "INSERT INTO calls (id_usuario, data_entrada, hora_entrada, data_saida, hora_saida, permanencia) VALUES (?,?,?,?,?,?)"
    req = secure_execute(query=QUERY_SELECT, values=[id_user], return_value=True)
    if req:
        time_in_str = req[0][0]
        
        saida = datetime.now()    
        entrada = datetime.strptime(time_in_str, '%Y-%m-%d %H:%M:%S')
        permanencia = (saida - entrada).total_seconds()

        values = [
            id_user,
            entrada.date().strftime('%Y-%m-%d'),
            entrada.time().strftime('%H:%M:%S'),
            saida.date().strftime('%Y-%m-%d'),
            saida.time().strftime('%H:%M:%S'),
            permanencia
        ]

        secure_execute(QUERY_INSERT, values=values)

        secure_execute(QUERY_DELETE, values=[id_user])
    else:
        log(f"Usuario desconectado sem registro de entrada [{id_user}]")

