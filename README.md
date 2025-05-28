# Expense tracker

## Descrição
Um sistema de gerenciamento financeiro pessoal, desenvolvido com princípios de Programação Orientada a Objetos (POO). Permite registrar receitas e despesas, categorizá-las e gerar relatórios.

## Estrutura do Projeto
- **Sistema**: Gerencia as operações principais (adicionar transações, gerar relatórios, etc.).
- **Transação** (classe abstrata): Representa uma operação financeira.
  - **Receita**: Representa entradas de dinheiro.
  - **Despesa**: Representa saídas de dinheiro (possui controle de parcelamento).
- **Carteira**: Agrupa formas de pagamento e calcula o saldo total.
- **FormaDePagamento** (classe abstrata): Representa um método de pagamento.
  - **Débito**: Gerencia saldo bancário.
  - **Crédito**: Gerencia limite de crédito, dia de fechamento e vencimento de fatura.
- **Gráfico**: Gera visualizações financeiras por mês e por categoria.
- **Banco de Dados**: Persistência de dados de transações e formas de pagamento.

## Tecnologias Utilizadas
- Linguagem: Python 3.11
- Banco de Dados: SQLite
- Bibliotecas principais:
  - Tkinter (Interface Gráfica)
  - matplotlib (Geração de gráficos)
  - sqlite3 (Persistência de dados)

## Como Executar
```bash
# Clone o repositório
git clone https://github.com/bbiancalopess/expense-tracker

# Acesse a pasta do projeto
cd expense-tracker

# Execute o programa
python3 main.py
```

## Funcionalidades
- [ ] Cadastro de transações ( Receitas ou Despesas )
- [ ] Parcelamento automático de despesas
- [ ] Atualização automática de saldo
- [ ] Visualização de saldo geral e por forma de pagamento
- [ ] Relatório financeiro por categoria e mês
- [ ] Geração de gráficos financeiros
- [ ] Cadastro de contas como forma de pagamento

 
