
import streamlit as st

from banco import inicializar_banco, cadastrar_tudo_no_banco

from funcoes import (
    buscar_musicas,
    buscar_por_artista,
    buscar_por_album,
    buscar_historia_artista,
    buscar_artistas_por_termo,
    buscar_albuns_por_termo,
    buscar_detalhes_album,
    obter_top_5,
    registrar_visualizacao,
    buscar_musica_por_id,
    buscar_por_humor,
    listar_artistas,
    listar_musicas,
    listar_humores
)


# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="MusicBase",
    page_icon="🎵",
    layout="wide"
)


# Inicializa o banco
inicializar_banco()


# ==========================================
# ESTILO VISUAL
# ==========================================

st.markdown("""
<style>

    .titulo-musicbase {
        font-size: 42px;
        font-weight: bold;
        color: #D6A84B;
    }

    .subtitulo {
        color: #A0A0A0;
        font-size: 17px;
    }

    .resultado {
        padding: 10px;
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# CABEÇALHO
# ==========================================

st.markdown(
    '<div class="titulo-musicbase">🎵 MusicBase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Muito além da música. Descubra histórias, '
    'artistas e significados.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def exibir_musica(musica):

    st.divider()

    st.header(f"🎵 {musica['titulo']}")

    st.write(f"**Artista:** {musica['artista']}")
    st.write(f"**Álbum:** {musica['album']}")

    if musica["ano"]:
        st.write(f"**Ano:** {musica['ano']}")

    st.caption(
        f"👁️ {musica['visualizacoes']} visualizações"
    )

    # LETRA

    st.markdown("### 📝 Letra da música")

    if musica["letra"]:

        st.text_area(
            "Letra",
            value=musica["letra"],
            height=250,
            disabled=True,
            key=f"letra_{musica['id']}"
        )

    else:

        st.info("A letra ainda não foi cadastrada.")

    # SIGNIFICADO

    st.markdown("### 📖 Significado")

    st.write(
        musica["significado"] or
        "Significado ainda não cadastrado."
    )

    # HUMOR

    if musica["humor"]:

        st.write(f"**Vibe:** {musica['humor']}")

    # PLAYER

    if musica["url_musica"]:

        st.markdown("### ▶️ Ouça a música")

        try:
            st.video(musica["url_musica"])
        except Exception:
            st.warning("Não foi possível carregar o vídeo.")

    else:

        st.info("Esta música ainda não possui um vídeo cadastrado.")


# ==========================================
# SELEÇÃO DE MÚSICAS
# ==========================================

def exibir_lista_musicas(musicas, chave):

    if not musicas:

        st.warning("Nenhuma música encontrada.")
        return

    opcoes = {
        (
            f"{m['titulo']} — {m['artista']} "
            f"({m['album']})"
        ): m["id"]

        for m in musicas
    }

    escolha = st.selectbox(
        "Selecione uma música:",
        list(opcoes.keys()),
        key=f"selecao_{chave}"
    )

    if st.button(
        "Abrir música",
        key=f"abrir_{chave}"
    ):

        musica_id = opcoes[escolha]

        # Atualiza somente quando o usuário abre a música
        if registrar_visualizacao(musica_id):

            st.session_state["musica_aberta"] = musica_id


def exibir_musica_selecionada():

    musica_id = st.session_state.get("musica_aberta")

    if musica_id is not None:

        musica = buscar_musica_por_id(musica_id)

        if musica:

            exibir_musica(musica)


# ==========================================
# TOP 5
# ==========================================

def exibir_top_5():

    st.subheader("🏆 Top 5 músicas mais acessadas")

    ranking = obter_top_5()

    if not ranking:

        st.info("Ainda não existem músicas cadastradas.")
        return

    for posicao, musica in enumerate(ranking, start=1):

        st.write(
            f"**{posicao}º — {musica['titulo']}**"
        )

        st.caption(
            f"{musica['artista']} | "
            f"{musica['album']} | "
            f"👁️ {musica['visualizacoes']} acessos"
        )

        st.divider()


# ==========================================
# QUATRO ABAS PRINCIPAIS
# ==========================================

aba_explorar, aba_cultura, aba_interatividade, aba_admin = st.tabs([
    "🔍 Explorar & Buscar",
    "📖 Cultura Pop",
    "🎮 Interatividade",
    "⚙️ Administração"
])


# ==========================================
# ABA 1 — EXPLORAR E BUSCAR
# ==========================================

with aba_explorar:

    st.header("🔍 Encontre sua música")

    st.write(
        "Pesquise por título, trecho da letra, "
        "artista, álbum ou gênero musical."
    )

    # PESQUISA ÚNICA

    with st.form("form_busca_principal"):

        termo = st.text_input(
            "O que você está procurando?",
            placeholder="Ex.: Tempo Perdido, Legião Urbana ou trecho da letra..."
        )

        pesquisar = st.form_submit_button(
            "🔍 Pesquisar",
            use_container_width=True
        )

    if pesquisar:

        if termo.strip():

            resultados = buscar_musicas(termo)

            st.session_state["resultados_busca"] = resultados
            st.session_state["termo_busca"] = termo

            st.session_state["artistas_encontrados"] = (
                buscar_artistas_por_termo(termo)
            )

            st.session_state["albuns_encontrados"] = (
                buscar_albuns_por_termo(termo)
            )

            st.session_state["musica_aberta"] = None

        else:

            st.warning("Digite algo para pesquisar.")

    # RESULTADOS

    if "resultados_busca" in st.session_state:

        resultados = st.session_state["resultados_busca"]

        artistas_encontrados = st.session_state.get(
            "artistas_encontrados", []
        )

        albuns_encontrados = st.session_state.get(
            "albuns_encontrados", []
        )

        # BIOGRAFIA ANTES DAS MÚSICAS

        if artistas_encontrados:

            st.markdown("## 📚 História do artista")

            for artista in artistas_encontrados:

                st.subheader(artista["nome"])

                st.write(
                    f"**Gênero:** {artista['genero']}"
                )

                st.write(
                    artista["historia"] or
                    "História ainda não cadastrada."
                )

        # CONTEXTO DO ÁLBUM ANTES DAS MÚSICAS

        if albuns_encontrados:

            st.markdown("## 💿 Álbuns encontrados")

            for album in albuns_encontrados:

                with st.expander(
                    f"{album['titulo']} — {album['artista']}"
                ):

                    st.write(
                        f"**Ano:** {album['ano'] or 'Não informado'}"
                    )

                    st.write(
                        album["contexto"] or
                        "Contexto ainda não cadastrado."
                    )

        # RESULTADOS MUSICAIS

        st.markdown("## 🎼 Músicas encontradas")

        if resultados:

            st.success(
                f"{len(resultados)} música(s) encontrada(s)."
            )

            exibir_lista_musicas(
                resultados,
                "explorar"
            )

        else:

            st.info(
                "Nenhuma música encontrada para essa pesquisa."
            )

        # MÚSICA SELECIONADA

        exibir_musica_selecionada()

    st.divider()

    # RANKING

    exibir_top_5()


# ==========================================
# ABA 2 — CULTURA POP
# ==========================================

with aba_cultura:

    st.header("📖 Cultura Pop")

    st.write(
        "Explore a história dos artistas e os "
        "significados por trás das músicas."
    )

    subaba_artistas, subaba_musicas = st.tabs([
        "🎸 História das bandas",
        "💭 Significado das músicas"
    ])

    # HISTÓRIA DAS BANDAS

    with subaba_artistas:

        artistas = listar_artistas()

        if artistas:

            nomes = [a["nome"] for a in artistas]

            artista_escolhido = st.selectbox(
                "Escolha um artista:",
                nomes,
                key="cultura_artista"
            )

            if st.button(
                "Consultar biografia",
                key="consultar_biografia"
            ):

                historia = buscar_historia_artista(
                    artista_escolhido
                )

                if historia:

                    st.markdown(
                        f"## 🎸 {historia['nome']}"
                    )

                    st.write(
                        f"**Gênero:** {historia['genero']}"
                    )

                    st.write(
                        historia["historia"] or
                        "Biografia não cadastrada."
                    )

        else:

            st.info("Nenhum artista cadastrado.")

    # SIGNIFICADOS

    with subaba_musicas:

        musicas = listar_musicas()

        if musicas:

            opcoes = {
                f"{m['titulo']} — {m['artista']}": m["id"]
                for m in musicas
            }

            escolha = st.selectbox(
                "Escolha uma música:",
                list(opcoes.keys()),
                key="cultura_significado"
            )

            if st.button(
                "Descobrir significado",
                key="consultar_significado"
            ):

                musica = buscar_musica_por_id(
                    opcoes[escolha]
                )

                if musica:

                    st.markdown(
                        f"## 🎵 {musica['titulo']}"
                    )

                    st.write(
                        f"**Artista:** {musica['artista']}"
                    )

                    st.write(
                        f"**Álbum:** {musica['album']}"
                    )

                    st.markdown("### 📖 Significado")

                    st.write(
                        musica["significado"] or
                        "Significado ainda não cadastrado."
                    )

        else:

            st.info("Nenhuma música cadastrada.")


# ==========================================
# ABA 3 — INTERATIVIDADE
# ==========================================

with aba_interatividade:

    st.header("🎮 Descubra músicas pela sua vibe")

    st.write(
        "Escolha um humor e encontre músicas "
        "que combinam com seu momento."
    )

    humores = listar_humores()

    if humores:

        humor_escolhido = st.selectbox(
            "Como você está se sentindo?",
            humores,
            key="filtro_humor"
        )

        if st.button(
            "Encontrar músicas",
            key="buscar_humor"
        ):

            resultados_humor = buscar_por_humor(
                humor_escolhido
            )

            st.session_state["resultados_humor"] = resultados_humor
            st.session_state["musica_aberta"] = None

        if "resultados_humor" in st.session_state:

            resultados_humor = st.session_state[
                "resultados_humor"
            ]

            if resultados_humor:

                st.success(
                    f"{len(resultados_humor)} música(s) encontradas!"
                )

                exibir_lista_musicas(
                    resultados_humor,
                    "humor"
                )

                exibir_musica_selecionada()

            else:

                st.info("Nenhuma música encontrada para essa vibe.")

    else:

        st.info(
            "Cadastre músicas com diferentes humores "
            "para utilizar essa funcionalidade."
        )

    st.divider()

    st.markdown("### 💡 Exemplos de vibes")

    st.write(
        "😊 Feliz | 😢 Triste | ❤️ Romântica | "
        "🔥 Energética | 🌙 Reflexiva | "
        "✨ Nostálgica"
    )


# ==========================================
# ABA 4 — ADMINISTRAÇÃO
# ==========================================

with aba_admin:

    st.header("⚙️ Administração")

    st.write(
        "Cadastre novos artistas, álbuns e músicas "
        "no banco de dados do MusicBase."
    )

    with st.form("formulario_cadastro"):

        # ARTISTA

        st.subheader("🎸 Artista")

        nome_artista = st.text_input(
            "Nome do artista ou banda *"
        )

        genero = st.text_input(
            "Gênero musical"
        )

        historia = st.text_area(
            "História do artista"
        )

        st.divider()

        # ÁLBUM

        st.subheader("💿 Álbum")

        titulo_album = st.text_input(
            "Nome do álbum *"
        )

        ano_album = st.number_input(
            "Ano de lançamento",
            min_value=0,
            max_value=2100,
            value=0
        )

        contexto = st.text_area(
            "Contexto histórico do álbum"
        )

        st.divider()

        # MÚSICA

        st.subheader("🎵 Música")

        titulo_musica = st.text_input(
            "Nome da música *"
        )

        letra = st.text_area(
            "Letra da música",
            height=200
        )

        significado = st.text_area(
            "Significado da música"
        )

        humor = st.selectbox(
            "Humor / Vibe",
            [
                "Feliz",
                "Triste",
                "Romântica",
                "Energética",
                "Reflexiva",
                "Nostálgica",
                "Motivacional",
                "Calma",
                "Outro"
            ]
        )

        url_musica = st.text_input(
            "Link do vídeo ou música"
        )

        st.caption(
            "* Campos obrigatórios. Utilize apenas "
            "letras que você tenha autorização para armazenar."
        )

        cadastrar = st.form_submit_button(
            "💾 Cadastrar no MusicBase",
            use_container_width=True
        )

        if cadastrar:

            if not nome_artista.strip():

                st.error("Informe o nome do artista.")

            elif not titulo_album.strip():

                st.error("Informe o nome do álbum.")

            elif not titulo_musica.strip():

                st.error("Informe o nome da música.")

            else:

                artista = {
                    "nome": nome_artista,
                    "genero": genero,
                    "historia": historia
                }

                album = {
                    "titulo": titulo_album,
                    "ano": ano_album if ano_album > 0 else None,
                    "contexto": contexto
                }

                musica = {
                    "titulo": titulo_musica,
                    "letra": letra,
                    "significado": significado,
                    "humor": humor,
                    "url_musica": url_musica
                }

                try:

                    ids = cadastrar_tudo_no_banco(
                        artista,
                        album,
                        musica
                    )

                    st.success(
                        "Cadastro realizado ou registros existentes reutilizados!"
                    )

                    st.write(
                        f"Artista ID: {ids['artista_id']}"
                    )

                    st.write(
                        f"Álbum ID: {ids['album_id']}"
                    )

                    st.write(
                        f"Música ID: {ids['musica_id']}"
                    )

                except Exception as erro:

                    st.error(
                        f"Não foi possível cadastrar: {erro}"
                    )


# ==========================================
# RODAPÉ
# ==========================================

st.divider()

st.caption(
    "🎵 MusicBase — Cultura, história e música em um só lugar."
)
