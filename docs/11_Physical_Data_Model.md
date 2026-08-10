# Modelagem Física do Banco de Dados

**Projeto:** Fraud Analytics Platform

**Documento:** 11_Physical_Data_Model.md

**Versão:** 0.1

**Status:** Em desenvolvimento

---

# 1. Objetivo

Este documento define a **modelagem física do banco de dados** da plataforma Fraud Analytics Platform.

O objetivo é especificar a estrutura física do banco SQL Server, incluindo schemas, tabelas, tipos de dados, chaves, índices e padrões de nomenclatura que serão utilizados na implementação da arquitetura de dados.

A modelagem física será utilizada como base para o desenvolvimento do ETL, da camada ODS e do Data Warehouse.

---

# 2. Arquitetura Física

O banco será organizado em camadas, seguindo a arquitetura definida no documento **10_ETL_Design.md**.

```text
CSV (Kaggle)
        ↓
      RAW
        ↓
      STG
        ↓
      ODS
        ↓
       DW
```

Cada camada será implementada em um schema específico do SQL Server.

---

# 3. Estrutura do Banco

## Banco de dados

```text
FraudAnalytics
```

## Plataforma

* Microsoft SQL Server 2022
* Linguagem T-SQL
* Banco relacional

## Schemas

| Schema | Finalidade           |
| ------ | -------------------- |
| raw    | dados originais      |
| stg    | staging              |
| ods    | dados integrados     |
| dw     | modelo dimensional   |
| audit  | logs e monitoramento |

---

# 4. Camada RAW

## Objetivo

Armazenar os dados exatamente como recebidos do dataset.

## Tabelas

* raw.train_transaction
* raw.train_identity
* raw.test_transaction
* raw.test_identity

## Características

* preservação da estrutura original;
* sem transformações;
* carga otimizada para alto volume.

## Chave primária

Todas as tabelas utilizarão:

```text
TransactionID
```

como chave primária.

---

# 5. Estrutura das Tabelas RAW

## raw.train_transaction

### Campos principais

| Coluna         | Tipo          |
| -------------- | ------------- |
| TransactionID  | BIGINT        |
| TransactionDT  | INT           |
| TransactionAmt | DECIMAL(18,4) |
| ProductCD      | VARCHAR(10)   |
| card1          | INT           |
| card2          | INT           |
| card3          | INT           |
| card4          | VARCHAR(20)   |
| card5          | INT           |
| card6          | VARCHAR(20)   |
| addr1          | INT           |
| addr2          | INT           |
| dist1          | DECIMAL(18,4) |
| dist2          | DECIMAL(18,4) |
| P_emaildomain  | VARCHAR(100)  |
| R_emaildomain  | VARCHAR(100)  |
| isFraud        | BIT           |

As colunas V1–V339 serão armazenadas como **FLOAT**.

---

## raw.train_identity

### Campos principais

| Coluna        | Tipo         |
| ------------- | ------------ |
| TransactionID | BIGINT       |
| DeviceType    | VARCHAR(20)  |
| DeviceInfo    | VARCHAR(255) |

Os campos id_01 até id_38 utilizarão tipos numéricos ou textuais conforme o dicionário do dataset.

---

## raw.test_transaction

Estrutura idêntica à tabela train_transaction, sem a coluna **isFraud**.

---

## raw.test_identity

Estrutura idêntica à tabela train_identity.

---

# 6. Relacionamentos

O dataset original possui relacionamento **1:1** entre as tabelas de transações e identidade.

```text
train_transaction
        |
        | TransactionID
        |
train_identity
```

Na camada RAW não serão criadas chaves estrangeiras para preservar a performance de carga.

Os relacionamentos serão implementados na camada ODS.

---

# 7. Estratégia de Chaves

## Chaves primárias

| Tabela            | Chave         |
| ----------------- | ------------- |
| train_transaction | TransactionID |
| train_identity    | TransactionID |
| test_transaction  | TransactionID |
| test_identity     | TransactionID |

## Chaves estrangeiras

Serão implementadas apenas nas camadas ODS e DW.

---

# 8. Estratégia de Índices

## Índice Clustered

Todas as tabelas RAW utilizarão índice clustered em:

```text
TransactionID
```

## Índices Nonclustered

Serão criados índices para as colunas:

* TransactionDT
* ProductCD
* card1
* card4
* isFraud

Esses índices serão utilizados nas consultas analíticas e nos processos de transformação.

---

# 9. Padronização de Tipos de Dados

## Valores monetários

```sql
DECIMAL(18,4)
```

Evita problemas de precisão.

## Identificadores

```sql
BIGINT
```

Permite crescimento futuro.

## Campos categóricos

```sql
VARCHAR
```

Reduz consumo de armazenamento.

## Variável alvo

```sql
BIT
```

Representação eficiente para o campo **isFraud**.

---

# 10. Convenções de Nomenclatura

## Tabelas

Padrão:

```text
schema.nome_da_tabela
```

Exemplos:

* raw.train_transaction
* stg.train_transaction
* ods.transaction_fraud
* dw.fact_transaction

## Chaves primárias

Padrão:

```text
PK_NomeTabela
```

Exemplo:

```text
PK_TrainTransaction
```

## Chaves estrangeiras

Padrão:

```text
FK_TabelaFilha_TabelaPai
```

## Índices

Padrão:

```text
IX_Tabela_Coluna
```

Exemplo:

```text
IX_TrainTransaction_ProductCD
```

---

# 11. Considerações de Performance

A modelagem física foi projetada para suportar:

* cargas em lote;
* transformações de ETL;
* consultas analíticas;
* integração com Power BI.

As tabelas RAW serão otimizadas para **INSERT**, enquanto as tabelas ODS e DW serão otimizadas para **SELECT**.

---

# 12. Evolução da Modelagem

Na Sprint 3 serão implementadas apenas as estruturas da camada RAW.

As próximas etapas incluirão:

## STG

* padronização;
* auditoria;
* controle de carga.

## ODS

* integração das tabelas;
* regras de negócio;
* variáveis derivadas.

## DW

* tabela fato;
* dimensões;
* modelo estrela.

---

# 13. Artefatos de Implementação

A implementação da modelagem física será realizada por meio do script:

```text
sql/01_create_database.sql
```

Este script criará:

* banco FraudAnalytics;
* schemas;
* tabelas RAW;
* chaves primárias;
* índices iniciais.

---

# 14. Próximos Passos

Sprint 3.2

* criação do banco FraudAnalytics;
* criação dos schemas;
* criação das tabelas RAW;
* implementação dos índices;
* carga inicial dos arquivos CSV.

Este documento servirá como referência técnica para a implementação física do banco SQL Server e para o desenvolvimento das próximas etapas do pipeline de dados.
