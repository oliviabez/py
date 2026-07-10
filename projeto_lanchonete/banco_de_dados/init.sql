-- =========================================================
-- Sistema de Lanchonete - Schema final
-- Implementa as Histórias de Usuário 01 a 14
-- =========================================================

CREATE DATABASE IF NOT EXISTS lanchonete_db;
USE lanchonete_db;

DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS atendentes;
DROP TABLE IF EXISTS administradores;

-- =========================================================
-- HU01 / HU02 / HU03 - Cliente (cadastro, login, listagem, exclusão)
-- =========================================================
CREATE TABLE clientes (
    id_cliente      INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    email           VARCHAR(100) NOT NULL UNIQUE,
    senha           VARCHAR(255) NOT NULL,
    codigo_cliente  VARCHAR(20)  NOT NULL UNIQUE,
    data_cadastro   DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- HU12 - Atendente (cadastro e login)
-- =========================================================
CREATE TABLE atendentes (
    id_atendente    INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    usuario         VARCHAR(50)  NOT NULL UNIQUE,
    senha           VARCHAR(255) NOT NULL,
    data_cadastro   DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- HU13 - Administrador (cadastro e login)
-- =========================================================
CREATE TABLE administradores (
    id_administrador INT AUTO_INCREMENT PRIMARY KEY,
    nome             VARCHAR(100) NOT NULL,
    usuario          VARCHAR(50)  NOT NULL UNIQUE,
    senha            VARCHAR(255) NOT NULL,
    data_cadastro    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- HU04 / HU05 / HU06 / HU07 - Produto (cardápio)
-- =========================================================
CREATE TABLE produtos (
    id_produto      INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    descricao       VARCHAR(255),
    categoria       VARCHAR(50),
    tipo            VARCHAR(50),
    tamanho         VARCHAR(20),
    preco           DECIMAL(10,2) NOT NULL,
    estoque         INT DEFAULT 0,
    ativo           BOOLEAN DEFAULT TRUE,

    CONSTRAINT chk_produto_preco CHECK (preco > 0)
);

-- =========================================================
-- HU08 / HU09 / HU10 / HU11 / HU14 - Pedido
-- numero_pedido: 3 dígitos, reinicia todos os dias
-- =========================================================
CREATE TABLE pedidos (
    id_pedido       INT AUTO_INCREMENT PRIMARY KEY,
    numero_pedido   VARCHAR(3)   NOT NULL,
    id_cliente      INT NOT NULL,
    data_pedido     DATETIME DEFAULT CURRENT_TIMESTAMP,
    forma_pagamento VARCHAR(30)  NOT NULL,
    status_pedido   VARCHAR(30)  NOT NULL DEFAULT 'Pedido recebido com sucesso',
    valor_total     DECIMAL(10,2) DEFAULT 0,

    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);

CREATE TABLE itens_pedido (
    id_item         INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido       INT NOT NULL,
    id_produto      INT NOT NULL,
    quantidade      INT NOT NULL,
    tamanho         VARCHAR(20),
    preco_unitario  DECIMAL(10,2) NOT NULL,
    subtotal        DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_item_pedido
        FOREIGN KEY (id_pedido)
        REFERENCES pedidos(id_pedido),

    CONSTRAINT fk_item_produto
        FOREIGN KEY (id_produto)
        REFERENCES produtos(id_produto)
);

-- =========================================================
-- Dados iniciais para teste
-- =========================================================
INSERT INTO administradores (nome, usuario, senha)
VALUES ('Admin Geral', 'admin', 'admin123');

INSERT INTO atendentes (nome, usuario, senha)
VALUES ('Atendente Padrão', 'atendente', 'atendente123');


INSERT INTO produtos (nome, descricao, categoria, tipo, tamanho, preco, estoque)
VALUES ('Bk chicken','sanduíche','Hamburguer','lanche','Médio','15.60','23')
