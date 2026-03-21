create table EMPRESA(
	id_empresa BIGINT AUTO_INCREMENT PRIMARY KEY,
	nome VARCHAR(40) NOT NULL
)

create table SETOR(
	id_setor BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome_setor VARCHAR(30) UNIQUE NOT NULL
)

create table MOTORISTA(
	id_motorista BIGINT AUTO_INCREMENT PRIMARY KEY,
	cpf BIGINT NOT NULL,
    nome_motorista VARCHAR(50) NOT NULL,
    id_empresa BIGINT,
    id_setor BIGINT,
    CONSTRAINT id_empresa FOREIGN KEY (id_empresa) REFERENCES EMPRESA (id_empresa),
    CONSTRAINT id_setor FOREIGN KEY (id_setor) REFERENCES SETOR (id_setor)
)


create table VEICULO(
	id_veiculo BIGINT AUTO_INCREMENT PRIMARY KEY,
	placa_veiculo VARCHAR(10)  NOT NULL,
    placa_carreta VARCHAR(10) NOT NULL    
)

create table NF(
	id_nf BIGINT PRIMARY KEY AUTO_INCREMENT,
    num_nf INT NOT NULL,
    id_empresa BIGINT,
    CONSTRAINT fk_id_empresa FOREIGN KEY (id_empresa) REFERENCES EMPRESA (id_empresa)
)

create table VEICULO_MOTORISTA(
	id_veiculo BIGINT PRIMARY KEY,
    id_motorista BIGINT,
    id_nf BIGINT,
	CONSTRAINT fk_id_veiculo FOREIGN KEY (id_veiculo) REFERENCES VEICULO(id_veiculo),
    CONSTRAINT fk_id_motorista FOREIGN KEY (id_motorista) REFERENCES MOTORISTA(id_motorista),
    CONSTRAINT fk_id_nf FOREIGN KEY (id_nf) REFERENCES NF(id_nf)
)
	
create table TRANSPORTADORA(
	id_transportadora BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome_transportadora VARCHAR(30) NOT NULL
)

create table EMBALAGEM(
	id_emb BIGINT AUTO_INCREMENT PRIMARY KEY,
    qtd_emb BIGINT NOT NULL
)


create table AGENTE(
	id_agente BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome_agente VARCHAR(50) NOT NULL
)

create table ES(
	id_es BIGINT AUTO_INCREMENT PRIMARY KEY,
	entrada DATETIME NOT NULL,
	saida DATETIME,    
    id_veiculo BIGINT,
    id_empresa BIGINT,
    id_emb BIGINT,
    id_agente BIGINT,
    id_motorista BIGINT,
    id_nf BIGINT,
    id_transportadora BIGINT,
    id_setor BIGINT,
    CONSTRAINT fk_id_veiculo_es FOREIGN KEY (id_veiculo) REFERENCES VEICULO(id_veiculo),
    CONSTRAINT fk_id_empresa_es FOREIGN KEY (id_empresa) REFERENCES EMPRESA (id_empresa),
    CONSTRAINT fk_id_emb_es FOREIGN KEY (id_emb) REFERENCES EMBALAGEM (id_emb),
    CONSTRAINT fk_id_agente_es FOREIGN KEY (id_agente) REFERENCES AGENTE (id_agente),
    CONSTRAINT fk_id_motorista_es FOREIGN KEY (id_motorista) REFERENCES MOTORISTA (id_motorista),
    CONSTRAINT fk_id_nf_es FOREIGN KEY (id_nf) REFERENCES NF (id_nf),
    CONSTRAINT fk_id_transportadora_es FOREIGN KEY (id_transportadora) REFERENCES TRANSPORTADORA (id_transportadora),
    CONSTRAINT fk_id_setor_es FOREIGN KEY (id_setor) REFERENCES SETOR (id_setor)
)

INSERT INTO setor (nome_setor) VALUES ('EXPEDIÇÃO')
INSERT INTO setor (nome_setor) VALUES ('MATÉRIA-PRIMA')
INSERT INTO setor (nome_setor) VALUES ('ALMOXARIFADO')
INSERT INTO setor (nome_setor) VALUES ('GESCRAP')
INSERT INTO setor (nome_setor) VALUES ('SAÍDA NF')


