# colocar as funções do código aqui
import sqlite3

conn = sqlite3.connect('musicas.db')
conn.execute("PRAGMA foreign_keys = ON")


def adicionar_artista(nome, genero=None, historia=None):
    try:
        cursor = conn.execute(
            """INSERT INTO artista (nome, genero, historia)
               VALUES (?, ?, ?)""",
            (nome, genero, historia)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Artista '{nome}' já está cadastrado.")
        return None


def adicionar_album(titulo, nome_artista, ano=None, contexto=None):
    artista = conn.execute(
        "SELECT id FROM artista WHERE nome = ?", (nome_artista,)
    ).fetchone()

    if artista is None:
        print(f"Artista '{nome_artista}' não encontrado. Cadastre-o primeiro.")
        return None

    cursor = conn.execute(
        """INSERT INTO albuns (titulo, ano, contexto, artista_id)
           VALUES (?, ?, ?, ?)""",
        (titulo, ano, contexto, artista[0])
    )
    conn.commit()
    return cursor.lastrowid


def adicionar_musica(titulo, album_id, link, letra=None, significado=None,
                     historia=None, visualizacoes=0):
    if album_id is None:
        print("Álbum inválido. Cadastre o álbum primeiro.")
        return None

    try:
        cursor = conn.execute(
            """INSERT INTO musicas
                   (titulo, letra, significado, historia, visualizacoes, link, albuns_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (titulo, letra, significado, historia, visualizacoes, link, album_id)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"Erro ao cadastrar música: {e}")
        return None


if __name__ == "__main__":
    adicionar_artista('rau', 'mpb', 'cara_louco')

    album_id = adicionar_album('Meu Album', 'rau', 2020)

    adicionar_musica(
        'Minha Música',
        album_id,
        link='https://example.com/minha-musica',
        letra='la la la',
        significado='algo',
        historia='algo'
    )

    for linha in conn.execute("SELECT * FROM musicas"):
        print(linha)