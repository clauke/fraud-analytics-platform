/* 
============================================================================
=== 
Projeto: Fraud Analytics Platform 
Arquivo: 03_create_stg_tables.sql 
Objetivo: Criação das tabelas da camada STG (Staging) 
Banco: FraudAnalytics 
Schema: stg 
Versão: 0.1 
============================================================================
=== 
*/

USE FraudAnalytics;
GO

/* 
============================================================================ 
    Tabela: stg.train_transaction 

============================================================================ 
*/

IF OBJECT_ID('stg.train_transaction', 'U') IS NULL
BEGIN

    CREATE TABLE stg.train_transaction
    (
        stg_id BIGINT IDENTITY(1,1) NOT NULL,

        TransactionID BIGINT NOT NULL,
        TransactionDT BIGINT NULL,
        TransactionAmt DECIMAL(18,4) NULL,
        ProductCD VARCHAR(10) NULL,

        card1 BIGINT NULL,
        card2 DECIMAL(18,4) NULL,
        card3 DECIMAL(18,4) NULL,
        card4 VARCHAR(50) NULL,
        card5 DECIMAL(18,4) NULL,
        card6 VARCHAR(50) NULL,

        addr1 DECIMAL(18,4) NULL,
        addr2 DECIMAL(18,4) NULL,

        dist1 DECIMAL(18,4) NULL,
        dist2 DECIMAL(18,4) NULL,

        P_emaildomain VARCHAR(255) NULL,
        R_emaildomain VARCHAR(255) NULL,

        isFraud BIT NULL,

        load_date DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        source_file VARCHAR(255) NULL,
        batch_id UNIQUEIDENTIFIER NULL,
        etl_status VARCHAR(20) NULL,

        CONSTRAINT PK_stg_train_transaction
            PRIMARY KEY CLUSTERED (stg_id)
    );

END;
GO

/*
============================================================================ 
    Tabela: stg.train_identity 

============================================================================ 
*/

IF OBJECT_ID('stg.train_identity', 'U') IS NULL
BEGIN

    CREATE TABLE stg.train_identity
    (
        stg_id BIGINT IDENTITY(1,1) NOT NULL,

        TransactionID BIGINT NOT NULL,
        DeviceType VARCHAR(50) NULL,
        DeviceInfo VARCHAR(255) NULL,

        load_date DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        source_file VARCHAR(255) NULL,
        batch_id UNIQUEIDENTIFIER NULL,
        etl_status VARCHAR(20) NULL,

        CONSTRAINT PK_stg_train_identity
            PRIMARY KEY CLUSTERED (stg_id)
    );

END;
GO

/*
============================================================================ 
    Tabela: stg.test_transaction 

============================================================================ 
*/

IF OBJECT_ID('stg.test_transaction', 'U') IS NULL 
BEGIN 

    CREATE TABLE stg.test_transaction 
    ( 
        stg_id BIGINT IDENTITY(1,1) NOT NULL, 
        
        TransactionID BIGINT NOT NULL, 
        TransactionDT BIGINT NULL, 
        TransactionAmt DECIMAL(18,4) NULL, 
        ProductCD VARCHAR(10) NULL, 
        
        card1 BIGINT NULL, 
        card2 DECIMAL(18,4) NULL, 
        card3 DECIMAL(18,4) NULL, 
        card4 VARCHAR(50) NULL, 
        card5 DECIMAL(18,4) NULL, 
        card6 VARCHAR(50) NULL, 
        
        addr1 DECIMAL(18,4) NULL, 
        addr2 DECIMAL(18,4) NULL, 
        
        dist1 DECIMAL(18,4) NULL, 
        dist2 DECIMAL(18,4) NULL, 
        
        P_emaildomain VARCHAR(255) NULL, 
        R_emaildomain VARCHAR(255) NULL, 
        
        load_date DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), 
        source_file VARCHAR(255) NULL, 
        batch_id UNIQUEIDENTIFIER NULL, 
        etl_status VARCHAR(20) NULL, 
        
        CONSTRAINT PK_stg_test_transaction 
            PRIMARY KEY CLUSTERED (stg_id) 
    ); 
            
END; 
GO

/* 
============================================================================ 
    Tabela: stg.test_identity 

============================================================================ 
*/

IF OBJECT_ID('stg.test_identity', 'U') IS NULL 
BEGIN 

    CREATE TABLE stg.test_identity 
    ( 
        stg_id BIGINT IDENTITY(1,1) NOT NULL, 
        
        TransactionID BIGINT NOT NULL, 
        DeviceType VARCHAR(50) NULL, 
        DeviceInfo VARCHAR(255) NULL, 
        
        load_date DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(), 
        source_file VARCHAR(255) NULL, 
        batch_id UNIQUEIDENTIFIER NULL, 
        etl_status VARCHAR(20) NULL, 
        
        CONSTRAINT PK_stg_test_identity 
            PRIMARY KEY CLUSTERED (stg_id) 
    ); 
    
END; 
GO

/* 
============================================================================ 
    Índices 

============================================================================ 
*/

CREATE INDEX IX_stg_train_transaction_TransactionID
ON stg.train_transaction (TransactionID);
GO

CREATE INDEX IX_stg_train_identity_TransactionID
ON stg.train_identity (TransactionID);
GO

CREATE INDEX IX_stg_test_transaction_TransactionID
ON stg.test_transaction (TransactionID);
GO

CREATE INDEX IX_stg_test_identity_TransactionID
ON stg.test_identity (TransactionID);
GO

/* 
============================================================================ 
    Fim do script 
    
============================================================================ 
*/