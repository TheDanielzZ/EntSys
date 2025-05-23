import pymysql
from datetime import datetime
import pandas as pd


conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='1234!Daniel',
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
   

    print("Dados a inserir:")
    print("Entrada:", entrada)
    print("id_veiculo:", id_veiculo)
    print("id_motorista:", id_motorista)
    print("id_empresa:", id_empresa)
    print("id_setor:", id_setor)
    print("id_agente:", id_agente)
    print("id_nf:", id_nf)
    print("id_transportadora:", id_transportadora)


    cursor.execute('''
        INSERT INTO ES (entrada, id_veiculo, id_motorista, id_nf, id_setor, id_transportadora, id_empresa, id_agente)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (entrada, id_veiculo, id_motorista, id_nf, id_setor, id_transportadora, id_empresa, id_agente))

    conn.commit()

def buscar_setores():
    cursor.execute("SELECT nome_setor FROM SETOR")
    resultado = cursor.fetchall()
    return [linha[0].strip() for linha in resultado]

def registrar_saida(placa_veiculo, placa_carreta):
    saida = datetime.now()
    cursor.execute('''
        SELECT id_es FROM ES
        WHERE id_veiculo = (SELECT id_veiculo FROM VEICULO WHERE placa_veiculo = %s AND placa_carreta = %s)
        AND saida IS NULL
    ''', (placa_veiculo, placa_carreta))
    
    result = cursor.fetchone()
    if not result:
        raise ValueError("Caminhão não encontrado com entrada pendente.")
    
    cursor.execute('''
        UPDATE ES SET saida = %s 
        WHERE id_es = %s
    ''', (saida, result[0]))
    conn.commit()

def exportar_excel(caminho='C:/Documentos/movimentacao.xlsx'):
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

    # Pega os nomes das colunas automaticamente
    colunas = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(rows, columns=colunas)
    df.to_excel(caminho, index=False)

def fechar_conexao():
    cursor.close()
    conn.close()

def sair_app():
    fechar_conexao()
    
