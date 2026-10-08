/*
    Fraud Analytics Platform
    Script: 09_create_dwh_fact.sql
    Objetivo: Criação da tabela fato de transações no Data Warehouse
*/

USE FraudAnalytics;
GO

IF OBJECT_ID('dwh.fact_transaction', 'U') IS NOT NULL
BEGIN
    DROP TABLE dwh.fact_transaction;
END;
GO

CREATE TABLE dwh.fact_transaction
(
    -- Chave substituta da fato
    TransactionKey  BIGINT IDENTITY(1,1) NOT NULL,

    -- Chave de negócio
    TransactionID   BIGINT NOT NULL,

    -- Chaves estrangeiras das dimensões
    DateKey     INT     NOT NULL,
    ProductKey  INT     NOT NULL,
    CardKey     INT     NOT NULL,
    IdentityKey INT     NOT NULL,
    DeviceKey   INT     NOT NULL,
    AddressKey  INT     NOT NULL,

    -- Métricas e atributos da transação
    TransactionDT   BIGINT          NULL,
    TransactionAmt  DECIMAL(18,6)   NULL,
    isFraud         BIT             NULL,

    -- Metadados de carga
    source_file     VARCHAR(255)        NULL,
    batch_id        UNIQUEIDENTIFIER    NOT NULL,
    load_date       DATETIME2           NOT NULL,
    etl_status      VARCHAR(20)         NOT NULL,

    CONSTRAINT PK_fact_transaction
        PRIMARY KEY (TransactionKey),

    CONSTRAINT UQ_fact_transaction_TransactionID
        UNIQUE (TransactionID),

    CONSTRAINT FK_fact_transaction_date
        FOREIGN KEY (DateKey)
        REFERENCES dwh.dim_date (DateKey),

    CONSTRAINT FK_fact_transaction_product
        FOREIGN KEY (ProductKey)
        REFERENCES dwh.dim_product (ProductKey),
        
    CONSTRAINT FK_fact_transaction_card
        FOREIGN KEY (CardKey)
        REFERENCES dwh.dim_card (CardKey),

    CONSTRAINT FK_fact_transaction_identity
        FOREIGN KEY (IdentityKey)
        REFERENCES dwh.dim_identity (IdentityKey),

    CONSTRAINT FK_fact_transaction_device
        FOREIGN KEY (DeviceKey)
        REFERENCES dwh.dim_device (DeviceKey),
    
    CONSTRAINT FK_fact_transaction_address
        FOREIGN KEY (AddressKey)
        REFERENCES dwh.dim_address (AddressKey)
);
GO