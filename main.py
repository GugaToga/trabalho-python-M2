from usuarios import Usuarios
from livros import Livros

def menu1() -> None:
    """Menu inicial: login, cadastro ou sair."""
    print("Bem-vindo à Biblioteca\n")
    print("1 - Login")
    print("2 - Cadastro")
    print("3 - Sair")

    try:
        escolha = int(input("Escolha: "))
    except ValueError:
        print("Opção inválida!")
        return

    match escolha:
        case 1:
            if Usuarios.ValidarUsuario():
                menu2()
            else:
                print("Nome ou CPF inválidos!")
        case 2:
            Usuarios.CadastrarUsuario()
        case 3:
            print("Saindo...")
            exit(0)
        case _:
            print("Opção inválida!")

def menu2() -> None:
    """Menu do usuário após login."""
    biblioteca = Livros()
    while True:
        print("\n--- Menu ---")
        print("1 - Cadastrar livro")
        print("2 - Fazer empréstimo")
        print("3 - Devolução de livro")
        print("4 - Consultar livros")
        print("5 - Sair")

        try:
            escolha = int(input("O que deseja fazer hoje: "))
        except ValueError:
            print("Opção inválida!")
            continue

        match escolha:
            case 1:
                biblioteca.CadastrarLivro()
            case 2:
                usuario_nome = input("Digite seu nome: ").strip()
                biblioteca.Emprestimo(usuario_nome)
            case 3:
                biblioteca.Devolucao()
            case 4:
                biblioteca.Consultar()
            case 5:
                print("Saindo...")
                break
            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    while True:
        menu1()
