/*
    Fraud Analytics Platform
    Script: 07_create_dwh_dimensions.sql
    Objetivo: Criação das dimensões do Data Warehouse (DWH)
*/

USE FraudAnalytics;
GO

/* ============================================================
   1. DIM_DATE
   ============================================================ */

IF OBJECT_ID('dwh.dim_date', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.dim_date
    (
        DateKey     int             NOT NULL,
        FullDate    date            NOT NULL,
        [Year]      smallint        NOT NULL,
        [Quarter]   tinyint         NOT NULL,
        [Month]     tinyint         NOT NULL,
        MonthName   varchar(20)     NOT NULL,
        [Day]       tinyint         NOT NULL,
        DayOfWeek   tinyint         NOT NULL,
        DayName     varchar(20)     NOT NULL,
        IsWeekend   bit             NOT NULL,

        CONSTRAINT PK_dim_date
            PRIMARY KEY (DateKey),

        CONSTRAINT UQ_dim_date_FullDate
            UNIQUE (FullDate)
    );
END;
GO

/* ============================================================
   2. DIM_PRODUCT
   ============================================================ */

IF OBJECT_ID('dwh.dim_product', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.dim_product
    (
        ProductKey      int IDENTITY(1,1)   NOT NULL,
        ProductCD       varchar(10)         NULL,

        CONSTRAINT PK_dim_product
            PRIMARY KEY (ProductKey),

        CONSTRAINT UQ_dim_product_ProductCD
            UNIQUE (ProductCD)
    );
END;
GO

/* ============================================================
   3. DIM_CARD
   ============================================================ */

IF OBJECT_ID('dwh.dim_card', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.dim_card
    (
        CardKey     int IDENTITY(1,1)   NOT NULL,
        card1       int                 NULL,
        card2       int                 NULL,
        card3       decimal(18,6)       NULL,
        card4       varchar(50)         NULL,
        card5       decimal(18,6)       NULL,
        card6       varchar(50)         NULL,

        CONSTRAINT PK_dim_card
            PRIMARY KEY (CardKey)
    );
END;
GO

/* ============================================================
   4. DIM_IDENTITY
   ============================================================ */

IF OBJECT_ID('dwh.dim_identity', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.dim_identity
    (
        IdentityKey     int IDENTITY(1,1)   NOT NULL,

        /* Campos numéricos */
        id_01           decimal(18,6)       NULL,
        id_02           decimal(18,6)       NULL,
        id_03           decimal(18,6)       NULL,
        id_04           decimal(18,6)       NULL,
        id_05           decimal(18,6)       NULL,
        id_06           decimal(18,6)       NULL,
        id_07           decimal(18,6)       NULL,
        id_08           decimal(18,6)       NULL,
        id_09           decimal(18,6)       NULL,
        id_10           decimal(18,6)       NULL,
        id_11           decimal(18,6)       NULL,

        /* Campo textual */
        id_12           varchar(255)        NULL,

        /* Campos numéricos */
        id_13           decimal(18,6)       NULL,
        id_14           decimal(18,6)       NULL,

        /* Campos textuais */
        id_15           varchar(255)        NULL,
        id_16           varchar(255)        NULL,

        /* Campos numéricos */
        id_17           decimal(18,6)       NULL,
        id_18           decimal(18,6)       NULL,
        id_19           decimal(18,6)       NULL,
        id_20           decimal(18,6)       NULL,
        id_21           decimal(18,6)       NULL,
        id_22           decimal(18,6)       NULL,

        /* Campo textual */
        id_23           varchar(255)        NULL,

        /* Campos numéricos */
        id_24           decimal(18,6)       NULL,
        id_25           decimal(18,6)       NULL,
        id_26           decimal(18,6)       NULL,

        /* Campos textuais */
        id_27           varchar(255)        NULL,
        id_28           varchar(255)        NULL,
        id_29           varchar(255)        NULL,
        id_30           varchar(255)        NULL,
        id_31           varchar(255)        NULL,

        /* Campo numérico */
        id_32           decimal(18,6)       NULL,

        /* Campos textuais */
        id_33           varchar(255)        NULL,
        id_34           varchar(255)        NULL,
        id_35           varchar(255)        NULL,
        id_36           varchar(255)        NULL,
        id_37           varchar(255)        NULL,
        id_38           varchar(255)        NULL,

        CONSTRAINT PK_dim_identity
            PRIMARY KEY (IdentityKey)
    );
END;
GO

/* ============================================================
   5. DIM_DEVICE
   ============================================================ */

IF OBJECT_ID ('dwh.dim_device', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.dim_device
    (
        DeviceKey       int IDENTITY(1,1)   NOT NULL,
        DeviceType      varchar(50)         NULL,
        DeviceInfo      varchar(255)        NULL,

        CONSTRAINT PK_dim_device
            PRIMARY KEY (DeviceKey)
    );
END;
GO

/* ============================================================
   6. DIM_ADDRESS
   ============================================================ */

IF OBJECT_ID('dwh.dim_address', 'U') IS NULL
BEGIN
    CREATE TABLE dwh.dim_address
    (
        AddressKey  int IDENTITY(1,1)   NOT NULL,
        addr1       decimal(18,6)       NULL,
        addr2       decimal(18,6)       NULL,
        dist1       decimal(18,6)       NULL,
        dist2       decimal(18,6)       NULL,

        CONSTRAINT PK_dim_address
            PRIMARY KEY (AddressKey)
    );
END;
GO