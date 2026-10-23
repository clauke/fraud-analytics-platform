# SSIS Pipeline Documentation — Fraud Analytics Platform

## 1. Objetivo

Documentar a orquestração do pipeline de ETL do projeto Fraud Analytics Platform por meio do SQL Server Integration Services (SSIS), integrando a carga de dados do ambiente STG para ODS e, posteriormente, do ODS para o Data Warehouse (DWH).

## 2. Pacote SSIS

- **Package:** `PKG_FraudAnalytics_STG_ODS.dtsx`
- **Projeto SSIS:** `FraudAnalyticsSSIS`
- **Localização:** `ssis/FraudAnalyticsSSIS/FraudAnalyticsSSIS/`
- **Banco de dados:** `FraudAnalytics`
- **Servidor SQL Server:** `DESKTOP-R90TA06\SQL2022`

## 3. Arquitetura do pipeline

O processo integrado contempla as seguintes etapas:

1. **STG → ODS:** execução do script Python `05_load_ods_data.py`, responsável pela carga das tabelas de transações e identidades.
2. **Carga da dimensão de datas:** execução da procedure `dwh.usp_load_dim_date`.
3. **Carga das dimensões do DWH:** execução da procedure `dwh.usp_load_dwh_dimensions`.
4. **Carga da tabela fato:** execução da procedure `dwh.usp_load_fact_transaction`.

As etapas são conectadas por restrições de precedência de sucesso, de modo que a próxima tarefa seja executada após a conclusão bem-sucedida da anterior.

## 4. Componentes do pacote

| Componente | Responsabilidade |
|---|---|
| Execute Process Task | Executar o script Python de carga STG → ODS |
| `SQL_Load_Dim_Date` | Carregar a dimensão de datas |
| `SQL_Load_DWH_Dimensions` | Carregar as dimensões do Data Warehouse |
| `SQL_Load_DWH_Fact` | Carregar a tabela fato de transações |

## 5. Modelo dimensional

O Data Warehouse utiliza as seguintes tabelas dimensionais:

- `dwh.dim_date`
- `dwh.dim_product`
- `dwh.dim_card`
- `dwh.dim_identity`
- `dwh.dim_device`
- `dwh.dim_address`

A tabela fato é `dwh.fact_transaction`.

## 6. Validação da execução integrada

O pacote SSIS foi executado com sucesso, com todas as tarefas concluídas sem erros.

As verificações realizadas confirmaram:

- Ausência de `TransactionID` duplicados na tabela fato.
- Ausência de transações com `DateKey` sem correspondência na dimensão de datas.
- Ausência de registros na dimensão de dispositivos com `DeviceType` e `DeviceInfo` simultaneamente nulos.
- Preservação do membro especial `DeviceKey = 0`, com valores `Unknown`.
- Manutenção de 2.960 registros em `dwh.dim_device` após a execução integrada.

## 7. Tratamento de qualidade dos dados

Durante a validação, foi identificado um registro inválido na dimensão `dwh.dim_device`, com `DeviceType` e `DeviceInfo` nulos.

A procedure `dwh.usp_load_dwh_dimensions` foi ajustada para impedir novas inserções de registros em que ambos os atributos estejam nulos.

O registro inválido existente foi removido após a confirmação de que não havia transações associadas a ele. A execução subsequente do pacote confirmou que o problema não voltou a ocorrer.

## 8. Considerações finais

A orquestração SSIS integra a carga STG → ODS e as rotinas de carga do Data Warehouse em um fluxo automatizado.

Os testes realizados demonstraram execução bem-sucedida do pacote e consistência das verificações de qualidade aplicadas às tabelas dimensionais e à tabela fato.

Este documento registra a configuração e os resultados observados durante a validação do pipeline. Alterações futuras no pacote, nas procedures ou nas regras de qualidade deverão ser refletidas nesta documentação.
