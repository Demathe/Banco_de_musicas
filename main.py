import sqlite3 as sqlite

print("=== Menu ===")
print("(1) - Adicionar música")
print("(2) - Pegar música")
print("(3) - Top 10 musicas")
print("(4) - surpreenda me")

while (True):
    perguntar = int(input("Digite qual opção você deseja: "))
    if perguntar == 1:
        print("Adicionando música...")
    elif perguntar == 2:
        pass
    elif perguntar == 3:
        pass
    elif perguntar == 4:
        pass
    else:
        print("Opção inválida, tente novamente.")