import sqlite3
conn = (sqlite3.connect('musicas.db'))

for linha in conn.execute("SELECT * FROM artista"):
    print(linha)