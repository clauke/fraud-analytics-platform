/*
    Fraud Analytics Platform
    Script: 06_create_dwh_schema.sql
    Objetivo: Criação do schema Data Warehouse (DWH)
*/

USE FraudAnalytics;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'dwh'
)
BEGIN
    EXEC('CREATE SCHEMA dwh');
END;
GO