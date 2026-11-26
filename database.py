import sqlite3

conn = sqlite3.connect('musicas.db')
conn.execute("PRAGMA foreign_keys = ON")

def criar_tabelas():
    conn.executescript(
    """CREATE TABLE IF NOT EXISTS artista(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    genero TEXT, 
    historia TEXT);
    CREATE TABLE IF NOT EXISTS albuns(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    datalancamento DATE,
    contexto TEXT,
    artista_id INTEGER NOT NULL REFERENCES artista(id));
    CREATE TABLE IF NOT EXISTS musicas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    letra TEXT,
    significado TEXT,
    historia TEXT,
    visualizacoes INTEGER,
    albuns_id INTEGER NOT NULL REFERENCES albuns(id),
    visualizacoes INTEGER);
    
    """
    )
criar_tabelas()
