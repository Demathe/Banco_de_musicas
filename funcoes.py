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


def adicionar_musica(titulo, nome_album, nome_artista, link, letra=None,
                     significado=None, historia=None, visualizacoes=0):
    album = conn.execute(
        """SELECT albuns.id
           FROM albuns
           JOIN artista ON albuns.artista_id = artista.id
           WHERE albuns.titulo = ? AND artista.nome = ?""",
        (nome_album, nome_artista)
    ).fetchone()

    if album is None:
        print(f"Álbum '{nome_album}' de '{nome_artista}' não encontrado. Cadastre-o primeiro.")
        return None

    try:
        cursor = conn.execute(
            """INSERT INTO musicas
                   (titulo, letra, significado, historia, visualizacoes, link, albuns_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (titulo, letra, significado, historia, visualizacoes, link, album[0])
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"Erro ao cadastrar música: {e}")
        return None


def add_musica():
    while (True):
        print("===Nova musica===")
        nome = input("Nome da música: ")
        nome_autor = input("Nome do autor: ")
        album = input("Nome do album: ")
        hist = input("Historia da musica: ")
        sig = input("Significado da música: ")
        letra = input("Letra: ")
        link = input("Link do YouTube: ")
        adicionar_musica(nome, album, nome_autor, link, letra, sig, hist)
        resposta = input("Deseja adicionar novamente? (S/N): ")
        if resposta.upper() != "S":
                break

def add_album():
    while (True):
        print("===Novo álbum===")
        titulo = input("Título do álbum: ")
        nome_artista = input("Nome do artista: ")
        ano = int(input("Ano de lançamento: "))
        contexto = input("Contexto do álbum: ")
        adicionar_album(titulo, nome_artista, ano, contexto)
        resposta = input("Deseja adicionar outro álbum? (S/N): ")
        if resposta.upper() != "S":
                break

def add_artista():
    while (True):
        print("===Novo artista===")
        nome = input("Nome do artista: ")
        genero = input("Gênero musical: ")
        historia = input("História do artista: ")
        adicionar_artista(nome, genero, historia)
        resposta = input("Deseja adicionar outro artista? (S/N): ")
        if resposta.upper() != "S":
                break


def pesquisar_musicas(termo, limite=5):
    termo = termo.strip()
    contem = f"%{termo}%"
    comeca = f"{termo}%"

    return conn.execute(
        """SELECT musicas.id,
                  musicas.titulo AS musica,
                  artista.nome   AS artista,
                  albuns.titulo  AS album
           FROM musicas
           JOIN albuns  ON musicas.albuns_id = albuns.id
           JOIN artista ON albuns.artista_id = artista.id
           WHERE musicas.titulo LIKE ?
              OR artista.nome  LIKE ?
              OR albuns.titulo LIKE ?
           ORDER BY
              CASE
                  WHEN musicas.titulo = ? COLLATE NOCASE THEN 0
                  WHEN artista.nome   = ? COLLATE NOCASE THEN 1
                  WHEN albuns.titulo  = ? COLLATE NOCASE THEN 2
                  WHEN musicas.titulo LIKE ?             THEN 3
                  WHEN artista.nome   LIKE ?             THEN 4
                  WHEN albuns.titulo  LIKE ?             THEN 5
                  ELSE 6
              END,
              musicas.visualizacoes DESC,
              albuns.titulo,
              musicas.titulo
           LIMIT ?""",
        (
            contem, contem, contem,     # WHERE (3)
            termo, termo, termo,        # CASE: igual (3)
            comeca, comeca, comeca,     # CASE: começa com (3)
            limite                      # LIMIT (1)
        )
    ).fetchall()

def ver_musica():
    termo = input("Digite o nome da música, artista ou álbum: ").strip()
    if not termo:
        print("Digite algo para pesquisar.")
        return

    resultados = pesquisar_musicas(termo)

    if not resultados:
        print("Nenhuma música encontrada.")
        return

    print("\nResultados:")
    for i, r in enumerate(resultados, start=1):
        print(f"{i} - {r['musica']} - {r['artista']} ({r['album']})")

    escolha = input("\nDigite o número da música: ")
    if not escolha.isdigit() or not (1 <= int(escolha) <= len(resultados)):
        print("Opção inválida.")
        return

    musica_id = resultados[int(escolha) - 1]['id']

    musica = conn.execute(
        """SELECT musicas.titulo AS musica,
                  artista.nome   AS artista,
                  albuns.titulo  AS album,
                  musicas.letra, musicas.link,
                  musicas.significado AS sig,
                  musicas.historia    AS hist
           FROM musicas
           JOIN albuns  ON musicas.albuns_id = albuns.id
           JOIN artista ON albuns.artista_id = artista.id
           WHERE musicas.id = ?""",
        (musica_id,)
    ).fetchone()

    print(f"\nMúsica: {musica['musica']}")
    print(f"Autor: {musica['artista']}")
    print(f"Álbum: {musica['album']}")
    print(f"Letra: {musica['letra']}")
    print(f"Link: {musica['link']}")
    print(f"Significado: {musica['sig']}")
    print(f"História: {musica['hist']}")