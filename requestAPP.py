import os
print("Seja bem-vindo(a) ao Request APP")

while True:
    print("Selecione o arquivo Python que deseja executar:")
    print("1. requestAPI.py")
    print("2. requestSQL.py")
    print("Digite 'sair' para encerrar o programa.")

    choice = input("Digite 1, 2 ou sair: ")

    if choice == "1":
        os.system("python requestAPI.py")
    elif choice == "2":
        os.system("python requestSQL.py")
    elif choice == "sair":
        break
    else:
        print("Escolha inválida. Digite 1, 2 ou sair.")
