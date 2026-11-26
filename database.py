import sqlite3

conn = sqlite3.connect('musicas.db')
conn.execute("PRAGMA foreign_keys = ON")


def criar_tabelas():
    conn.executescript(
        """
        DROP TABLE IF EXISTS musicas;
        DROP TABLE IF EXISTS albuns;
        DROP TABLE IF EXISTS artista;

        CREATE TABLE artista(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            genero TEXT,
            historia TEXT
        );

        CREATE TABLE albuns(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            ano INTEGER,
            contexto TEXT,
            artista_id INTEGER NOT NULL REFERENCES artista(id)
        );

        CREATE TABLE musicas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            letra TEXT,
            significado TEXT,
            historia TEXT,
            visualizacoes INTEGER DEFAULT 0,
            link TEXT UNIQUE,
            albuns_id INTEGER NOT NULL REFERENCES albuns(id)
        );
        """
    )
    conn.commit()


criar_tabelas()
conn.close()