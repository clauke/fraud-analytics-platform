/*
===============================================================================
Fraud Analytics Platform
SQL Script: 04_create_ods_tables.sql
Camada: ODS (Operational Data Store)
Versão: 0.2
===============================================================================

Objetivo:
- Consolidar os dados provenientes da camada STG
- Manter uma estrutura operacional integrada
- Preparar os dados para as etapas posteriores de DW e Machine Learning

Schema: ods
===============================================================================
*/

USE FraudAnalytics;
GO

/* ============================================================================
   1. Criar schema ODS
============================================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'ods'
)
BEGIN
    EXEC('CREATE SCHEMA ods');
END;
GO

/* ============================================================================
   2. Limpeza das tabelas ODS existentes
============================================================================ */

IF OBJECT_ID('ods.transactions', 'U') IS NOT NULL
    DROP TABLE ods.transactions;
GO

IF OBJECT_ID('ods.identities', 'U') IS NOT NULL
    DROP TABLE ods.identities;
GO

/* ============================================================================
   3. Tabela ODS - TRANSACTIONS
============================================================================ */

CREATE TABLE ods.transactions
(
    TransactionID     BIGINT            NOT NULL,
    TransactionDT     BIGINT            NULL,
    TransactionAmt    DECIMAL(18, 6)    NULL,

    ProductCD         VARCHAR(10)       NULL,

    card1             INT               NULL,
    card2             INT               NULL,
    card3             DECIMAL(18, 6)    NULL,
    card4             VARCHAR(50)       NULL,
    card5             DECIMAL(18, 6)    NULL,
    card6             VARCHAR(50)       NULL,

    addr1             DECIMAL(18, 6)    NULL,
    addr2             DECIMAL(18, 6)    NULL,

    dist1             DECIMAL(18, 6)    NULL,
    dist2             DECIMAL(18, 6)    NULL,

    P_emaildomain     VARCHAR(255)      NULL,
    R_emaildomain     VARCHAR(255)      NULL,

    isFraud           BIT               NULL,

    /* Metadados da origem */
    data_source       VARCHAR(10)       NOT NULL,
    source_file       VARCHAR(255)      NULL,
    batch_id          UNIQUEIDENTIFIER  NOT NULL,
    load_date         DATETIME2(0)      NOT NULL,

    /* Controle de processamento */
    etl_status        VARCHAR(20)       NOT NULL,

    CONSTRAINT PK_ods_transactions
        PRIMARY KEY (TransactionID, data_source)
);
GO

/* ============================================================================
   4. Tabela ODS - IDENTITIES
============================================================================ */

CREATE TABLE ods.identities
(
    TransactionID       BIGINT           NOT NULL,

    /* Campos numéricos */
    id_01               DECIMAL(18, 6)   NULL,
    id_02               DECIMAL(18, 6)   NULL,
    id_03               DECIMAL(18, 6)   NULL,
    id_04               DECIMAL(18, 6)   NULL,
    id_05               DECIMAL(18, 6)   NULL,
    id_06               DECIMAL(18, 6)   NULL,
    id_07               DECIMAL(18, 6)   NULL,
    id_08               DECIMAL(18, 6)   NULL,
    id_09               DECIMAL(18, 6)   NULL,
    id_10               DECIMAL(18, 6)   NULL,
    id_11               DECIMAL(18, 6)   NULL,

    /* Campos textuais */
    id_12               VARCHAR(255)     NULL,

    /* Campos numéricos */
    id_13               DECIMAL(18, 6)   NULL,
    id_14               DECIMAL(18, 6)   NULL,

    /* Campos textuais */
    id_15               VARCHAR(255)     NULL,
    id_16               VARCHAR(255)     NULL,

    /* Campos numéricos */
    id_17               DECIMAL(18, 6)   NULL,
    id_18               DECIMAL(18, 6)   NULL,
    id_19               DECIMAL(18, 6)   NULL,
    id_20               DECIMAL(18, 6)   NULL,
    id_21               DECIMAL(18, 6)   NULL,
    id_22               DECIMAL(18, 6)   NULL,

    /* Campo textual */
    id_23               VARCHAR(255)     NULL,

    /* Campos numéricos */
    id_24               DECIMAL(18, 6)   NULL,
    id_25               DECIMAL(18, 6)   NULL,
    id_26               DECIMAL(18, 6)   NULL,

    /* Campos textuais */
    id_27               VARCHAR(255)     NULL,
    id_28               VARCHAR(255)     NULL,
    id_29               VARCHAR(255)     NULL,
    id_30               VARCHAR(255)     NULL,
    id_31               VARCHAR(255)     NULL,

    /* Campo numérico */
    id_32               DECIMAL(18, 6)   NULL,

    /* Campos textuais */
    id_33               VARCHAR(255)     NULL,
    id_34               VARCHAR(255)     NULL,
    id_35               VARCHAR(255)     NULL,
    id_36               VARCHAR(255)     NULL,
    id_37               VARCHAR(255)     NULL,
    id_38               VARCHAR(255)     NULL,

    DeviceType          VARCHAR(50)      NULL,
    DeviceInfo          VARCHAR(255)     NULL,

    /* Metadados da origem */
    data_source         VARCHAR(10)      NOT NULL,
    source_file         VARCHAR(255)     NULL,
    batch_id            UNIQUEIDENTIFIER NOT NULL,
    load_date           DATETIME2(0)     NOT NULL,

    /* Controle de processamento */
    etl_status          VARCHAR(20)      NOT NULL,

    CONSTRAINT PK_ods_identities
        PRIMARY KEY (TransactionID, data_source)
);
GO

/* ============================================================================
   5. Índices
============================================================================ */

CREATE INDEX IX_ods_transactions_source
    ON ods.transactions (data_source);
GO

CREATE INDEX IX_ods_transactions_isFraud
    ON ods.transactions (isFraud);
GO

CREATE INDEX IX_ods_identities_source
    ON ods.identities (data_source);
GO

CREATE INDEX IX_ods_identities_DeviceType
    ON ods.identities (DeviceType);
GO

/* ============================================================================
   6. Validação da estrutura
============================================================================ */

SELECT
    s.name AS schema_name,
    t.name AS table_name
FROM sys.tables t
INNER JOIN sys.schemas s
    ON t.schema_id = s.schema_id
WHERE s.name = 'ods'
ORDER BY t.name;
GO
