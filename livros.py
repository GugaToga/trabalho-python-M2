import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional

class Livros:
    """Classe para gerenciamento de livros e empréstimos."""

    BIBLIOTECA_FILE = Path("biblioteca.csv")
    EMPRESTIMOS_FILE = Path("emprestimos.csv")

    def CadastrarLivro(self, nome: str = None, autor: str = None,
                        publicacao: str = None, quantidade: Optional[int] = None) -> None:
        """
        Cadastra um novo livro na biblioteca.

        Args:
            nome (str, optional): Título do livro. Solicita input se None.
            autor (str, optional): Autor do livro. Solicita input se None.
            publicacao (str, optional): Ano de publicação. Solicita input se None.
            quantidade (int, optional): Quantidade de exemplares. Solicita input se None.
        """
        if nome is None:
            nome = input("Digite o nome do livro: ").strip()
        if autor is None:
            autor = input("Digite o nome do autor: ").strip()
        if publicacao is None:
            publicacao = input("Data de publicação: ").strip()
        if quantidade is None:
            try:
                quantidade = int(input("Quantidade de exemplares: ").strip())
            except ValueError:
                quantidade = 1

        escrever_cabecalho = not self.BIBLIOTECA_FILE.exists()

        with self.BIBLIOTECA_FILE.open("a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if escrever_cabecalho:
                escritor.writerow(["titulo","autor","data_publicacao","quantidade"])
            escritor.writerow([nome, autor, publicacao, quantidade])
        print(f"Livro '{nome}' cadastrado com sucesso!")

    def ListarEstoque(self) -> List[List[str]]:
        """Retorna a lista de livros disponíveis e exibe na tela."""
        livros = []
        if not self.BIBLIOTECA_FILE.exists():
            print("Nenhum livro cadastrado.")
            return livros

        with self.BIBLIOTECA_FILE.open("r", newline="", encoding="utf-8") as f:
            leitor = csv.reader(f)
            next(leitor, None)
            for linha in leitor:
                if len(linha) < 4:
                    continue
                livros.append(linha)

        if not livros:
            print("Nenhum livro cadastrado.")
            return livros

        print("\nLIVROS DISPONÍVEIS:")
        for i, livro in enumerate(livros, start=1):
            titulo, autor, data, quantidade = livro
            print(f"{i}. {titulo} ({autor}) - {data} | Quantidade: {quantidade}")
        return livros

    def Emprestimo(self, usuario_nome: str) -> None:
        """Realiza o empréstimo de um livro para um usuário."""
        livros = self.ListarEstoque()
        if not livros:
            return

        try:
            escolha = int(input("\nDigite o número do livro que deseja emprestar: ")) - 1
        except ValueError:
            print("Entrada inválida!")
            return

        if escolha < 0 or escolha >= len(livros):
            print("Número inválido!")
            return

        titulo, autor, _, quantidade = livros[escolha]
        if int(quantidade) <= 0:
            print("Livro indisponível para empréstimo.")
            return

        livros[escolha][3] = str(int(quantidade) - 1)

        # Atualiza biblioteca
        with self.BIBLIOTECA_FILE.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["titulo","autor","data_publicacao","quantidade"])
            escritor.writerows(livros)

        # Registra empréstimo
        data_emprestimo = datetime.now().strftime("%d/%m/%Y %H:%M")
        escrever_cabecalho = not self.EMPRESTIMOS_FILE.exists()
        with self.EMPRESTIMOS_FILE.open("a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if escrever_cabecalho:
                escritor.writerow(["usuario","titulo","autor","data_emprestimo"])
            escritor.writerow([usuario_nome, titulo, autor, data_emprestimo])
        print(f"Empréstimo realizado: {titulo} para {usuario_nome}.")

    def Devolucao(self) -> None:
        """Realiza a devolução de um livro emprestado."""
        livros = self.ListarEstoque()
        if not livros:
            return

        if not self.EMPRESTIMOS_FILE.exists():
            print("Nenhum empréstimo registrado.")
            return

        with self.EMPRESTIMOS_FILE.open("r", newline="", encoding="utf-8") as f:
            leitor = csv.reader(f)
            emprestimos = list(leitor)

        if len(emprestimos) <= 1:
            print("Nenhum empréstimo ativo.")
            return

        print("\n--- Empréstimos Ativos ---")
        for i, linha in enumerate(emprestimos[1:], start=1):
            usuario, titulo, autor, data_emprestimo = linha
            print(f"{i}. {titulo} ({autor}) - {usuario} - {data_emprestimo}")

        try:
            escolha = int(input("\nDigite o número do empréstimo que deseja devolver: ")) - 1
        except ValueError:
            print("Entrada inválida!")
            return

        if escolha < 0 or escolha >= len(emprestimos)-1:
            print("Número inválido!")
            return

        devolvido = emprestimos.pop(escolha+1)

        # Atualiza quantidade na biblioteca
        for livro in livros:
            if livro[0] == devolvido[1] and livro[1] == devolvido[2]:
                livro[3] = str(int(livro[3]) + 1)
                break

        # Reescreve arquivos
        with self.BIBLIOTECA_FILE.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["titulo","autor","data_publicacao","quantidade"])
            escritor.writerows(livros)

        with self.EMPRESTIMOS_FILE.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerows(emprestimos)

        print(f"Livro '{devolvido[1]}' devolvido com sucesso.")

    def Consultar(self) -> None:
        """Consulta livros por título ou autor e exibe os encontrados."""
        if not self.BIBLIOTECA_FILE.exists():
            print("Nenhum livro cadastrado ainda.")
            return

        with self.BIBLIOTECA_FILE.open("r", newline="", encoding="utf-8") as f:
            leitor = csv.reader(f)
            next(leitor, None)
            livros = [linha for linha in leitor if len(linha) >= 4]

        filtro = input("Digite o título ou autor para buscar (ou ENTER para listar todos): ").strip().lower()
        encontrados = []
        for livro in livros:
            titulo, autor, data, quantidade = livro
            if filtro == "" or filtro in titulo.lower() or filtro in autor.lower():
                encontrados.append(livro)

        if not encontrados:
            print("Nenhum livro encontrado com esses critérios.")
            return

        print("\nLIVROS ENCONTRADOS:")
        for i, livro in enumerate(encontrados, start=1):
            titulo, autor, data, quantidade = livro
            print(f"{i}. {titulo} ({autor}) - {data} | Quantidade: {quantidade}")
