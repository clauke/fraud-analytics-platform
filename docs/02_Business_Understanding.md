# Business Understanding

**Projeto:** Fraud Analytics Platform

**Subtítulo:** End-to-End Data Platform for Fraud Detection and Business Intelligence

**Versão:** 0.1
**Status:** Em desenvolvimento

---

# 1. Introdução

Este documento apresenta o entendimento do problema de negócio que motivou o desenvolvimento da **Fraud Analytics Platform**.

Seu objetivo é definir o contexto organizacional, o problema de negócio, os objetivos estratégicos e analíticos, além dos indicadores que orientarão o desenvolvimento da solução.

As definições apresentadas servirão como referência para todas as etapas do projeto, desde a engenharia de dados até a construção dos modelos de Machine Learning e dashboards executivos.

---

# 2. Contexto de Negócio

A **FinTrust Bank** é uma fintech fictícia que oferece serviços de pagamentos digitais aos seus clientes. Com o crescimento do volume de transações eletrônicas, a instituição passou a registrar um aumento nas tentativas de fraude durante o processo de autorização de pagamentos.

O processo atual baseia-se principalmente em regras de negócio e análises manuais, dificultando a identificação rápida de transações suspeitas e aumentando o risco de perdas financeiras e do bloqueio indevido de operações legítimas.

Para apoiar a equipe de prevenção à fraude, a empresa decidiu investir em uma plataforma analítica capaz de integrar dados, automatizar processos e fornecer informações confiáveis para suporte à tomada de decisão.

---

# 3. Problema de Negócio

A FinTrust Bank necessita de uma solução que permita identificar transações eletrônicas potencialmente fraudulentas de forma mais eficiente, reduzindo perdas financeiras e auxiliando os analistas de risco na priorização das investigações.

Além da classificação das transações, a organização precisa acompanhar indicadores operacionais e analíticos que permitam avaliar continuamente o desempenho da operação de prevenção à fraude.

---

# 4. Objetivos Estratégicos

* Reduzir perdas associadas a fraudes em transações eletrônicas.
* Apoiar a equipe de prevenção à fraude na priorização das análises.
* Disponibilizar indicadores confiáveis para acompanhamento da operação.
* Construir uma plataforma analítica utilizando tecnologias gratuitas amplamente adotadas pelo mercado.

---

# 5. Objetivos Analíticos

A plataforma deverá permitir:

* realizar a ingestão e preparação dos dados;
* aplicar processos de limpeza e transformação;
* armazenar os dados em um ambiente analítico estruturado;
* identificar padrões associados às transações fraudulentas;
* desenvolver um modelo de Machine Learning para classificação de transações;
* disponibilizar dashboards para acompanhamento dos principais indicadores.

---

# 6. Perguntas de Negócio

A plataforma deverá apoiar respostas para as seguintes questões:

* Qual é a proporção de transações fraudulentas em relação ao total processado?
* Quais atributos apresentam maior associação com fraudes?
* Quais variáveis possuem maior importância para o modelo preditivo?
* Como evoluem os indicadores de desempenho do modelo ao longo do tempo?
* Como priorizar transações suspeitas para investigação?

---

# 7. Indicadores de Sucesso (KPIs)

## Indicadores de Negócio

* Taxa de transações fraudulentas.
* Percentual de transações classificadas como suspeitas.

## Indicadores do Modelo

* Precision.
* Recall.
* F1-Score.
* ROC-AUC.

## Indicadores da Plataforma

* Quantidade de registros processados.
* Percentual de registros válidos após o ETL.
* Tempo de execução do pipeline de processamento.

---

# 8. Benefícios Esperados

Com a implantação da plataforma, espera-se:

* melhorar a identificação de transações potencialmente fraudulentas;
* reduzir o esforço necessário para análise manual;
* disponibilizar informações confiáveis para apoio à tomada de decisão;
* padronizar o processo de preparação e análise dos dados;
* demonstrar uma arquitetura completa de Engenharia de Dados, Analytics e Data Science.

---

# 9. Premissas

* O dataset IEEE-CIS Fraud Detection representa adequadamente um cenário de transações eletrônicas com ocorrência de fraudes.
* As ferramentas gratuitas selecionadas são suficientes para demonstrar uma arquitetura corporativa de dados.
* O processamento será realizado em ambiente local durante o desenvolvimento do projeto.

---

# 10. Restrições

* Utilização exclusiva de ferramentas gratuitas.
* Ausência de integração com sistemas bancários reais.
* Processamento em lote (batch), sem análise em tempo real.
* Utilização de dados públicos para fins educacionais e de demonstração.

---

# 11. Critérios de Sucesso

O projeto será considerado bem-sucedido quando demonstrar um fluxo completo de dados, desde a ingestão até a geração de informações para apoio à tomada de decisão, incluindo:

* pipeline de ETL implementado;
* armazenamento estruturado dos dados;
* modelo de Machine Learning treinado e avaliado;
* dashboards em Power BI com indicadores relevantes;
* documentação técnica completa e organizada no GitHub.
