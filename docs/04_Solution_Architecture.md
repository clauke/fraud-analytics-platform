# Solution Architecture

**Projeto:** Fraud Analytics Platform

**Versão:** 0.1

**Status:** Em desenvolvimento

---

# 1. Objetivo

Este documento apresenta a arquitetura da solução proposta para a **Fraud Analytics Platform**, descrevendo seus principais componentes, o fluxo de dados e as tecnologias utilizadas.

A arquitetura foi concebida para representar uma solução corporativa de dados utilizando exclusivamente ferramentas gratuitas, abrangendo processos de Engenharia de Dados, Data Science, Business Intelligence, Inteligência Artificial Generativa e Cloud.

---

# 2. Visão Geral da Arquitetura

A plataforma foi estruturada em camadas, separando claramente as responsabilidades de ingestão, armazenamento, transformação, modelagem analítica e consumo dos dados.

Essa abordagem favorece a organização do projeto, facilita sua manutenção e aproxima a solução de arquiteturas adotadas em ambientes corporativos.

---

# 3. Arquitetura da Solução

```text
                    IEEE-CIS Fraud Detection
                           (CSV Files)
                                │
                                ▼
                        RAW (data/raw)
                                │
                                ▼
            Python - Ingestion & Data Validation
                                │
                                ▼
                SQL Server Express - STAGING
                                │
                                ▼
                 SSIS - ETL & Data Integration
                                │
                                ▼
             ODS (Operational Data Store)
                                │
                                ▼
            Data Warehouse (Dimensional Model)
                     │                    │
                     │                    │
                     ▼                    ▼
            Machine Learning        Power BI
               (Python)            Dashboards
                     │
                     ▼
        IA Generativa (Ollama)
                     │
                     ▼
           BigQuery Sandbox (Cloud)
```

---

# 4. Fluxo dos Dados

O fluxo da plataforma será composto pelas seguintes etapas:

1. Os arquivos originais do dataset serão armazenados na camada **Raw**, preservando sua estrutura original.

2. Scripts em **Python** realizarão a ingestão dos dados, validações iniciais, limpeza básica e carregamento para o banco de dados.

3. O **SQL Server Express** será utilizado como ambiente de **Staging**, armazenando os dados antes das transformações analíticas.

4. Os processos de **ETL**, implementados com **SQL Server Integration Services (SSIS)**, serão responsáveis pela padronização, integração e movimentação dos dados para o **Operational Data Store (ODS)**.

5. A partir do ODS, os dados serão organizados em um **Data Warehouse** utilizando modelagem dimensional, facilitando consultas analíticas.

6. O **Data Warehouse** servirá como fonte para os modelos de **Machine Learning** desenvolvidos em Python e para os dashboards construídos no **Power BI**.

7. Os resultados dos modelos poderão ser interpretados por meio da integração com **Ollama**, utilizando Inteligência Artificial Generativa para produzir explicações em linguagem natural.

8. Como demonstração de integração com ambientes em nuvem, parte dos dados tratados será disponibilizada no **BigQuery Sandbox**.

---

# 5. Componentes da Solução

| Componente           | Responsabilidade                                                           |
| -------------------- | -------------------------------------------------------------------------- |
| Raw                  | Armazenar os arquivos originais do dataset.                                |
| Python               | Ingestão, validação e preparação inicial dos dados.                        |
| SQL Server (Staging) | Persistência dos dados antes das transformações.                           |
| SSIS                 | Execução dos processos de ETL e integração entre as camadas.               |
| ODS                  | Armazenamento dos dados padronizados para consumo analítico.               |
| Data Warehouse       | Organização dos dados em modelo dimensional.                               |
| Machine Learning     | Desenvolvimento e avaliação dos modelos preditivos.                        |
| Power BI             | Construção de dashboards e indicadores.                                    |
| Ollama               | Geração de explicações em linguagem natural sobre os resultados do modelo. |
| BigQuery Sandbox     | Demonstração de integração com ambiente cloud.                             |

---

# 6. Tecnologias Utilizadas

| Área                        | Tecnologia                             |
| --------------------------- | -------------------------------------- |
| Linguagem                   | Python                                 |
| Banco de Dados              | SQL Server                     |
| ETL                         | SQL Server Integration Services (SSIS) |
| Consultas                   | SQL (T-SQL)                            |
| Machine Learning            | Scikit-learn                           |
| Business Intelligence       | Power BI Desktop                       |
| IA Generativa               | Ollama                                 |
| Cloud                       | BigQuery Sandbox                       |
| Versionamento               | Git e GitHub                           |
| Ambiente de Desenvolvimento | Visual Studio Code e Jupyter Notebook  |

---

# 7. Justificativa da Arquitetura

A arquitetura proposta busca reproduzir um fluxo de dados semelhante ao encontrado em ambientes corporativos, mantendo um equilíbrio entre boas práticas de Engenharia de Dados e a viabilidade de implementação utilizando ferramentas gratuitas.

A separação em camadas permite isolar responsabilidades, melhorar a organização do projeto e facilitar futuras evoluções, como a substituição de componentes ou a inclusão de novas fontes de dados.

---

# 8. Benefícios da Arquitetura

A arquitetura adotada oferece os seguintes benefícios:

* Separação clara das responsabilidades entre as camadas da solução.
* Facilidade de manutenção e evolução do projeto.
* Organização do fluxo de dados desde a ingestão até o consumo analítico.
* Integração entre Engenharia de Dados, Data Science e Business Intelligence.
* Utilização de ferramentas amplamente empregadas no mercado.
* Estrutura adequada para fins de estudo, demonstração técnica e composição de portfólio.
