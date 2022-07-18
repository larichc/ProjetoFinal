import mysql.connector

def conectar(usuario: str = 'root', senha: str = 'throwaway11', host: str = '127.0.0.1', banco: str = 'xpto_alimentos'):
    cnx = mysql.connector.connect(user = usuario, password = senha,
                                    host = host,
                                    database = banco)

    return cnx

def fecha_conexao(cnx,cursor):
    cnx.commit()
    cursor.close()
    cnx.close()