/*
    Fraud Analytics Platform
    Script: 08_insert_dwh_unknown_members.sql
    Objetivo: Inserção dos registros Unknown nas dimensões do DWH
*/

USE FraudAnalytics;
GO


/* ============================================================
   1. DIM_PRODUCT
   ============================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM dwh.dim_product
    WHERE ProductKey = 0
)
BEGIN
    SET IDENTITY_INSERT dwh.dim_product ON;

    INSERT INTO dwh.dim_product
    (
        ProductKey,
        ProductCD
    )
    VALUES
    (
        0,
        'Unknown'
    );

    SET IDENTITY_INSERT dwh.dim_product OFF;
END;
GO

/* ============================================================
   2. DIM_CARD
   ============================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM dwh.dim_card
    WHERE CardKey = 0
)
BEGIN
    SET IDENTITY_INSERT dwh.dim_card ON;

    INSERT INTO dwh.dim_card
    (
        CardKey,
        card1,
        card2,
        card3,
        card4,
        card5,
        card6
    )
    VALUES
    (
        0,
        NULL,
        NULL,
        NULL,
        'Unknown',
        NULL,
        'Unknown'
    );

    SET IDENTITY_INSERT dwh.dim_card OFF;
END;
GO

/* ============================================================
   3. DIM_IDENTITY
   ============================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM dwh.dim_identity
    WHERE IdentityKey = 0
)
BEGIN
    SET IDENTITY_INSERT dwh.dim_identity ON;

    INSERT INTO dwh.dim_identity
    (
        IdentityKey,
        id_01,
        id_02,
        id_03,
        id_04,
        id_05,
        id_06,
        id_07,
        id_08,
        id_09,
        id_10,
        id_11,
        id_12,
        id_13,
        id_14,
        id_15,
        id_16,
        id_17,
        id_18,
        id_19,
        id_20,
        id_21,
        id_22,
        id_23,
        id_24,
        id_25,
        id_26,
        id_27,
        id_28,
        id_29,
        id_30,
        id_31,
        id_32,
        id_33,
        id_34,
        id_35,
        id_36,
        id_37,
        id_38
    )
    VALUES
    (
        0,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    );

    SET IDENTITY_INSERT dwh.dim_identity OFF;
END;
GO

/* ============================================================
   4. DIM_DEVICE
   ============================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM dwh.dim_device
    WHERE DeviceKey = 0
)
BEGIN
    SET IDENTITY_INSERT dwh.dim_device ON;

    INSERT INTO dwh.dim_device
    (
        DeviceKey,
        DeviceType,
        DeviceInfo
    )
    VALUES
    (
        0,
        'Unknown',
        'Unknown'
    );

    SET IDENTITY_INSERT dwh.dim_device OFF;
END;
GO

/* ============================================================
   5. DIM_ADDRESS
   ============================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM dwh.dim_address
    WHERE AddressKey = 0
)
BEGIN
    SET IDENTITY_INSERT dwh.dim_address ON;

    INSERT INTO dwh.dim_address
    (
        AddressKey,
        addr1,
        addr2,
        dist1,
        dist2
    )
     VALUES
    (
        0,
        NULL,
        NULL,
        NULL,
        NULL
    );

    SET IDENTITY_INSERT dwh.dim_address OFF;
END;
GO