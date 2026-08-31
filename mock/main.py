import uuid 
id = uuid.uuid4()

todo_db = {}
task_id = 1

while True:
    tarefa = input("Adicione uma tarefa: ")
    status = input("Adicione um status: ")
    prioridade = input("Adicione uma prioridade: ")
    criado_em = input("Adicione a data de criação (aaaa-mm-dd): ")

    # Adiciona a nova tarefa no dicionário usando o task_id como chave
    todo_db[task_id] = {
        "tarefa": tarefa,
        "status": status,
        "prioridade": prioridade,
        "criado_em": criado_em
    }
    
    task_id += 1 # Prepara o ID para a próxima tarefa
    
    op = input("Continuar? S/N: ")
    if op.lower() == 'n':
        import pprint
        print("\nResultado do todo_db:")
        pprint.pprint(todo_db, width=80)
        break
