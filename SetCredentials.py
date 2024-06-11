import getpass
import keyring

servicename = "AssetLogin"
username = "asset@assetimoveis.com"

if keyring.get_password(servicename, username):
    print("Senha já cadastrada. Deseja deletar? (Y/N)")
    opt = input()
    if opt == "Y" or opt == "y":
        keyring.delete_password(servicename, username)
        if not keyring.get_password(servicename, username):
            print("Senha deletada com sucesso! Deseja cadastrar nova senha? (Y/N)")
            new_opt = input()
            if new_opt == "Y" or new_opt == "y":
                print("Digite a nova senha do Canal Pro:")
                password = getpass.getpass(prompt="Senha: ")
                keyring.set_password(servicename, username, password)
                if keyring.get_password(servicename, username):
                    print("Nova senha cadastrada com sucesso!")

            else:
                print("Senha descadastrada")

    else:
        print("Senha mantida")
else:
    print("Nenhuma senha cadastrada!\nDigite a senha do Canal Pro:")
    password = getpass.getpass(prompt="Senha: ")
    keyring.set_password(servicename, username, password)
    if keyring.get_password(servicename, username):
        print("Nova senha cadastrada com sucesso!")




