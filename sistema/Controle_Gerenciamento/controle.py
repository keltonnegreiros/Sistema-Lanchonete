import mysql.connector as mysql_connector
import os

banco = mysql_connector.connect(
    host="localhost",
    user="root",
    passwd="Vieira_maria22",
    database="lanchonete"
)

# Atributos públicos


# Sistema começa aqui
def funcao_principal():
    print(f"Entrando no sistema da Lanchonete")

    while (True):
        # MENU
        print("------------Menu------------")  
        print("[1] - Cadastrar Cliente")
        print("[2] - Cadastrar Funcionário")  
        print("[3] - Fazer Login")
        print("[4] - Sair")
        opcao = int(input("Digite a opção desejada: "))

        if opcao == 1:
            nome = str(input("Digite seu nome: "))
            cpf = str(input("Digite seu CPF: "))
            telefone = str(input("Digite seu número (formato: (XX) XXXXX-XXXX): "))

            cursor = banco.cursor()
            comando_SQL = "INSERT INTO cliente (telefone, cpf, nome) VALUES (%s, %s, %s)"
            dados = (str(telefone), str(cpf), str(nome))
            cursor.execute(comando_SQL, dados)
            banco.commit()
            os.system('cls')



funcao_principal()