import sqlite3
import funcoes
conn = (sqlite3.connect('musicas.db'))



funcoes.adicionar_artista('rau', 'mpb', 'cara_louco')
funcoes.adicionar_album('Meu Album', 'rau', 2020)
funcoes.adicionar_musica('Minha Música', 'Meu Album',
                          letra='la la la',
                          significado='algo',
                          historia='algo',
                 nome_artista='rau',
                 link='https://example.com/minha-musica')