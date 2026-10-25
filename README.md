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