musicas = []

def add_musica():
    while (True):
        print("===Nova musica===")
        nome = input("Nome da música: ")
        nome_autor = input("Nome do autor: ")
        album = input("Nome do album: ")
        hist = input("Historia da musica: ")
        sig = input("Significado da música")
        letra = input("Letra: ")
        link = input("Link do YouTube: ")
        resposta = ("Deseja adicionar novamente? (S/N): ")
        if resposta.upper != "S":
                break
        musica = {nome: 'nome', nome_autor: 'nome_autor', letra: 'letra', link:'link', album: 'album', hist:'hist', sig: 'sig'}
        musicas.append(musica)

def ver_musica(conn, id, nome, artista):
     pesquisa = input("Digite o nome, artista ou id: ")
     """PROCURAR MUSICA EM BD"""
     conn = sqlite3.connect("musicas.db")
     conn.execute("SELECT (nome, artista, id) FROM musica WHERE nome ILIKE= (%+?+%) OR id ILIKE=(%+?+%)  OR artista ILIKE=(%+?+%)" (id, nome, artista,))
     for musica in pesquisa:
          """MOSTRAR OPCOES DE MUSICA PARA SELECIONAR, O USUARIO DIGITA O ID E A MUSICA CORRESPONDENTE APARECE COM AS INFORMAÇÕES ABAIXO"""
     print(f"Música: {musica['musica']} /nAutor: {musica['autor']} /nAlbum: {musica['album']} /nLetra: {musica['letra']} /nLink: {musica['link']}, /nSignificado: {musica['sig']} /nHistória: {musica['hist']}")