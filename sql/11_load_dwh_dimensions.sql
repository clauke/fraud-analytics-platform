/*
    Fraud Analytics Platform
    Script: 11_load_dwh_dimensions.sql
    Objetivo: Carga das dimensões do Data Warehouse
              a partir das tabelas da ODS.

    Dimensões carregadas:
        - dim_product
        - dim_card
        - dim_identity
        - dim_device
        - dim_address
*/

USE FraudAnalytics;
GO

/* ============================================================
   1. DIM_PRODUCT
   ============================================================ */

INSERT INTO dwh.dim_product
(
    ProductCD
)
SELECT DISTINCT
    t.ProductCD
FROM ods.transactions t
WHERE t.ProductCD IS NOT NULL
  AND NOT EXISTS
  (
    SELECT 1
    FROM dwh.dim_product d
    WHERE d.ProductCD = t.ProductCD
  );
GO

/* ============================================================
   2. DIM_CARD
   ============================================================ */

INSERT INTO dwh.dim_card
(
    card1,
    card2,
    card3,
    card4,
    card5,
    card6
)
SELECT DISTINCT
    t.card1,
    t.card2,
    t.card3,
    t.card4,
    t.card5,
    t.card6
FROM ods.transactions t
WHERE NOT EXISTS
(
    SELECT 1
    FROM dwh.dim_card d
    WHERE
        ISNULL(d.card1, -1) = ISNULL(t.card1, -1)
        AND ISNULL(d.card2, -1) = ISNULL(t.card2, -1)
        AND ISNULL(d.card3, -1) = ISNULL(t.card3, -1)
        AND ISNULL(d.card4, '') = ISNULL(t.card4, '')
        AND ISNULL(d.card5, -1) = ISNULL(t.card5, -1)
        AND ISNULL(d.card6, '') = ISNULL(t.card6, '')
);
GO

/* ============================================================
   3. DIM_IDENTITY
   ============================================================ */

INSERT INTO dwh.dim_identity
(
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
SELECT DISTINCT
    i.id_01,
    i.id_02,
    i.id_03,
    i.id_04,
    i.id_05,
    i.id_06,
    i.id_07,
    i.id_08,
    i.id_09,
    i.id_10,
    i.id_11,
    i.id_12,
    i.id_13,
    i.id_14,
    i.id_15,
    i.id_16,
    i.id_17,
    i.id_18,
    i.id_19,
    i.id_20,
    i.id_21,
    i.id_22,
    i.id_23,
    i.id_24,
    i.id_25,
    i.id_26,
    i.id_27,
    i.id_28,
    i.id_29,
    i.id_30,
    i.id_31,
    i.id_32,
    i.id_33,
    i.id_34,
    i.id_35,
    i.id_36,
    i.id_37,
    i.id_38
FROM ods.identities i
WHERE NOT EXISTS
(
    SELECT 1
    FROM dwh.dim_identity d
    WHERE
        ISNULL(d.id_01, -1) = ISNULL(i.id_01, -1)
        AND ISNULL(d.id_02, -1) = ISNULL(i.id_02, -1)
        AND ISNULL(d.id_03, -1) = ISNULL(i.id_03, -1)
        AND ISNULL(d.id_04, -1) = ISNULL(i.id_04, -1)
        AND ISNULL(d.id_05, -1) = ISNULL(i.id_05, -1)
        AND ISNULL(d.id_06, -1) = ISNULL(i.id_06, -1)
        AND ISNULL(d.id_07, -1) = ISNULL(i.id_07, -1)
        AND ISNULL(d.id_08, -1) = ISNULL(i.id_08, -1)
        AND ISNULL(d.id_09, -1) = ISNULL(i.id_09, -1)
        AND ISNULL(d.id_10, -1) = ISNULL(i.id_10, -1)
        AND ISNULL(d.id_11, -1) = ISNULL(i.id_11, -1)
        AND ISNULL(d.id_12, -1) = ISNULL(i.id_12, -1)
        AND ISNULL(d.id_13, -1) = ISNULL(i.id_13, -1)
        AND ISNULL(d.id_14, -1) = ISNULL(i.id_14, -1)
        AND ISNULL(d.id_15, -1) = ISNULL(i.id_15, -1)
        AND ISNULL(d.id_16, -1) = ISNULL(i.id_16, -1)
        AND ISNULL(d.id_17, -1) = ISNULL(i.id_17, -1)
        AND ISNULL(d.id_18, -1) = ISNULL(i.id_18, -1)
        AND ISNULL(d.id_19, -1) = ISNULL(i.id_19, -1)
        AND ISNULL(d.id_20, -1) = ISNULL(i.id_20, -1)
        AND ISNULL(d.id_21, -1) = ISNULL(i.id_21, -1)
        AND ISNULL(d.id_22, -1) = ISNULL(i.id_22, -1)
        AND ISNULL(d.id_23, -1) = ISNULL(i.id_23, -1)
        AND ISNULL(d.id_24, -1) = ISNULL(i.id_24, -1)
        AND ISNULL(d.id_25, -1) = ISNULL(i.id_25, -1)
        AND ISNULL(d.id_26, -1) = ISNULL(i.id_26, -1)
        AND ISNULL(d.id_27, -1) = ISNULL(i.id_27, -1)
        AND ISNULL(d.id_28, -1) = ISNULL(i.id_28, -1)
        AND ISNULL(d.id_29, -1) = ISNULL(i.id_29, -1)
        AND ISNULL(d.id_30, -1) = ISNULL(i.id_30, -1)
        AND ISNULL(d.id_31, -1) = ISNULL(i.id_31, -1)
        AND ISNULL(d.id_32, -1) = ISNULL(i.id_32, -1)
        AND ISNULL(d.id_33, -1) = ISNULL(i.id_33, -1)
        AND ISNULL(d.id_34, -1) = ISNULL(i.id_34, -1)
        AND ISNULL(d.id_35, -1) = ISNULL(i.id_35, -1)
        AND ISNULL(d.id_36, -1) = ISNULL(i.id_36, -1)
        AND ISNULL(d.id_37, -1) = ISNULL(i.id_37, -1)
        AND ISNULL(d.id_38, -1) = ISNULL(i.id_38, -1)
);
GO

/* ============================================================
   4. DIM_DEVICE
   ============================================================ */

INSERT INTO dwh.dim_device
(
    DeviceType,
    DeviceInfo
)
SELECT DISTINCT
    i.DeviceType,
    i.DeviceInfo
FROM ods.identities i
WHERE NOT EXISTS
(
    SELECT 1
    FROM dwh.dim_device d
    WHERE
        ISNULL(d.DeviceType, '') = ISNULL(i.DeviceType, '')
        AND ISNULL(d.DeviceInfo, '') = ISNULL(i.DeviceInfo, '')
);
GO

/* ============================================================
   5. DIM_ADDRESS
   ============================================================ */

INSERT INTO dwh.dim_address
(
    addr1,
    addr2,
    dist1,
    dist2
)
SELECT DISTINCT
    t.addr1,
    t.addr2,
    t.dist1,
    t.dist2
FROM ods.transactions t
WHERE NOT EXISTS
(
    SELECT 1
    FROM dwh.dim_address d
    WHERE
        ISNULL(d.addr1, -1) = ISNULL(t.addr1, -1)
        AND ISNULL(d.addr2, -1) = ISNULL(t.addr2, -1)
        AND ISNULL(d.dist1, -1) = ISNULL(t.dist1, -1)
        AND ISNULL(d.dist2, -1) = ISNULL(t.dist2, -1)
);
GO