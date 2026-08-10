# ETL Design

**Projeto:** Fraud Analytics Platform

**Documento:** 10_ETL_Design.md

**Versão:** 0.1

**Status:** Em desenvolvimento

---

# 1. Objetivo

Este documento define a arquitetura do processo de **ETL (Extract, Transform, Load)** da plataforma Fraud Analytics Platform.

O objetivo é estabelecer a estrutura das camadas de dados, os fluxos de transformação, as regras de carregamento e os padrões de nomenclatura que serão utilizados durante a Sprint 3.

A implementação será realizada utilizando **Python, SQL Server e SSIS**.

---

# 2. Arquitetura do Pipeline

O pipeline será organizado em quatro camadas principais.

```text
CSV (Kaggle)
        ↓
      RAW
        ↓
    STAGING
        ↓
       ODS
        ↓
DATA WAREHOUSE
```

Cada camada possui uma responsabilidade específica.

---

# 3. Camada RAW

## Objetivo

Armazenar os arquivos originais sem qualquer transformação.

## Origem

Arquivos do dataset IEEE-CIS Fraud Detection.

## Arquivos

* train_transaction.csv
* train_identity.csv
* test_transaction.csv
* test_identity.csv
* sample_submission.csv

## Características

* sem alterações de estrutura;
* sem padronização de nomes;
* preservação integral do conteúdo original.

## Localização

```text
data/raw/
```

---

# 4. Camada STAGING

## Objetivo

Realizar ingestão, padronização inicial e preparação dos dados.

## Principais transformações

### Estrutura

* padronização de tipos de dados;
* tratamento de colunas numéricas;
* normalização de campos categóricos;
* remoção de espaços;
* padronização de valores nulos.

### Auditoria

Serão adicionadas colunas técnicas.

| Coluna      | Descrição              |
| ----------- | ---------------------- |
| load_date   | Data de carga          |
| source_file | Arquivo de origem      |
| batch_id    | Identificador da carga |

## Schema

```sql
stg
```

## Tabelas

* stg.train_transaction
* stg.train_identity
* stg.test_transaction
* stg.test_identity

---

# 5. Camada ODS (Operational Data Store)

## Objetivo

Consolidar os dados e aplicar regras de negócio.

## Principais atividades

### Integração

LEFT JOIN entre:

* train_transaction
* train_identity

### Padronização

* DeviceType
* DeviceInfo
* ProductCD
* card4
* card6

### Variáveis derivadas

As seguintes variáveis serão criadas.

| Variável             | Origem         |
| -------------------- | -------------- |
| TransactionHour      | TransactionDT  |
| TransactionDay       | TransactionDT  |
| Faixa_TransactionAmt | TransactionAmt |
| is_mobile            | DeviceType     |

### Regras de qualidade

* validação de chaves;
* consistência de tipos;
* monitoramento de valores ausentes;
* validação de volumes.

## Schema

```sql
ods
```

## Tabela principal

```sql
ods.transaction_fraud
```

---

# 6. Data Warehouse

## Objetivo

Disponibilizar dados analíticos para Power BI e Machine Learning.

## Modelo

Será utilizado modelo dimensional.

### Tabela fato

FactTransaction

### Dimensões

DimProduct

DimCard

DimDevice

DimTime

## Schema

```sql
dw
```

---

# 7. Estrutura do Banco SQL Server

O banco será organizado em schemas.

| Schema | Finalidade           |
| ------ | -------------------- |
| raw    | dados originais      |
| stg    | staging              |
| ods    | dados integrados     |
| dw     | modelo dimensional   |
| audit  | logs e monitoramento |

---

# 8. Fluxo de Execução

## Extração

Python

↓

Leitura dos CSVs

↓

Validação de arquivos

↓

Carga para STAGING

↓

Transformações SQL

↓

Carga para ODS

↓

Carga para DW

↓

Power BI

---

# 9. Estratégia de Carga

## Fase inicial

Carga completa (Full Load).

## Fases futuras

Carga incremental.

Controle por:

* batch_id;
* load_date;
* TransactionID.

---

# 10. Validações

Ao final de cada carga serão executadas verificações.

## Volume

* registros lidos;
* registros carregados;
* registros rejeitados.

## Integridade

* duplicidade de TransactionID;
* chaves órfãs;
* valores nulos críticos.

## Reconciliação

Comparação entre:

RAW

↓

STAGING

↓

ODS

---

# 11. Ferramentas

## Python

Responsável por:

* ingestão;
* validações;
* automação.

## SQL Server

Responsável por:

* armazenamento;
* transformações;
* integração;
* ODS;
* Data Warehouse.

## SSIS

Responsável por:

* orquestração;
* agendamento;
* monitoramento;
* cargas incrementais.

---

# 12. Próximos Passos

Sprint 3.1

* instalação e configuração do SQL Server;
* criação do banco FraudAnalytics;
* criação dos schemas;
* criação das tabelas STAGING;
* desenvolvimento do primeiro pipeline Python (CSV → STAGING).

Este documento servirá como referência técnica para toda a implementação da camada de Engenharia de Dados do projeto.
