
import sqlite3
from pathlib import Path
from contextlib import contextmanager


# ==========================================
# CONFIGURAÇÃO DO BANCO
# ==========================================

CAMINHO_BANCO = Path(__file__).resolve().parent / "musicbase.db"


@contextmanager
def obter_conexao():
    """Cria uma conexão segura com o banco de dados."""

    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==========================================
# CRIAÇÃO DAS TABELAS
# ==========================================

def criar_banco():

    with obter_conexao() as conn:

        cursor = conn.cursor()

        # Tabela de artistas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artistas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                genero TEXT,
                historia TEXT
            );
        """)

        # Tabela de álbuns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS albuns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                ano INTEGER,
                contexto TEXT,
                artista_id INTEGER NOT NULL,

                UNIQUE(titulo, artista_id),

                FOREIGN KEY (artista_id)
                    REFERENCES artistas(id)
                    ON DELETE CASCADE
            );
        """)

        # Tabela de músicas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS musicas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                letra TEXT,
                significado TEXT,
                humor TEXT,
                url_musica TEXT,
                visualizacoes INTEGER DEFAULT 0,
                album_id INTEGER NOT NULL,

                UNIQUE(titulo, album_id),

                FOREIGN KEY (album_id)
                    REFERENCES albuns(id)
                    ON DELETE CASCADE
            );
        """)

    print("Banco de dados inicializado!")


# ==========================================
# CADASTRO RELACIONAL
# ==========================================

def cadastrar_tudo_no_banco(artista, album, musica):

    # Verifica os campos obrigatórios
    if not artista.get("nome", "").strip():
        raise ValueError("O nome do artista é obrigatório.")

    if not album.get("titulo", "").strip():
        raise ValueError("O título do álbum é obrigatório.")

    if not musica.get("titulo", "").strip():
        raise ValueError("O título da música é obrigatório.")

    with obter_conexao() as conn:

        cursor = conn.cursor()

        # 1. ARTISTA

        cursor.execute("""
            INSERT OR IGNORE INTO artistas
            (nome, genero, historia)
            VALUES (?, ?, ?);
        """, (
            artista["nome"].strip(),
            artista.get("genero", "").strip(),
            artista.get("historia", "").strip()
        ))

        cursor.execute("""
            SELECT id FROM artistas
            WHERE nome = ? COLLATE NOCASE;
        """, (artista["nome"].strip(),))

        resultado = cursor.fetchone()

        if resultado is None:
            raise ValueError("Erro ao localizar artista.")

        artista_id = resultado["id"]

        # 2. ÁLBUM

        cursor.execute("""
            INSERT OR IGNORE INTO albuns
            (titulo, ano, contexto, artista_id)
            VALUES (?, ?, ?, ?);
        """, (
            album["titulo"].strip(),
            album.get("ano"),
            album.get("contexto", "").strip(),
            artista_id
        ))

        cursor.execute("""
            SELECT id FROM albuns
            WHERE titulo = ? COLLATE NOCASE
              AND artista_id = ?;
        """, (
            album["titulo"].strip(),
            artista_id
        ))

        resultado = cursor.fetchone()

        if resultado is None:
            raise ValueError("Erro ao localizar álbum.")

        album_id = resultado["id"]

        # 3. MÚSICA

        cursor.execute("""
            INSERT OR IGNORE INTO musicas
            (
                titulo,
                letra,
                significado,
                humor,
                url_musica,
                album_id
            )
            VALUES (?, ?, ?, ?, ?, ?);
        """, (
            musica["titulo"].strip(),
            musica.get("letra", "").strip(),
            musica.get("significado", "").strip(),
            musica.get("humor", "").strip(),
            musica.get("url_musica", "").strip(),
            album_id
        ))

        cursor.execute("""
            SELECT id FROM musicas
            WHERE titulo = ? COLLATE NOCASE
              AND album_id = ?;
        """, (
            musica["titulo"].strip(),
            album_id
        ))

        resultado = cursor.fetchone()

        if resultado is None:
            raise ValueError("Erro ao localizar música.")

        musica_id = resultado["id"]

        return {
            "artista_id": artista_id,
            "album_id": album_id,
            "musica_id": musica_id
        }


# ==========================================
# MÚSICA PADRÃO
# ==========================================

def popular_banco_inicial():

    with obter_conexao() as conn:

        quantidade = conn.execute(
            "SELECT COUNT(*) FROM musicas;"
        ).fetchone()[0]

    # Não popula novamente se já houver músicas
    if quantidade > 0:
        return

    artista = {
        "nome": "Legião Urbana",
        "genero": "Rock brasileiro",
        "historia": (
            "A Legião Urbana foi uma banda brasileira "
            "de rock formada em Brasília em 1982. "
            "Tornou-se um dos principais nomes do rock "
            "nacional, abordando temas sociais, "
            "sentimentos e questões da juventude."
        )
    }

    album = {
        "titulo": "Dois",
        "ano": 1986,
        "contexto": (
            "Segundo álbum de estúdio da Legião Urbana, "
            "lançado em 1986. O disco consolidou a "
            "identidade musical da banda no rock brasileiro."
        )
    }

    musica = {
        "titulo": "Tempo Perdido",
        "letra": "",
        "significado": (
            "A música apresenta reflexões sobre o tempo, "
            "a juventude, as escolhas e a importância "
            "de aproveitar o presente."
        ),
        "humor": "Reflexiva",
        "url_musica": ""
    }

    cadastrar_tudo_no_banco(
        artista,
        album,
        musica
    )

    print("Música padrão cadastrada!")


# ==========================================
# INICIALIZAÇÃO
# ==========================================

def inicializar_banco():

    criar_banco()
    popular_banco_inicial()


if __name__ == "__main__":
    inicializar_banco()
