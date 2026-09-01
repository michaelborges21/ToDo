# import os
import uuid
import subprocess

# Dicionário para armazenar as tarefas em memória (ID -> Tarefa)
tarefas = {}

def add_task():
    descricao = input("\nDigite a descrição da tarefa: ").strip()
    if descricao:
        task_id = str(uuid.uuid4())
        nova_tarefa = {
            "descricao": descricao,
            "concluida": False
        }
        tarefas[task_id] = nova_tarefa

        print("✅ Tarefa adicionada com sucesso!\n")
    else:
        print("❌ A descrição não pode ser vazia.\n")

def complet_toggle_task():
    list_all_task()
    if not tarefas:
        return

    try:
        escolha = int(input("\nDigite o número da tarefa para alternar (ou 0 para cancelar): ").strip())
        if escolha == 0:
            print("Ação cancelada.\n")
            return
            
        indice = escolha - 1
        # Verifica se o índice digitado é válido e está dentro da quantidade de tarefas
        if 0 <= indice < len(tarefas):

            # Por que usar list(tarefas.keys())?
            # 'tarefas' é um dicionário e .keys() não permite acessar um item pela sua posição numérica.
            # Por isso foi convertido  para list(), permitindo buscar a chave exata através do '[indice]'.
            
            task_id = list(tarefas.keys())[indice]
            
            # Acessa os dados da tarefa no dicionário usando o id encontrado
            tarefa = tarefas[task_id]
            
            # Inverte o estado de conclusão (se estava pendente, conclui; se concluída, deixa pendente)
            tarefa["concluida"] = not tarefa["concluida"]
            
            # Define qual será a palavra exibida com base no novo estado
            if tarefa["concluida"]:
                status = "concluída"
            else:
                status = "pendente"
                
            print(f"🔄 Tarefa atualizada para: {status}!\n")
        else:
            print("❌ Número de tarefa inválido.\n")
    except ValueError:
        print("❌ Por favor, digite um número válido.\n")

def remove_task():
    list_all_task()
    if not tarefas:
        return

    try:
        escolha = int(input("\nDigite o número da tarefa para remover (ou 0 para cancelar): ").strip())
        if escolha == 0:
            print("Ação cancelada.\n")
            return
            
        indice = escolha - 1
        if 0 <= indice < len(tarefas):
            task_id = list(tarefas.keys())[indice]
            tarefa_removida = tarefas.pop(task_id)
            print(f"🗑️  Tarefa '{tarefa_removida['descricao']}' removida com sucesso!\n")
        else:
            print("❌ Número de tarefa inválido.\n")
    except ValueError:
        print("❌ Por favor, digite um número válido.\n")

def list_all_task():
    print("\n--- Suas Tarefas ---")
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
    else:
        for indice, (task_id, tarefa) in enumerate(tarefas.items(), start=1):
            if tarefa["concluida"]:
                status = "[X]"
            else:
                status = "[ ]"
            print(f"{indice}. {status} {tarefa['descricao']}")
    print("-" * 20)


def menu():
    while True:
        print("\n" + "=" * 40)
        print(" " * 12 + "TO-DO LIST")
        print("=" * 40)
        print(" 1. Adicionar Nova Tarefa")
        print(" 2. Concluir/Alternar Tarefa")
        print(" 3. Remover Tarefa")
        print(" 4. Listar Tarefas")
        print(" 0. Sair do Aplicativo")
        print("=" * 40)

        opcao = input(" Escolha uma opção (0-4): ").strip()

        match opcao:
            case "1":
                add_task()
                subprocess.run(["clear"])
            case "2":
                complet_toggle_task()
                subprocess.run(["clear"])
            case "3":
                remove_task()
                subprocess.run(["clear"])
            case "4":
                list_all_task()
                subprocess.run(["clear"])
            case "0":
                print("Saindo do aplicativo. Até mais!")
                break
            case _:
                print("❌ Comando inválido. Tente novamente.\n")

def main() -> None:
    menu()

if __name__ == "__main__":
    main()
