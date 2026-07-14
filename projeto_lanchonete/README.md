# Sistema de Lanchonete — Versão Final

Implementação das Histórias de Usuário 01 a 14 (cadastro/login de cliente,
atendente e administrador, CRUD de produtos, e pedidos com regras de
negócio).

## Estrutura

```
banco_de_dados/
    schema.sql          -> script completo do banco (rode este primeiro)

src/
    dominio/            -> classes de dados (Cliente, Produto, Pedido, ...)
    dados/              -> repositories (acesso ao MySQL)
    negocio/            -> services (regras de negócio das histórias)
    apresentacao/
        main.py         -> menu do sistema (ponto de entrada)
```

## Como executar

1. Crie o banco rodando o script:
   `banco_de_dados/schema.sql` (ajuste usuário/senha do MySQL conforme
   necessário em `src/dados/conexao_singleton.py`).

2. Instale as dependências:
   `pip install -r requirements.txt`

3. Execute o sistema:
   `python src/apresentacao/main.py`

## Usuários de teste (criados pelo schema.sql)

- Administrador: usuário `admin`, senha `admin123`
- Atendente: usuário `atendente`, senha `atendente123`


## Histórias de usuário implementadas

| HU | Funcionalidade | Onde está |
|----|-----------------|-----------|
| 01 | Cadastro/login de cliente, permissões sobre os próprios dados | `cliente_service.py`, `autenticacao_service.py` |
| 02 | Listagem de clientes (atendente/admin) | `cliente_service.listar_clientes` |
| 03 | Exclusão de cliente (admin) | `cliente_service.remover_cliente` |
| 04 | Cadastro de produto (admin) | `produto_service.cadastrar_produto` |
| 05 | Listagem do cardápio por categoria | `produto_service.listar_produtos` |
| 06 | Atualização de produto (admin) | `produto_service.atualizar_produto` |
| 07 | Exclusão de produto (admin) | `produto_service.remover_produto` |
| 08 | Registro de pedido (nº de 3 dígitos diário, limite de 3 pedidos/dia, forma de pagamento sem parcelamento, cálculo automático do total) | `pedido_service.criar_pedido` |
| 09 | Consulta de pedidos por e-mail ou número | `pedido_service.consultar_pedidos` |
| 10 | Atualização de pedido (mesmo dia, até 20 min) | `pedido_service.atualizar_pedido` |
| 11 | Cancelamento de pedido (cliente: 20 min / admin: após 1h sem retirada) | `pedido_service.cancelar_pedido` |
| 12 | Cadastro/login de atendente | `autenticacao_service.py` |
| 13 | Cadastro/login de administrador | `autenticacao_service.py` |
| 14 | Atualização de status do pedido (atendente/admin) | `pedido_service.atualizar_status` |

## Observações

- As senhas são armazenadas em texto puro apenas para fins didáticos;
  em um projeto real devem ser armazenadas com hash (ex.: bcrypt).
- O controle de papéis (cliente/atendente/administrador) é feito via
  sessão retornada pelo `AutenticacaoService`, repassada aos demais
  services para validar permissões em cada operação.
