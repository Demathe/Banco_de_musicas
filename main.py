
import sqlite3 as sqlite

while True:

    print("\n========== MUSICBASE ==========")
    print("(1) - Pesquisar músicas/artistas/álbuns")
    print("(2) - Top 10 músicas")
    print("(3) - Modificar conteúdo")
    print("(4) - Surpreenda-me")
    print("(0) - Sair")

    perguntar = int(input("\nDigite a opção desejada: "))

    # PESQUISAR
    if perguntar == 1:

        print("\n========== PESQUISAR ==========")
        
    # TOP 10
    elif perguntar == 2:

        print("\n========== TOP 10 ==========")
        # Código para mostrar as 10 músicas mais acessadas

    # MODIFICAR CONTEÚDO
    elif perguntar == 3:

        print("\n========== ADMINISTRAÇÃO ==========")
        print("(1) - Adicionar")
        print("(2) - Editar")
        print("(3) - Remover")
        print("(0) - Voltar")

        perguntar = int(input("Escolha: "))

        if perguntar == 1:

            print("\n========== ADICIONAR ==========")
            print("(1) - Música")
            print("(2) - Artista")
            print("(3) - Álbum")
            print("(0) - Voltar")

            perguntar = int(input("Escolha: "))

            if perguntar == 1:
                print("\n=== Adicionar música ===")

            elif perguntar == 2:
                print("\n=== Adicionar artista ===")

            elif perguntar == 3:
                print("\n=== Adicionar álbum ===")

            elif perguntar == 0:
                continue

            else:
                print("Opção inválida!")

        elif perguntar == 2:

            print("\n========== EDITAR ==========")
            print("(1) - Música")
            print("(2) - Artista")
            print("(3) - Álbum")
            print("(0) - Voltar")

            perguntar = int(input("Escolha: "))

            if perguntar == 1:
                print("\n=== Editar música ===")

            elif perguntar == 2:
                print("\n=== Editar artista ===")

            elif perguntar == 3:
                print("\n=== Editar álbum ===")

            elif perguntar == 0:
                continue

            else:
                print("Opção inválida!")

        elif perguntar == 3:

            print("\n========== REMOVER ==========")
            print("(1) - Música")
            print("(2) - Artista")
            print("(3) - Álbum")
            print("(0) - Voltar")

            perguntar = int(input("Escolha: "))

            if perguntar == 1:
                print("\n=== Remover música ===")

            elif perguntar == 2:
                print("\n=== Remover artista ===")

            elif perguntar == 3:
                print("\n=== Remover álbum ===")

            elif perguntar == 0:
                continue

            else:
                print("Opção inválida!")

        elif perguntar == 0:
            continue

        else:
            print("Opção inválida!")

    # SURPREENDA-ME
    elif perguntar == 4:

        print("\n========== SURPREENDA-ME ==========")
        # Código para selecionar uma música aleatória

    # SAIRs
    elif perguntar == 0:

        print("\nObrigado por utilizar o MusicBase!")
        break

    else:
        print("Opção inválida! Tente novamente.")
