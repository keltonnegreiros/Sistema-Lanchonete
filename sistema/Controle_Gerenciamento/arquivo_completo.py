from pathlib import Path
import mysql.connector
from PyQt5 import uic, QtWidgets

numero_id = 0

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Vieira_maria22",
    database="lanchonete"
)

# Funcionários -------------------------------------------------------------------------------------------------------
def gerenciarFunc():
    telaPrincipal.close()
    telaFunc.show()

    telaFunc.bt_voltar.clicked.connect(lambda: [telaFunc.close(), telaPrincipal.show()])


def cadastrarFunc():
    telaFunc.close()
    telaFunc_cadastro.show()


def confirmarCadastro_func():
    nome = telaFunc_cadastro.txt_nomeCadastroFunc.text()
    cpf = telaFunc_cadastro.txt_cpfCadastroFunc.text()
    salario = telaFunc_cadastro.txt_salarioCadastroFunc.text()
    funcao = telaFunc_cadastro.txt_funcaoCadastroFunc.text()

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO funcionario (salario, cpf, nome, funcao) VALUES (%s, %s, %s, %s)"
    dados = (float(salario), str(cpf), str(nome), str(funcao))
    cursor.execute(comando_SQL, dados)
    banco.commit()
    telaFunc_cadastro.close()
    telaFunc.show()


def buscarFunc():
    id = telaFunc.txt_buscarFunc.text()

    cursor = banco.cursor()
    comando_SQL = "SELECT * from funcionario WHERE idFunc = %s"
    dado = (int(id),)
    cursor.execute(comando_SQL, dado)
    busca = cursor.fetchall()

    telaFunc.tabela_funcionarios.setRowCount(len(busca))
    telaFunc.tabela_funcionarios.setColumnCount(4)

    for i in range(0, len(busca)):
         for j in range(0, 4):
            telaFunc.tabela_funcionarios.setItem(i, j, QtWidgets.QTableWidgetItem(str(busca[i][j])))


def listarFuncionarios():
    cursor = banco.cursor()
    comando_SQL = "SELECT * from funcionario"
    cursor.execute(comando_SQL)
    busca = cursor.fetchall()

    telaFunc.tabela_funcionarios.setRowCount(len(busca))
    telaFunc.tabela_funcionarios.setColumnCount(5)

    for i in range(0, len(busca)):
         for j in range(0, 5):
            telaFunc.tabela_funcionarios.setItem(i, j, QtWidgets.QTableWidgetItem(str(busca[i][j])))


def atualizarFunc():
    global numero_id
    linha = telaFunc.tabela_funcionarios.currentRow()

    cursor = banco.cursor()
    comando_SQL = "SELECT idFunc FROM funcionario"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    comando_SQL = "SELECT * FROM funcionario WHERE idFunc = %s"
    dado = (int(valor_id),)
    cursor.execute(comando_SQL, dado)
    func = cursor.fetchall()
    telaFunc_atualizar.show()

    numero_id = valor_id

    telaFunc_atualizar.txt_nomeAtualizarFunc.setText(str(func[0][3]))
    telaFunc_atualizar.txt_salarioAtualizarFunc.setText(str(func[0][1]))
    telaFunc_atualizar.txt_funcaoAtualizarFunc.setText(str(func[0][4]))

def salvarFuncionario():
    # pega o numero do id
    global numero_id
    nome = telaFunc_atualizar.txt_nomeAtualizarFunc.text()
    salario = telaFunc_atualizar.txt_salarioAtualizarFunc.text()
    funcao = telaFunc_atualizar.txt_funcaoAtualizarFunc.text()

    cursor = banco.cursor()
    comando_SQL = "UPDATE funcionario SET nome = %s, salario = %s, funcao = %s WHERE idFunc = %s"
    dados_lidos = (str(nome), float(salario), str(funcao), int(numero_id))
    cursor.execute(comando_SQL, dados_lidos)
    banco.commit()

    # atualizar as janelas
    telaFunc_atualizar.close()
    telaFunc.close()
    atualizarTabelaFunc()


def removerFuncionario():
    linha = telaFunc.tabela_funcionarios.currentRow()
    telaFunc.tabela_funcionarios.removeRow(linha)

    cursor = banco.cursor()
    comando_SQL = "SELECT idFunc FROM funcionario"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    comando_SQL = "DELETE FROM funcionario WHERE idFunc = %s"
    dado = (int(valor_id),)
    cursor.execute(comando_SQL, dado)
    banco.commit()


def atualizarTabelaFunc():
    telaFunc.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM funcionario"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    telaFunc.tabela_funcionarios.setRowCount(len(dados_lidos))
    telaFunc.tabela_funcionarios.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
         for j in range(0, 5):
            telaFunc.tabela_funcionarios.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


# Pedidos -------------------------------------------------------------------------------------------------------
# EU VOU FAZER ISSO



# Mesas -------------------------------------------------------------------------------------------------------
def gerenciarMesas():
    telaPrincipal.close()
    telaMesas.show()

    telaMesas.bt_voltar.clicked.connect(lambda: [telaMesas.close(), telaPrincipal.show()])


def cadastrarMesa():
    telaMesas.close()
    telaMesas_cadastrar.show()


def confirmarCadastro_mesa():
    numero = telaMesas_cadastrar.txt_numeroCadastrarMesa.text()
    # se JÁ EXISTER O NUMERO, NÃO CADASTRAR
    capacidade  = telaMesas_cadastrar.txt_qtdCadastrarMesa.text()
    status = "Disponível"

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO mesa (status, numero, capacidade) VALUES (%s, %s, %s)"
    dados_lidos = (str(status), int(numero), int(capacidade))
    cursor.execute(comando_SQL, dados_lidos)
    banco.commit()

    telaMesas_cadastrar.close()
    atualizarTabelaMesas()
    telaMesas.show()


def removerMesa():
    linha = telaMesas.tabela_mesas.currentRow()
    telaMesas.tabela_mesas.removeRow(linha)

    cursor = banco.cursor()
    comando_SQL = "SELECT idMesa FROM mesa"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    comando_SQL = "DELETE from mesa WHERE idMesa = %s"
    dado = (int(valor_id),)
    cursor.execute(comando_SQL, dado)
    banco.commit()


def listarMesas():
    # Serve para mostrar TODAS as mesas cadastradas no sistema
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM mesa"
    cursor.execute(comando_SQL)
    exibir_mesas = cursor.fetchall()

    telaMesas.tabela_mesas.setRowCount(len(exibir_mesas))
    telaMesas.tabela_mesas.setColumnCount(4)

    for i in range(0, len(exibir_mesas)):
         for j in range(0, 4):
            telaMesas.tabela_mesas.setItem(i, j, QtWidgets.QTableWidgetItem(str(exibir_mesas[i][j])))


def atualizarTabelaMesas():
    telaMesas.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM mesa"
    cursor.execute(comando_SQL)
    exibir_mesas = cursor.fetchall()

    telaMesas.tabela_mesas.setRowCount(len(exibir_mesas))
    telaMesas.tabela_mesas.setColumnCount(4)

    for i in range(0, len(exibir_mesas)):
         for j in range(0, 4):
            telaMesas.tabela_mesas.setItem(i, j, QtWidgets.QTableWidgetItem(str(exibir_mesas[i][j])))


# COMIDAS  -------------------------------------------------------------------------------------------------------
# lica tu vau fazer essa parte aquirrr!!!!





# faz com que o sistema funcione
app = QtWidgets.QApplication([])

# TODAS as telas que forem criadas tem que fazer isso ai
# Tela principal
ui_path1 = Path(__file__).with_name("telaPrincipal.ui")
telaPrincipal = uic.loadUi(str(ui_path1))

# botões da tela principal
telaPrincipal.bt_gerFunc.clicked.connect(gerenciarFunc)
telaPrincipal.bt_gerFunc.clicked.connect(listarFuncionarios) # esse aqui é pra quando o usuário clicar no botão Gerenciar Funcionário, a tabela carregar
telaPrincipal.bt_gerMesas.clicked.connect(gerenciarMesas)
telaPrincipal.bt_gerMesas.clicked.connect(listarMesas)

# Tela funcionário
ui_path2 = Path(__file__).with_name("telaFuncionarios.ui")
telaFunc = uic.loadUi(str(ui_path2))

# botoões da tela funcionário
telaFunc.bt_cadastrarFunc.clicked.connect(cadastrarFunc)
telaFunc.bt_buscarFunc.clicked.connect(buscarFunc)
telaFunc.bt_atualizarFunc.clicked.connect(atualizarFunc)
telaFunc.bt_excluirFunc.clicked.connect(removerFuncionario)

# Tela funcionário_cadastro
ui_path3 = Path(__file__).with_name("telaFuncionarios_cadastro.ui")
telaFunc_cadastro = uic.loadUi(str(ui_path3))

# botão da tela funcionário_cadastro
telaFunc_cadastro.bt_confirmarCadastroFun.clicked.connect(confirmarCadastro_func)

# Tela funcionário_atualizar
ui_path4 = Path(__file__).with_name("telaFuncionarios_atualizar.ui")
telaFunc_atualizar = uic.loadUi(str(ui_path4))

# botão da tela funcionário_atualizar
telaFunc_atualizar.bt_confirmarAtualizarFun.clicked.connect(salvarFuncionario)

# Tela mesas 
ui_path10 = Path(__file__).with_name("telaMesas.ui")
telaMesas = uic.loadUi(str(ui_path10))

# botão da tela Mesas
telaMesas.bt_cadastrarMesa.clicked.connect(cadastrarMesa)
telaMesas.bt_removerMesa.clicked.connect(removerMesa)

# Tela mesas_cadastrar
ui_path11 = Path(__file__).with_name("telaMesas_cadastrar.ui")
telaMesas_cadastrar = uic.loadUi(str(ui_path11))

# botão tela mesa_cadastrar
telaMesas_cadastrar.bt_confirmarCadastro_mesa.clicked.connect(confirmarCadastro_mesa)


# aqui é pra mostrar a TELA PRINCIPAL DO SISTEMA e executar o SISTEMA
telaPrincipal.show()
app.exec()


