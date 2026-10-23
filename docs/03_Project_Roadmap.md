# Project Roadmap

**Projeto:** Fraud Analytics Platform  
**Versão:** 0.2  
**Status:** Em desenvolvimento

---

## 1. Objetivo

Este documento apresenta o planejamento macro do projeto **Fraud Analytics Platform**, descrevendo as principais etapas de desenvolvimento, seus objetivos e entregáveis.

O roadmap é atualizado conforme a evolução real do projeto, mantendo a rastreabilidade entre as atividades executadas, a documentação e as próximas etapas.

---

## 2. Roadmap do Projeto

## Sprint 1 – Planejamento e Documentação

### Objetivo

Definir o contexto do projeto, o problema de negócio, a arquitetura da solução e os requisitos iniciais.

### Entregáveis

- Project Charter
- Business Understanding
- Project Roadmap
- Solution Architecture
- Requirements

---

## Sprint 2 – Data Understanding

### Objetivo

Compreender o dataset, avaliar sua qualidade e identificar oportunidades para análise.

### Entregáveis

- Data Profiling
- Data Dictionary
- Data Quality Report
- Análise Exploratória Inicial

---

## Sprint 3 – Engenharia de Dados e ETL

### Objetivo

Construir os processos de ingestão, limpeza, transformação e organização dos dados nas camadas iniciais da arquitetura.

### Entregáveis

- Scripts Python para processamento dos dados
- Processos de limpeza e padronização
- Carga de dados entre as camadas RAW, STG e ODS
- Scripts SQL associados aos processos de carga
- Documentação do desenho do ETL

---

## Sprint 4 – Modelagem e Preparação do Data Warehouse

### Objetivo

Definir a estrutura analítica e preparar a modelagem dimensional para suportar consultas e análises de transações financeiras.

### Entregáveis

- Modelo físico de dados
- Modelo dimensional
- Definição das tabelas fato e dimensão
- Dicionário e documentação dos modelos
- Scripts SQL necessários à implementação

---

## Sprint 5 – Implementação do Data Warehouse e Integração SSIS

### Objetivo

Implementar e validar o Data Warehouse, integrando os processos de carga em um pipeline automatizado.

### Entregáveis

- Criação e carga das dimensões
- Criação e carga da tabela fato
- Procedures SQL para carga do DWH
- Pacote SSIS para integração das etapas STG → ODS → DWH
- Integração do script Python de carga ODS
- Restrições de precedência e controle de execução
- Validações de integridade referencial e consistência dos dados
- Documentação do pipeline SSIS

### Critérios de conclusão

- Execução integrada do pacote SSIS concluída com sucesso.
- Integridade dos dados validada.
- Regras de qualidade verificadas.
- Procedures e pacote documentados e versionados.

---

## Sprint 6 – Machine Learning

### Objetivo

Desenvolver, treinar e avaliar modelos de Machine Learning para classificação de transações fraudulentas, utilizando os dados disponíveis na plataforma.

### Entregáveis

- Definição da variável-alvo e dos atributos
- Análise exploratória direcionada à modelagem
- Engenharia de atributos
- Preparação dos dados para treinamento
- Pipeline de pré-processamento
- Treinamento de modelo baseline
- Avaliação comparativa de modelos
- Análise de métricas de classificação
- Seleção justificada do modelo final
- Persistência dos artefatos e documentação dos resultados

### Critérios de conclusão

- Variável-alvo e atributos validados.
- Estratégia de treinamento e avaliação documentada.
- Vazamento de dados evitado.
- Modelos avaliados com métricas adequadas à detecção de fraudes.
- Seleção do modelo final justificada pelos resultados.
- Código, artefatos e documentação organizados e versionados conforme os padrões do projeto.

---

## Sprint 7 – Business Intelligence

### Objetivo

Construir dashboards para acompanhamento dos indicadores operacionais e analíticos, utilizando os dados do Data Warehouse e os resultados de Machine Learning quando aplicável.

### Entregáveis

- Modelo semântico
- Medidas DAX
- KPIs operacionais e analíticos
- Dashboards em Power BI
- Análise de indicadores de fraude
- Documentação das visualizações e métricas

---

## Sprint 8 – IA Generativa e Cloud

### Objetivo

Complementar a plataforma com recursos de Inteligência Artificial Generativa e explorar a disponibilização de dados em ambiente de nuvem.

### Entregáveis

- Integração com Ollama
- Geração de explicações em linguagem natural
- Exploração de casos de uso para interpretação dos resultados de fraude
- Publicação de dados selecionados no BigQuery Sandbox
- Validação da arquitetura integrada
- Documentação técnica das integrações

---

## Sprint 9 – Documentação Final e Encerramento

### Objetivo

Consolidar a documentação técnica, revisar os componentes da plataforma e preparar o projeto para apresentação e publicação no portfólio.

### Entregáveis

- Atualização do README
- Revisão da documentação
- Organização final do repositório
- Revisão dos scripts, testes e configurações
- Evidências das principais etapas
- Apresentação da arquitetura e dos resultados
- Registro das limitações e oportunidades de evolução

---

## 3. Tecnologias Utilizadas

| Área | Tecnologia |
|---|---|
| Linguagem | Python |
| Banco de Dados | SQL Server |
| ETL e Integração | Python e SSIS |
| Consultas | SQL (T-SQL) |
| Machine Learning | Scikit-learn |
| Análise de Dados | pandas e NumPy |
| Visualização | Matplotlib e Power BI |
| IA Generativa | Ollama |
| Cloud | BigQuery Sandbox |
| Versionamento | Git e GitHub |
| Ambiente de Desenvolvimento | Visual Studio Code e Jupyter Notebook |

---

## 4. Critérios de Conclusão do Projeto

O projeto será considerado concluído quando todas as sprints forem finalizadas e a plataforma demonstrar um fluxo integrado de dados, desde a ingestão até a disponibilização de análises, modelos preditivos, dashboards e recursos complementares de IA.

A solução deverá possuir:

- Pipeline de dados documentado e validado.
- Data Warehouse implementado e consistente.
- Modelo de Machine Learning treinado e avaliado.
- Dashboards e indicadores analíticos.
- Integrações complementares documentadas.
- Código e documentação organizados e versionados.
- Evidências que permitam compreender e reproduzir as principais etapas do projeto.

---

## 5. Controle de Versão do Documento

| Versão | Descrição |
|---|---|
| 0.1 | Roadmap inicial do projeto |
| 0.2 | Atualização do sequenciamento das sprints para refletir a implementação do Data Warehouse na Sprint 5 e o planejamento de Machine Learning na Sprint 6 |

