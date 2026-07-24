# Data Profiling Report

**Projeto:** Fraud Analytics Platform

**Documento:** 06_Data_Profiling_Report.md

**Versão:** 0.1

**Status:** Concluído

---

# 1. Objetivo

Este relatório apresenta os resultados da etapa de **Data Profiling** realizada sobre o dataset **IEEE-CIS Fraud Detection**.

O objetivo foi compreender a estrutura dos dados, avaliar sua qualidade e identificar características relevantes para orientar o desenvolvimento do pipeline de ETL, dos modelos de Machine Learning e dos dashboards analíticos.

---

# 2. Metodologia

A análise foi conduzida por meio do notebook **01_Data_Profiling.ipynb**, utilizando Python e a biblioteca Pandas.

Foram avaliados:

* estrutura dos arquivos;
* quantidade de registros e colunas;
* tipos de dados;
* consumo de memória;
* valores ausentes;
* registros duplicados;
* cardinalidade das variáveis;
* colunas constantes;
* estatísticas descritivas;
* distribuição da variável alvo (`isFraud`);
* relacionamento entre os arquivos do dataset.

---

# 3. Visão Geral do Dataset

O dataset é composto por cinco arquivos:

| Arquivo               | Finalidade                                                              |
| --------------------- | ----------------------------------------------------------------------- |
| train_transaction.csv | Transações utilizadas para treinamento do modelo.                       |
| train_identity.csv    | Informações complementares de identidade das transações de treinamento. |
| test_transaction.csv  | Transações destinadas à geração das previsões.                          |
| test_identity.csv     | Informações complementares das transações de teste.                     |
| sample_submission.csv | Modelo de submissão utilizado na competição Kaggle.                     |

A integração entre os arquivos é realizada por meio da coluna **TransactionID**.

---

# 4. Principais Resultados

## Estrutura dos dados

O conjunto de dados apresenta grande volume de informações, com centenas de atributos distribuídos entre variáveis numéricas, categóricas e atributos anonimizados (`V1` a `V339`).

A estrutura dos arquivos mostrou-se consistente para suportar as próximas etapas do projeto.

---

## Qualidade dos dados

A análise identificou colunas com elevados percentuais de valores ausentes, especialmente entre os atributos de identidade.

Também foram observadas colunas com baixa cardinalidade e colunas com elevada cardinalidade, características que deverão ser consideradas durante o processo de preparação dos dados.

Não foram identificadas inconsistências estruturais que inviabilizem o processamento do dataset.

---

## Variável alvo

A variável **isFraud** apresenta forte desbalanceamento entre as classes.

Esse comportamento confirma que o problema representa um cenário real de detecção de fraude e indica que o treinamento dos modelos deverá considerar técnicas específicas para tratamento de classes desbalanceadas.

---

## Relacionamento entre os arquivos

A validação da chave **TransactionID** demonstrou que:

* a chave é única nas tabelas `train_transaction` e `train_identity`;
* o relacionamento entre essas tabelas é do tipo **1:1 opcional**;
* o conjunto de treinamento contém **590.540** transações;
* apenas **144.233** transações (**24,42%**) possuem informações complementares de identidade;
* **446.307** transações (**75,58%**) não possuem registro correspondente na tabela de identidade.

Esses resultados demonstram que as informações de identidade representam um enriquecimento parcial do dataset e não podem ser consideradas obrigatórias para todas as transações.

---

# 5. Impactos para o Projeto

Os resultados obtidos nesta etapa influenciarão diretamente as próximas fases do projeto.

As principais decisões decorrentes do Data Profiling são:

* definir regras específicas para tratamento de valores ausentes durante o ETL;
* preservar a estrutura de relacionamento baseada na chave `TransactionID`;
* avaliar a relevância das variáveis de identidade para os modelos de Machine Learning;
* considerar estratégias para tratamento do desbalanceamento da variável alvo;
* utilizar o Data Profiling como base para a elaboração do Data Quality Report e da Exploratory Data Analysis.

---

# 6. Conclusão

A etapa de Data Profiling proporcionou uma visão abrangente da estrutura, da qualidade e dos relacionamentos presentes no dataset IEEE-CIS Fraud Detection.

As análises realizadas forneceram evidências suficientes para compreender o comportamento dos dados e reduzir riscos nas etapas seguintes do projeto.

O conhecimento obtido nesta fase servirá como referência para a implementação do pipeline de ETL, para a modelagem analítica e para o desenvolvimento dos modelos de Machine Learning.

---

# 7. Próximos Passos

Com a conclusão do Data Profiling, o projeto seguirá para as seguintes atividades:

1. elaboração do **Data Quality Report**;
2. realização da **Exploratory Data Analysis (EDA)**;
3. construção do **Data Dictionary**;
4. implementação do pipeline de ETL.
