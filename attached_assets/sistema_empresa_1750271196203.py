class Empregado:
    contador_id = 1

    def __init__(self, nome, cpf, telefone, endereco, setor="Nenhum"):
        self.id = Empregado.contador_id
        Empregado.contador_id += 1

        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.setor = setor

    def editar_dados(self):
        print(f"\n--- Editar dados de {self.nome} ---")
        self.telefone = input("Novo telefone: ")
        self.endereco = input("Novo endereço: ")
        print("Dados atualizados com sucesso.\n")


class Setor:
    def __init__(self, nome):
        self.nome = nome
        self.equipe = []

    def adicionar_empregado(self, empregado):
        self.equipe.append(empregado)

    def remover_empregado(self, empregado):
        self.equipe.remove(empregado)


# Dados
empregados = []
setores = []


# Funções
def validar_numero(texto):
    if not texto.isdigit():
        print("⚠️ Entrada inválida. Digite apenas números.")
        return False
    return True


def cadastrar_empregado():
    print("\n--- Cadastrar Empregado ---")
    nome = input("Nome (ou Enter para cancelar): ")
    if not nome:
        print("Cadastro cancelado.\n")
        return

    cpf = input("CPF (apenas números): ")
    if not validar_numero(cpf):
        return

    telefone = input("Telefone (apenas números): ")
    if not validar_numero(telefone):
        return

    endereco = input("Endereço: ")

    setor_nome = "Nenhum"
    if setores:
        print("\nSetores disponíveis:")
        for idx, setor in enumerate(setores):
            print(f"{idx + 1}. {setor.nome}")

        escolha = input("Escolha o número do setor (ou Enter para 'Nenhum'): ")
        if escolha:
            if not escolha.isdigit():
                print("⚠️ Entrada inválida.\n")
                setor = None
            else:
                idx = int(escolha) - 1
                if 0 <= idx < len(setores):
                    setor = setores[idx]
                    setor_nome = setor.nome
                else:
                    print("Setor inválido.\n")
                    setor = None
        else:
            setor = None
    else:
        print("Nenhum setor cadastrado. Empregado será cadastrado sem setor.\n")
        setor = None

    empregado = Empregado(nome, cpf, telefone, endereco, setor_nome)
    empregados.append(empregado)

    if setor:
        setor.adicionar_empregado(empregado)

    print("Empregado cadastrado com sucesso.\n")


def editar_empregado():
    if not empregados:
        print("Não há empregados cadastrados.\n")
        return

    print("\n--- Lista de Empregados ---")
    for emp in empregados:
        print(f"ID: {emp.id} - Nome: {emp.nome} - Setor: {emp.setor}")

    escolha = input("Digite o ID do empregado para editar (ou Enter para cancelar): ")
    if not escolha:
        print("Edição cancelada.\n")
        return

    if not escolha.isdigit():
        print("ID inválido.\n")
        return

    id_emp = int(escolha)
    empregado = encontrar_empregado_por_id(id_emp)

    if empregado:
        empregado.nome = input(f"Novo nome ({empregado.nome}) (ou Enter para manter): ") or empregado.nome
        empregado.telefone = input(f"Novo telefone ({empregado.telefone}) (ou Enter para manter): ") or empregado.telefone
        empregado.endereco = input(f"Novo endereço ({empregado.endereco}) (ou Enter para manter): ") or empregado.endereco
        print("Dados atualizados com sucesso.\n")
    else:
        print("Empregado não encontrado.\n")


def excluir_empregado():
    if not empregados:
        print("Não há empregados cadastrados.\n")
        return

    print("\n--- Lista de Empregados ---")
    for emp in empregados:
        print(f"ID: {emp.id} - Nome: {emp.nome} - Setor: {emp.setor}")

    escolha = input("Digite o ID do empregado para excluir (ou Enter para cancelar): ")
    if not escolha:
        print("Exclusão cancelada.\n")
        return

    if not escolha.isdigit():
        print("ID inválido.\n")
        return

    id_emp = int(escolha)
    empregado = encontrar_empregado_por_id(id_emp)

    if empregado:
        confirm = input(f"Tem certeza que deseja excluir {empregado.nome}? (s/n): ").lower()
        if confirm == 's':
            if empregado.setor != "Nenhum":
                setor = encontrar_setor_por_nome(empregado.setor)
                if setor:
                    setor.remover_empregado(empregado)

            empregados.remove(empregado)
            print("Empregado excluído com sucesso.\n")
        else:
            print("Exclusão cancelada.\n")
    else:
        print("Empregado não encontrado.\n")


def realocar_empregado():
    if not empregados:
        print("Não há empregados cadastrados.\n")
        return

    if not setores:
        print("Não há setores cadastrados.\n")
        return

    print("\n--- Lista de Empregados ---")
    for idx, emp in enumerate(empregados):
        print(f"{idx + 1}. {emp.nome} (ID: {emp.id}) - Setor atual: {emp.setor}")

    escolha = input("Digite o número do empregado para realocar (ou Enter para cancelar): ")
    if not escolha:
        print("Operação cancelada.\n")
        return

    if not escolha.isdigit():
        print("Entrada inválida.\n")
        return

    idx = int(escolha) - 1
    if not (0 <= idx < len(empregados)):
        print("Empregado inválido.\n")
        return

    empregado = empregados[idx]

    print("\nSetores disponíveis:")
    for i, setor in enumerate(setores):
        print(f"{i + 1}. {setor.nome}")

    escolha_setor = input("Digite o número do novo setor (ou Enter para cancelar): ")

    if not escolha_setor:
        print("Operação cancelada.\n")
        return

    if not escolha_setor.isdigit():
        print("Entrada inválida.\n")
        return

    idx_setor = int(escolha_setor) - 1
    if not (0 <= idx_setor < len(setores)):
        print("Setor inválido.\n")
        return

    novo_setor = setores[idx_setor]

    if empregado.setor != "Nenhum":
        setor_atual = encontrar_setor_por_nome(empregado.setor)
        if setor_atual:
            setor_atual.remover_empregado(empregado)

    empregado.setor = novo_setor.nome
    novo_setor.adicionar_empregado(empregado)

    print("Empregado realocado com sucesso.\n")


def visualizar_setores():
    if not setores:
        print("Não há setores cadastrados.\n")
        return

    for setor in setores:
        print(f"\nSetor: {setor.nome}")
        if setor.equipe:
            print("Equipe:")
            for emp in setor.equipe:
                print(f"- {emp.nome} (CPF: {emp.cpf})")
        else:
            print("Sem empregados nesse setor.")


def visualizar_empregados():
    if not empregados:
        print("Não há empregados cadastrados.\n")
        return

    print("\n--- Lista de Empregados ---")
    for emp in empregados:
        print(f"Nome: {emp.nome}, CPF: {emp.cpf}, Setor: {emp.setor}")


def gerenciar_setores():
    while True:
        print("\n--- Gerenciar Setores ---")
        print("1. Criar setor")
        print("2. Editar setor")
        print("3. Excluir setor")
        print("4. Visualizar setores e equipes")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do novo setor (ou Enter para cancelar): ")
            if not nome:
                print("Criação cancelada.\n")
                continue
            if encontrar_setor_por_nome(nome):
                print("Setor já existe.\n")
            else:
                setores.append(Setor(nome))
                print("Setor criado com sucesso.\n")

        elif opcao == '2':
            if not setores:
                print("Não há setores cadastrados.\n")
                continue

            print("\nSetores disponíveis:")
            for idx, setor in enumerate(setores):
                print(f"{idx + 1}. {setor.nome}")

            escolha = input("Digite o número do setor para editar (ou Enter para cancelar): ")
            if not escolha:
                print("Edição cancelada.\n")
                continue

            if not escolha.isdigit():
                print("Setor inválido.\n")
                continue

            idx = int(escolha) - 1
            if not (0 <= idx < len(setores)):
                print("Setor inválido.\n")
                continue

            setor = setores[idx]

            novo_nome = input(f"Novo nome para o setor ({setor.nome}) (ou Enter para cancelar): ")
            if not novo_nome:
                print("Edição cancelada.\n")
                continue

            if encontrar_setor_por_nome(novo_nome):
                print("Já existe um setor com esse nome.\n")
            else:
                for emp in setor.equipe:
                    emp.setor = novo_nome
                setor.nome = novo_nome
                print("Setor atualizado com sucesso.\n")

        elif opcao == '3':
            if not setores:
                print("Não há setores cadastrados.\n")
                continue

            print("\nSetores disponíveis:")
            for idx, setor in enumerate(setores):
                print(f"{idx + 1}. {setor.nome}")

            escolha = input("Digite o número do setor para excluir (ou Enter para cancelar): ")
            if not escolha:
                print("Exclusão cancelada.\n")
                continue

            if not escolha.isdigit():
                print("Setor inválido.\n")
                continue

            idx = int(escolha) - 1
            if not (0 <= idx < len(setores)):
                print("Setor inválido.\n")
                continue

            setor = setores[idx]

            confirm = input(f"Tem certeza que deseja excluir o setor '{setor.nome}'? (s/n): ").lower()
            if confirm == 's':
                for emp in setor.equipe:
                    emp.setor = "Nenhum"
                setores.remove(setor)
                print("Setor excluído com sucesso.\n")
            else:
                print("Exclusão cancelada.\n")

        elif opcao == '4':
            visualizar_setores()

        elif opcao == '5':
            print("Voltando ao menu principal...\n")
            break

        else:
            print("Opção inválida.\n")


# Funções auxiliares
def encontrar_empregado_por_id(id_emp):
    for emp in empregados:
        if emp.id == id_emp:
            return emp
    return None


def encontrar_setor_por_nome(nome):
    for setor in setores:
        if setor.nome == nome:
            return setor
    return None


# Programa Principal
def main():
    print("\n===== Sistema de Gestão de Empresa (Modo Terminal) =====")
    print("Login como administrador padrão.\n")

    while True:
        print("\n--- Menu Principal ---")
        print("1. Cadastrar empregado")
        print("2. Editar empregado")
        print("3. Excluir empregado")
        print("4. Gerenciar setores")
        print("5. Realocar empregado")
        print("6. Visualizar setores e equipes")
        print("7. Visualizar empregados")
        print("8. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_empregado()
        elif opcao == '2':
            editar_empregado()
        elif opcao == '3':
            excluir_empregado()
        elif opcao == '4':
            gerenciar_setores()
        elif opcao == '5':
            realocar_empregado()
        elif opcao == '6':
            visualizar_setores()
        elif opcao == '7':
            visualizar_empregados()
        elif opcao == '8':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    main()
