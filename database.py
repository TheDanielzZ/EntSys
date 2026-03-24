import pymysql
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import filedialog # NOVO: Necessário para a janelinha de Salvar Como

# Conexão com o banco de dados
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='entsys',
    port=3306
)

cursor = conn.cursor()

def buscar_ou_criar(query_select, query_insert, valores_select, valores_insert):
    cursor.execute(query_select, valores_select)
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute(query_insert, valores_insert)
    conn.commit()
    return cursor.lastrowid

def registrar_entrada(placa_veiculo, placa_carreta, motorista, cpf, nota_fiscal, setor, transportadora, empresa, agente):
    entrada = datetime.now()

    id_veiculo = buscar_ou_criar(
        "SELECT id_veiculo FROM VEICULO WHERE placa_veiculo = %s AND placa_carreta = %s",
        "INSERT INTO VEICULO (placa_veiculo, placa_carreta) VALUES (%s, %s)",
        (placa_veiculo, placa_carreta),
        (placa_veiculo, placa_carreta)
    )

    id_motorista = buscar_ou_criar(
        "SELECT id_motorista FROM MOTORISTA WHERE nome_motorista = %s",
        "INSERT INTO MOTORISTA (nome_motorista, cpf) VALUES (%s, %s)",
        (motorista,),
        (motorista, cpf)
    )

    id_nf = buscar_ou_criar(
        "SELECT id_nf FROM NF WHERE num_nf = %s",
        "INSERT INTO NF (num_nf) VALUES (%s)",
        (nota_fiscal,),
        (nota_fiscal,)
    )

    id_setor = buscar_ou_criar(
        "SELECT id_setor FROM SETOR WHERE nome_setor = %s",
        "INSERT INTO SETOR (nome_setor) VALUES (%s)",
        (setor,),
        (setor,)
    )

    id_transportadora = buscar_ou_criar(
        "SELECT id_transportadora FROM TRANSPORTADORA WHERE nome_transportadora = %s",
        "INSERT INTO TRANSPORTADORA (nome_transportadora) VALUES (%s)",
        (transportadora,),
        (transportadora,)
    )

    id_empresa = buscar_ou_criar(
        "SELECT id_empresa FROM EMPRESA WHERE nome = %s",
        "INSERT INTO EMPRESA (nome) VALUES (%s)",
        (empresa,),
        (empresa,)
    )
    
    id_agente = buscar_ou_criar(
        "SELECT id_agente FROM AGENTE WHERE nome_agente = %s",
        "INSERT INTO AGENTE (nome_agente) VALUES (%s)",
        (agente,),
        (agente,)
    )

    cursor.execute('''
        INSERT INTO ES (entrada, id_veiculo, id_motorista, id_nf, id_setor, id_transportadora, id_empresa, id_agente)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (entrada, id_veiculo, id_motorista, id_nf, id_setor, id_transportadora, id_empresa, id_agente))

    conn.commit()

def buscar_setores():
    cursor.execute("SELECT nome_setor FROM SETOR")
    resultado = cursor.fetchall()
    return [linha[0].strip() for linha in resultado]

# --- NOVAS FUNÇÕES DA INTERFACE ---

def buscar_veiculos_pendentes():
    cursor.execute('''
        SELECT v.placa_veiculo 
        FROM ES es
        JOIN VEICULO v ON es.id_veiculo = v.id_veiculo
        WHERE es.saida IS NULL
    ''')
    resultado = cursor.fetchall()
    return [linha[0].strip() for linha in resultado]

def buscar_carreta_por_veiculo(placa_veiculo):
    cursor.execute('''
        SELECT placa_carreta 
        FROM VEICULO 
        WHERE placa_veiculo = %s 
        LIMIT 1
    ''', (placa_veiculo,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    return ""

def registrar_saida(placa_veiculo, placa_carreta): # Ignora a carreta na consulta para evitar o erro de saída
    saida = datetime.now()
    
    cursor.execute('''
        SELECT es.id_es
        FROM ES es
        JOIN VEICULO v ON es.id_veiculo = v.id_veiculo
        WHERE v.placa_veiculo = %s
        AND es.saida IS NULL
    ''', (placa_veiculo,))

    result = cursor.fetchone()
    
    if not result:
        raise ValueError("Caminhão não encontrado com entrada pendente.")

    cursor.execute('''
        UPDATE ES SET saida = %s 
        WHERE id_es = %s
    ''', (saida, result[0]))
    conn.commit()

# --- MELHORIA: EXPORTAR COM JANELA DE SALVAR ---

def exportar_excel():
    # Cria a janelinha perguntando onde o usuário quer salvar
    root = tk.Tk()
    root.withdraw() # Esconde a tela principal vazia do Tkinter
    
    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os Arquivos", "*.*")],
        title="Salvar Relatório de Caminhões",
        initialfile="relatorio_movimentacao.xlsx"
    )
    
    # Se o usuário clicar em "Cancelar" na janela, o caminho fica vazio e interrompemos
    if not caminho_arquivo:
        return False 

    query = '''
    SELECT 
        es.id_es AS ID,
        es.entrada AS Entrada,
        es.saida AS Saída,
        v.placa_veiculo AS Veículo,
        v.placa_carreta AS Carreta,
        m.nome_motorista AS Motorista,
        m.cpf AS CPF,
        nf.num_nf AS NotaFiscal,
        s.nome_setor AS Setor,
        t.nome_transportadora AS Transportadora,
        e.nome AS Empresa,
        a.nome_agente AS Agente
    FROM ES es
    JOIN VEICULO v ON es.id_veiculo = v.id_veiculo
    JOIN MOTORISTA m ON es.id_motorista = m.id_motorista
    JOIN NF nf ON es.id_nf = nf.id_nf
    JOIN SETOR s ON es.id_setor = s.id_setor
    JOIN TRANSPORTADORA t ON es.id_transportadora = t.id_transportadora
    JOIN EMPRESA e ON es.id_empresa = e.id_empresa
    JOIN AGENTE a ON es.id_agente = a.id_agente
    ORDER BY es.entrada DESC
    '''
    
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        raise ValueError("Não há dados para exportar.")

    colunas = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(rows, columns=colunas)
    df.to_excel(caminho_arquivo, index=False)
    
    return True # Retorna True para avisar a GUI que deu certo

def fechar_conexao():
    cursor.close()
    conn.close()