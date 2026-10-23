/*
    Fraud Analytics Platform
    Script: 10_load_dim_date.sql
    Objetivo: Carga da dimensão de datas do Data Warehouse
*/

USE FraudAnalytics;
GO

DECLARE @DataBase DATETIME2 = '2017-11-30T00:00:00';

INSERT INTO dwh.dim_date
(
    DateKey,
    FullDate,
    [Year],
    [Quarter],
    [Month],
    MonthName,
    [Day],
    DayOfWeek,
    DayName,
    IsWeekend
)
SELECT DISTINCT

    CONVERT(
        INT,
        CONVERT(
            VARCHAR(8),
            CAST(
                DATEADD(SECOND, t.TransactionDT, @DataBase)
                AS DATE
            ),
            112
        )
    ) AS DateKey,

    CAST(
        DATEADD(SECOND, t.TransactionDT, @DataBase)
        AS DATE
    ) AS FullDate,

    YEAR(
        DATEADD(SECOND, t.TransactionDT, @DataBase)
    ) AS [Year],

    DATEPART(
        QUARTER,
        DATEADD(SECOND, t.TransactionDT, @DataBase)
    ) AS [Quarter],

    MONTH(
        DATEADD(SECOND, t.TransactionDT, @DataBase)
    ) AS [Month],

    DATENAME(
        MONTH,
        DATEADD(SECOND, t.TransactionDT, @DataBase)
    ) AS MonthName,

    DAY(
        DATEADD(SECOND, t.TransactionDT, @DataBase)
    ) AS [Day],

    DATEPART(
        WEEKDAY,
        DATEADD(SECOND, t.TransactionDT, @DataBase)
    ) AS DayOfWeek,

    DATENAME(
        WEEKDAY,
        DATEADD(SECOND, t.TransactionDT, @DataBase)
    ) AS DayName,

    CASE
        WHEN DATEPART(
            WEEKDAY,
            DATEADD(SECOND, t.TransactionDT, @DataBase)
        ) IN (1, 7)
        THEN 1
        ELSE 0
    END AS IsWeekend

FROM ods.transactions t

WHERE t.TransactionDT IS NOT NULL

  AND NOT EXISTS
  (
      SELECT 1
      FROM dwh.dim_date d
      WHERE d.FullDate =
          CAST(
              DATEADD(
                  SECOND,
                  t.TransactionDT,
                  @DataBase
              ) AS DATE
          )
  );
GO