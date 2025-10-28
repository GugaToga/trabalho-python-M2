import csv
from pathlib import Path

class Usuarios:
    """Classe para cadastro e validação de usuários."""

    CSV_FILE = Path("usuarios.csv")

    @staticmethod
    def CadastrarUsuario(nome: str = None, cpf: str = None) -> None:
        """
        Cadastra um novo usuário na biblioteca.

        Args:
            nome (str, optional): Nome do usuário. Solicita input se None.
            cpf (str, optional): CPF do usuário. Solicita input se None.
        """
        if nome is None:
            nome = input("Digite seu nome: ").strip()
        if cpf is None:
            cpf = input("Digite seu CPF: ").strip()

        escrever_cabecalho = not Usuarios.CSV_FILE.exists()

        with Usuarios.CSV_FILE.open("a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if escrever_cabecalho:
                escritor.writerow(["nome", "cpf"])
            escritor.writerow([nome, cpf])
        print(f"Usuário '{nome}' cadastrado com sucesso!")

    @staticmethod
    def ValidarUsuario(nome: str = None, cpf: str = None) -> bool:
        """
        Valida login do usuário pelo nome e CPF.

        Args:
            nome (str, optional): Nome do usuário. Solicita input se None.
            cpf (str, optional): CPF do usuário. Solicita input se None.

        Returns:
            bool: True se usuário existe, False caso contrário.
        """
        if nome is None:
            nome = input("Digite seu nome: ").strip()
        if cpf is None:
            cpf = input("Digite seu CPF: ").strip()

        if not Usuarios.CSV_FILE.exists():
            return False

        with Usuarios.CSV_FILE.open("r", newline="", encoding="utf-8") as f:
            leitor = csv.reader(f)
            next(leitor, None)  # pular cabeçalho
            for linha in leitor:
                if len(linha) < 2:
                    continue
                if linha[0] == nome and linha[1] == cpf:
                    return True
        return False
