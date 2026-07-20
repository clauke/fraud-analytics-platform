# Requirements

**Projeto:** Fraud Analytics Platform

**Versão:** 0.1

**Status:** Em desenvolvimento

---

# 1. Objetivo

Este documento define os requisitos da **Fraud Analytics Platform**, estabelecendo as principais funcionalidades esperadas e as características técnicas que orientarão o desenvolvimento da solução.

Os requisitos apresentados refletem o escopo definido para este projeto e servirão como referência durante todas as etapas de implementação.

---

# 2. Requisitos Funcionais

A plataforma deverá ser capaz de:

### RF01 – Ingestão de Dados

Importar os arquivos originais do dataset IEEE-CIS Fraud Detection para processamento.

---

### RF02 – Validação dos Dados

Realizar verificações básicas de qualidade, incluindo estrutura, tipos de dados e valores ausentes.

---

### RF03 – Processo de ETL

Executar processos de extração, transformação e carga utilizando Python e SSIS.

---

### RF04 – Armazenamento

Persistir os dados nas camadas Staging, ODS e Data Warehouse utilizando SQL Server.

---

### RF05 – Modelagem Analítica

Disponibilizar um modelo dimensional para consultas analíticas.

---

### RF06 – Machine Learning

Treinar e avaliar modelos de classificação para identificação de transações potencialmente fraudulentas.

---

### RF07 – Dashboards

Disponibilizar indicadores e visualizações em Power BI.

---

### RF08 – Inteligência Artificial Generativa

Gerar explicações em linguagem natural para apoiar a interpretação dos resultados do modelo utilizando Ollama.

---

### RF09 – Integração com Cloud

Publicar dados selecionados no BigQuery Sandbox para demonstrar integração com ambiente em nuvem.

---

### RF10 – Versionamento

Manter todo o código-fonte e a documentação versionados em GitHub.

---

# 3. Requisitos Não Funcionais

### RNF01

Utilizar exclusivamente ferramentas gratuitas.

---

### RNF02

Manter organização em arquitetura de dados por camadas.

---

### RNF03

Documentar todas as etapas do projeto.

---

### RNF04

Utilizar boas práticas de programação e versionamento.

---

### RNF05

Permitir a reprodução completa do projeto a partir da documentação disponível.

---

# 4. Premissas

* O dataset será utilizado exclusivamente para fins educacionais e de demonstração.
* O desenvolvimento ocorrerá em ambiente local.
* As tecnologias escolhidas permanecerão as mesmas durante o projeto, salvo necessidade técnica justificada.

---

# 5. Critérios de Aceitação

O projeto atenderá aos requisitos quando demonstrar:

* ingestão e processamento dos dados;
* pipeline de ETL funcional;
* armazenamento estruturado nas camadas propostas;
* modelo de Machine Learning treinado e avaliado;
* dashboards desenvolvidos em Power BI;
* integração com IA Generativa;
* integração demonstrativa com ambiente cloud;
* documentação técnica organizada e atualizada;
* código-fonte versionado no GitHub.
