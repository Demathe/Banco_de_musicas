# colocar as funções do código aqui
import sqlite3

conn = sqlite3.connect('musicas.db')

def adicionar_artista(nome, genero, historia):
    conn.execute(
        """INSERT INTO artista (nome, genero, historia)
           VALUES (?, ?, ?)""",
        (nome, genero, historia)
    )
    conn.commit()
