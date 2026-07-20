# Project Roadmap

**Projeto:** Fraud Analytics Platform

**Versão:** 0.1

**Status:** Em desenvolvimento

---

# 1. Objetivo

Este documento apresenta o planejamento macro do projeto **Fraud Analytics Platform**, descrevendo as principais etapas de desenvolvimento, seus objetivos e entregáveis.

O roadmap servirá como guia para acompanhar a evolução do projeto durante todas as sprints.

---

# 2. Roadmap do Projeto

## Sprint 1 – Planejamento e Documentação

### Objetivo

Definir o contexto do projeto, o problema de negócio, a arquitetura da solução e os requisitos iniciais.

### Entregáveis

* Project Charter
* Business Understanding
* Project Roadmap
* Solution Architecture
* Requirements

---

## Sprint 2 – Data Understanding

### Objetivo

Compreender o dataset, avaliar sua qualidade e identificar oportunidades para análise.

### Entregáveis

* Data Profiling
* Data Dictionary
* Data Quality Report
* Análise Exploratória Inicial

---

## Sprint 3 – Engenharia de Dados (ETL)

### Objetivo

Construir o pipeline de ingestão, limpeza e transformação dos dados.

### Entregáveis

* Pipeline em Python
* Processos de limpeza
* Padronização dos dados
* Carga para SQL Server
* Pipeline automatizado com SSIS

---

## Sprint 4 – Modelagem de Dados e Data Warehouse

### Objetivo

Estruturar o ambiente analítico para consultas e visualizações.

### Entregáveis

* Modelo dimensional
* Tabelas Fato e Dimensão
* Scripts SQL
* Data Warehouse

---

## Sprint 5 – Machine Learning

### Objetivo

Desenvolver e avaliar modelos para classificação de transações fraudulentas.

### Entregáveis

* Engenharia de atributos
* Treinamento dos modelos
* Avaliação de desempenho
* Seleção do modelo final

---

## Sprint 6 – Business Intelligence

### Objetivo

Construir dashboards para acompanhamento dos indicadores operacionais e analíticos.

### Entregáveis

* Modelo semântico
* Medidas DAX
* Dashboards em Power BI
* KPIs

---

## Sprint 7 – IA Generativa e Cloud

### Objetivo

Complementar a solução com recursos de Inteligência Artificial Generativa e armazenamento em nuvem.

### Entregáveis

* Integração com Ollama
* Explicações em linguagem natural
* Publicação de dados no BigQuery Sandbox
* Validação da arquitetura completa

---

## Sprint 8 – Documentação Final e Encerramento

### Objetivo

Consolidar toda a documentação técnica e preparar o projeto para publicação.

### Entregáveis

* Atualização do README
* Revisão da documentação
* Organização do repositório
* Evidências do projeto
* Apresentação final

---

# 3. Tecnologias Utilizadas

| Área                        | Tecnologia                            |
| --------------------------- | ------------------------------------- |
| Linguagem                   | Python                                |
| Banco de Dados              | SQL Server                    |
| ETL                         | SSIS                                  |
| Consultas                   | SQL (T-SQL)                           |
| Machine Learning            | Scikit-learn                          |
| IA Generativa               | Ollama                                |
| Business Intelligence       | Power BI Desktop                      |
| Cloud                       | BigQuery Sandbox                      |
| Versionamento               | Git e GitHub                          |
| Ambiente de Desenvolvimento | Visual Studio Code e Jupyter Notebook |

---

# 4. Critérios de Conclusão

O projeto será considerado concluído quando todas as sprints forem finalizadas e a plataforma demonstrar um fluxo completo de dados, desde a ingestão até a disponibilização de análises, modelos preditivos e dashboards, acompanhados de documentação técnica organizada e versionada.