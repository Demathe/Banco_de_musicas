# colocar as funções do código aqui
import sqlite3

conn = sqlite3.connect('musicas.db')

def adicionar_musica():
    conn.execute("""INSERT INTO """)