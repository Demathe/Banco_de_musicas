
from banco import obter_conexao


# ==========================================
# PESQUISA GERAL
# ==========================================

def buscar_musicas(termo):

    if not termo or not termo.strip():
        return []

    pesquisa = f"%{termo.strip()}%"

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                musicas.*,
                albuns.titulo AS album,
                albuns.ano AS ano,
                albuns.contexto AS contexto_album,
                artistas.nome AS artista,
                artistas.genero AS genero,
                artistas.historia AS historia_artista

            FROM musicas

            INNER JOIN albuns
                ON musicas.album_id = albuns.id

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            WHERE musicas.titulo LIKE ?
               OR musicas.letra LIKE ?
               OR musicas.significado LIKE ?
               OR artistas.nome LIKE ?
               OR artistas.genero LIKE ?
               OR artistas.historia LIKE ?
               OR albuns.titulo LIKE ?
               OR albuns.contexto LIKE ?

            ORDER BY musicas.titulo;
        """, (pesquisa,) * 8)

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# BUSCAR POR ARTISTA
# ==========================================

def buscar_por_artista(nome_artista):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                musicas.*,
                albuns.titulo AS album,
                albuns.ano AS ano,
                artistas.nome AS artista

            FROM musicas

            INNER JOIN albuns
                ON musicas.album_id = albuns.id

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            WHERE artistas.nome LIKE ?

            ORDER BY albuns.ano, musicas.titulo;
        """, (f"%{nome_artista.strip()}%",))

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# BUSCAR POR ÁLBUM
# ==========================================

def buscar_por_album(nome_album):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                musicas.*,
                albuns.titulo AS album,
                albuns.ano AS ano,
                artistas.nome AS artista

            FROM musicas

            INNER JOIN albuns
                ON musicas.album_id = albuns.id

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            WHERE albuns.titulo LIKE ?

            ORDER BY musicas.titulo;
        """, (f"%{nome_album.strip()}%",))

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# HISTÓRIA DO ARTISTA
# ==========================================

def buscar_historia_artista(nome_artista):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM artistas
            WHERE nome LIKE ?
            ORDER BY nome
            LIMIT 1;
        """, (f"%{nome_artista.strip()}%",))

        resultado = cursor.fetchone()

        return dict(resultado) if resultado else None


# ==========================================
# LISTAR ARTISTAS QUE COMBINAM COM A BUSCA
# ==========================================

def buscar_artistas_por_termo(termo):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM artistas
            WHERE nome LIKE ?
            ORDER BY nome;
        """, (f"%{termo.strip()}%",))

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# DETALHES DO ÁLBUM
# ==========================================

def buscar_detalhes_album(album_busca):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                albuns.*,
                artistas.nome AS artista,
                artistas.genero AS genero

            FROM albuns

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            WHERE albuns.titulo LIKE ?

            ORDER BY albuns.ano
            LIMIT 1;
        """, (f"%{album_busca.strip()}%",))

        resultado = cursor.fetchone()

        return dict(resultado) if resultado else None


# ==========================================
# LISTAR ÁLBUNS QUE COMBINAM COM A BUSCA
# ==========================================

def buscar_albuns_por_termo(termo):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                albuns.*,
                artistas.nome AS artista

            FROM albuns

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            WHERE albuns.titulo LIKE ?

            ORDER BY albuns.ano;
        """, (f"%{termo.strip()}%",))

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# TOP 5 MAIS VISUALIZADAS
# ==========================================

def obter_top_5():

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                musicas.id,
                musicas.titulo,
                musicas.visualizacoes,
                albuns.titulo AS album,
                artistas.nome AS artista

            FROM musicas

            INNER JOIN albuns
                ON musicas.album_id = albuns.id

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            ORDER BY musicas.visualizacoes DESC,
                     musicas.titulo ASC

            LIMIT 5;
        """)

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# REGISTRAR VISUALIZAÇÃO
# ==========================================

def registrar_visualizacao(musica_id):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE musicas
            SET visualizacoes = visualizacoes + 1
            WHERE id = ?;
        """, (musica_id,))

        return cursor.rowcount > 0


# ==========================================
# BUSCAR MÚSICA PELO ID
# ==========================================

def buscar_musica_por_id(musica_id):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                musicas.*,
                albuns.titulo AS album,
                albuns.ano AS ano,
                albuns.contexto AS contexto_album,
                artistas.nome AS artista,
                artistas.genero AS genero,
                artistas.historia AS historia_artista

            FROM musicas

            INNER JOIN albuns
                ON musicas.album_id = albuns.id

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            WHERE musicas.id = ?;
        """, (musica_id,))

        resultado = cursor.fetchone()

        return dict(resultado) if resultado else None


# ==========================================
# BUSCAR POR HUMOR
# ==========================================

def buscar_por_humor(humor):

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                musicas.*,
                albuns.titulo AS album,
                artistas.nome AS artista

            FROM musicas

            INNER JOIN albuns
                ON musicas.album_id = albuns.id

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            WHERE LOWER(musicas.humor) = LOWER(?)

            ORDER BY musicas.titulo;
        """, (humor,))

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# LISTAR ARTISTAS
# ==========================================

def listar_artistas():

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM artistas
            ORDER BY nome;
        """)

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# LISTAR MÚSICAS
# ==========================================

def listar_musicas():

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                musicas.id,
                musicas.titulo,
                artistas.nome AS artista,
                albuns.titulo AS album

            FROM musicas

            INNER JOIN albuns
                ON musicas.album_id = albuns.id

            INNER JOIN artistas
                ON albuns.artista_id = artistas.id

            ORDER BY musicas.titulo;
        """)

        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# LISTAR HUMORES
# ==========================================

def listar_humores():

    with obter_conexao() as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT humor
            FROM musicas
            WHERE humor IS NOT NULL
              AND TRIM(humor) != ''
            ORDER BY humor;
        """)

        return [row["humor"] for row in cursor.fetchall()]
