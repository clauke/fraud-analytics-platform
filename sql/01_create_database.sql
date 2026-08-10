```sql
/*
===============================================================================
Projeto: Fraud Analytics Platform
Arquivo: 01_create_database.sql
Objetivo: Criação do banco de dados e schemas da plataforma
Banco: SQL Server
Versão: 0.1
===============================================================================
*/

USE master;
GO

/* ============================================================================
   1. CRIAÇÃO DO BANCO DE DADOS
   ============================================================================ */

IF DB_ID('FraudAnalytics') IS NULL
BEGIN
    CREATE DATABASE FraudAnalytics;
END;
GO

/* ============================================================================
   2. UTILIZAÇÃO DO BANCO
   ============================================================================ */

USE FraudAnalytics;
GO

/* ============================================================================
   3. CRIAÇÃO DOS SCHEMAS
   ============================================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'raw'
)
BEGIN
    EXEC('CREATE SCHEMA raw');
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'stg'
)
BEGIN
    EXEC('CREATE SCHEMA stg');
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'ods'
)
BEGIN
    EXEC('CREATE SCHEMA ods');
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'dw'
)
BEGIN
    EXEC('CREATE SCHEMA dw');
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = 'audit'
)
BEGIN
    EXEC('CREATE SCHEMA audit');
END;
GO

/* ============================================================================
   4. VALIDAÇÃO DA ESTRUTURA
   ============================================================================ */

SELECT
    name AS schema_name
FROM sys.schemas
WHERE name IN ('raw', 'stg', 'ods', 'dw', 'audit')
ORDER BY name;
GO

/* ============================================================================
   FIM DO SCRIPT
   ============================================================================ */
```
