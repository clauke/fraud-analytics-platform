USE FraudAnalytics;
GO

CREATE OR ALTER PROCEDURE dwh.usp_load_fact_transaction
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dwh.fact_transaction
    (
        TransactionID,
        DateKey,
        ProductKey,
        CardKey,
        IdentityKey,
        DeviceKey,
        AddressKey,
        TransactionDT,
        TransactionAmt,
        isFraud,
        source_file,
        batch_id,
        load_date,
        etl_status
    )
    SELECT
        t.TransactionID,

        COALESCE(d.DateKey, 0) AS DateKey,

        COALESCE(p.ProductKey, 0) AS ProductKey,

        COALESCE(c.CardKey, 0) AS CardKey,

        COALESCE(i.IdentityKey, 0) AS IdentityKey,

        COALESCE(dv.DeviceKey, 0) AS DeviceKey,

        COALESCE(a.AddressKey, 0) AS AddressKey,

        t.TransactionDT,
        t.TransactionAmt,
        t.isFraud,
        t.source_file,
        t.batch_id,
        t.load_date,
        t.etl_status

    FROM ods.transactions t

    LEFT JOIN dwh.dim_date d
        ON d.FullDate = CAST(
            DATEADD(
                SECOND,
                t.TransactionDT,
                CAST(DATEFROMPARTS(2017, 11, 30) AS datetime2)
            ) AS date
        )

    LEFT JOIN dwh.dim_product p
        ON p.ProductCD = t.ProductCD

    LEFT JOIN dwh.dim_card c
        ON ISNULL(c.card1, -1) = ISNULL(t.card1, -1)
        AND ISNULL(c.card2, -1) = ISNULL(t.card2, -1)
        AND ISNULL(c.card3, -1) = ISNULL(t.card3, -1)
        AND ISNULL(c.card4, 'Unknown') = ISNULL(t.card4, 'Unknown')
        AND ISNULL(c.card5, -1) = ISNULL(t.card5, -1)
        AND ISNULL(c.card6, 'Unknown') = ISNULL(t.card6, 'Unknown')

    LEFT JOIN ods.identities oi
        ON oi.TransactionID = t.TransactionID

    LEFT JOIN dwh.dim_identity i
        ON ISNULL(i.id_01, -1) = ISNULL(oi.id_01, -1)
        AND ISNULL(i.id_02, -1) = ISNULL(oi.id_02, -1)
        AND ISNULL(i.id_03, -1) = ISNULL(oi.id_03, -1)
        AND ISNULL(i.id_04, -1) = ISNULL(oi.id_04, -1)
        AND ISNULL(i.id_05, -1) = ISNULL(oi.id_05, -1)
        AND ISNULL(i.id_06, -1) = ISNULL(oi.id_06, -1)
        AND ISNULL(i.id_07, -1) = ISNULL(oi.id_07, -1)
        AND ISNULL(i.id_08, -1) = ISNULL(oi.id_08, -1)
        AND ISNULL(i.id_09, -1) = ISNULL(oi.id_09, -1)
        AND ISNULL(i.id_10, -1) = ISNULL(oi.id_10, -1)
        AND ISNULL(i.id_11, -1) = ISNULL(oi.id_11, -1)
        AND ISNULL(i.id_12, 'Unknown') = ISNULL(oi.id_12, 'Unknown')
        AND ISNULL(i.id_13, -1) = ISNULL(oi.id_13, -1)
        AND ISNULL(i.id_14, -1) = ISNULL(oi.id_14, -1)
        AND ISNULL(i.id_15, 'Unknown') = ISNULL(oi.id_15, 'Unknown')
        AND ISNULL(i.id_16, 'Unknown') = ISNULL(oi.id_16, 'Unknown')
        AND ISNULL(i.id_17, -1) = ISNULL(oi.id_17, -1)
        AND ISNULL(i.id_18, -1) = ISNULL(oi.id_18, -1)
        AND ISNULL(i.id_19, -1) = ISNULL(oi.id_19, -1)
        AND ISNULL(i.id_20, -1) = ISNULL(oi.id_20, -1)
        AND ISNULL(i.id_21, -1) = ISNULL(oi.id_21, -1)
        AND ISNULL(i.id_22, -1) = ISNULL(oi.id_22, -1)
        AND ISNULL(i.id_23, 'Unknown') = ISNULL(oi.id_23, 'Unknown')
        AND ISNULL(i.id_24, -1) = ISNULL(oi.id_24, -1)
        AND ISNULL(i.id_25, -1) = ISNULL(oi.id_25, -1)
        AND ISNULL(i.id_26, -1) = ISNULL(oi.id_26, -1)
        AND ISNULL(i.id_27, 'Unknown') = ISNULL(oi.id_27, 'Unknown')
        AND ISNULL(i.id_28, 'Unknown') = ISNULL(oi.id_28, 'Unknown')
        AND ISNULL(i.id_29, 'Unknown') = ISNULL(oi.id_29, 'Unknown')
        AND ISNULL(i.id_30, 'Unknown') = ISNULL(oi.id_30, 'Unknown')
        AND ISNULL(i.id_31, 'Unknown') = ISNULL(oi.id_31, 'Unknown')
        AND ISNULL(i.id_32, -1) = ISNULL(oi.id_32, -1)
        AND ISNULL(i.id_33, 'Unknown') = ISNULL(oi.id_33, 'Unknown')
        AND ISNULL(i.id_34, 'Unknown') = ISNULL(oi.id_34, 'Unknown')
        AND ISNULL(i.id_35, 'Unknown') = ISNULL(oi.id_35, 'Unknown')
        AND ISNULL(i.id_36, 'Unknown') = ISNULL(oi.id_36, 'Unknown')
        AND ISNULL(i.id_37, 'Unknown') = ISNULL(oi.id_37, 'Unknown')
        AND ISNULL(i.id_38, 'Unknown') = ISNULL(oi.id_38, 'Unknown')

    LEFT JOIN dwh.dim_device dv
        ON ISNULL(dv.DeviceType, 'Unknown') =
           ISNULL(oi.DeviceType, 'Unknown')
        AND ISNULL(dv.DeviceInfo, 'Unknown') =
            ISNULL(oi.DeviceInfo, 'Unknown')

    LEFT JOIN dwh.dim_address a
        ON ISNULL(a.addr1, -1) = ISNULL(t.addr1, -1)
        AND ISNULL(a.addr2, -1) = ISNULL(t.addr2, -1)
        AND ISNULL(a.dist1, -1) = ISNULL(t.dist1, -1)
        AND ISNULL(a.dist2, -1) = ISNULL(t.dist2, -1)

    WHERE NOT EXISTS
    (
        SELECT 1
        FROM dwh.fact_transaction f
        WHERE f.TransactionID = t.TransactionID
    );
END;
GO