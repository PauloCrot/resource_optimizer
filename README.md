# Project EVM Monitor and Field Auditor

## O Problema de Negocio

Em empresas multidisciplinares de engenharia e gestao de projetos, como oleo e gas, mineracao, energias renovaveis e industria pesada, um grande desafio operacional e o desalinhamento entre o planejado e o executado. 

No dia a dia de campo, engenheiros e fiscais preenchem relatorios semanais sob pressao, gerando dados caoticos e inconsistentes. Isso inclui a mistura de pontuacoes, virgulas, cifras e formatos de datas divergentes. 

A utilizacao de planilhas espalhadas dificulta a consolidacao rapida de indicadores vitais. A demora na identificacao de estouros de orcamento ou desvios de cronograma gera prejuizos financeiros severos e riscos contratuais para a organizacao.

## A Solucao Tecnica e Arquitetura

O sistema foi desenvolvido utilizando uma arquitetura modular em Python buscando manter separacao de responsabilidades, manutenibilidade e escalabilidade do codigo. O fluxo e dividido nas seguintes camadas dentro do diretorio `src/`:

- `src/cleaning.py`: Modulo de ingestao e tratamento de dados brutos (`raw_field_data.csv`). Realiza a normalizacao de campos monetarios inconsistentes e conversao padronizada de datas.
- `src/metrics.py`: Modulo de regras de negocio do Earned Value Management (EVM). Executa o calculo do CPI (Cost Performance Index), SPI (Schedule Performance Index), classificacao automatizada de status de risco e ordenacao cronologica temporal.
- `src/storage.py`: Modulo de persistencia responsavel por exportar o DataFrame processado e ordenado para um arquivo de relatorio estruturado (`processed_evm_report.csv`).
- `src/main.py`: Modulo orquestrador que executa o pipeline completo de ponta a ponta.

## Estrutura do Repositorio

```text
nr-evm-monitor/
│
├── data/
│   ├── raw_field_data.csv
│   └── processed_evm_report.csv
│
├── src/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── metrics.py
│   ├── storage.py
│   └── main.py
│
├── requirements.txt
└── README.md


## Formulacao Matematica

O sistema utiliza formulacoes matematicas divididas entre a camada de diagnostico de desempenho (EVM) e a camada de prescricao de decisoes (Otimizacao de Recursos).

### 1. Indicadores de Desempenho (Earned Value Management)

Para cada medicao $t$ de um projeto $i$, os indices de desempenho de custo e prazo sao calculados por:

- **Indice de Desempenho de Custo (CPI):**
  $$CPI_i = \frac{EV_i}{AC_i}$$

- **Indice de Desempenho de Cronograma (SPI):**
  $$SPI_i = \frac{EV_i}{PV_i}$$

Onde:
- $PV_i$ (Planned Value): Valor Planejado.
- $EV_i$ (Earned Value): Valor Agregado.
- $AC_i$ (Actual Cost): Custo Real.

---

### 2. Modelo de Otimizacao de Alocacao de Recursos

A alocacao de orcamento adicional e modelada como um problema de Programacao Linear (Mochila Fracionaria / Fractional Knapsack), considerando apenas a medicao mais recente de cada projeto que apresente desvio ($CPI_i < 1.0$ ou $SPI_i < 1.0$).

#### Parametros e Variaveis:
- $I$: Conjunto de projetos elegiveis com desvio no portfolio.
- $B_{total}$: Orcamento global limite para aporte financeiro ($B_{total} = 2.500.000,00$).
- $AC_i$: Custo real atual do projeto $i$.
- $M_i$: Demanda maxima de aporte do projeto $i$, definida como 30% do custo real:
  $$M_i = 0.30 \cdot AC_i$$
- $W_i$: Fator de urgencia (peso da funcao objetivo), inversamente proporcional a media dos indices de desempenho:
  $$W_i = \max\left(0.1, 2.0 - \frac{CPI_i + SPI_i}{2}\right)$$
- $x_i$: Variavel de decisao representando o montante financeiro alocado ao projeto $i$.

#### Formulacao do Modelo:

- **Funcao Objetivo:** Maximizar o retorno ponderado de prioridade sobre os projetos contemplados:
  $$\max \sum_{i \in I} W_i \cdot x_i$$

- **Restricao de Orcamento Global:**
  $$\sum_{i \in I} x_i \le B_{total}$$

- **Restricoes de Demanda e Nao-Negatividade:**
  $$0 \le x_i \le M_i, \quad \forall i \in I$$