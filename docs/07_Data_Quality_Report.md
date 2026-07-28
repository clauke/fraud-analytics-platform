# Data Quality Report

**Projeto:** Fraud Analytics Platform

**Documento:** 08_Data_Quality_Report.md

**Versão:** 0.1

**Status:** Concluído

---

# 1. Objetivo

Este documento apresenta a avaliação da qualidade dos dados do dataset **IEEE-CIS Fraud Detection**.

Seu objetivo é registrar os principais problemas identificados durante o Data Profiling e definir as diretrizes que serão adotadas nas próximas etapas do projeto, especialmente na implementação do pipeline de ETL, na modelagem analítica e na preparação dos dados para Machine Learning.

---

# 2. Escopo

A avaliação contempla os cinco arquivos que compõem o dataset:

* `train_transaction.csv`
* `train_identity.csv`
* `test_transaction.csv`
* `test_identity.csv`
* `sample_submission.csv`

As análises foram realizadas a partir do notebook **01_Data_Profiling.ipynb**.

---

# 3. Dimensões Avaliadas

Foram analisadas as seguintes dimensões de qualidade dos dados:

* Completude
* Unicidade
* Integridade
* Consistência
* Variabilidade
* Balanceamento da variável alvo

---

# 4. Resultados da Avaliação

## 4.1 Completude

Foram identificadas diversas colunas com elevado percentual de valores ausentes.

Entre os principais resultados observados:

### train_transaction.csv

* `dist2` → 93,63% de valores ausentes
* `D7` → 93,41%
* `D13` → 89,51%
* `D14` → 89,47%
* `D12` → 89,04%

Também foram identificadas diversas variáveis da família `V` com aproximadamente 86% de valores ausentes.

### train_identity.csv

As colunas de identidade apresentam níveis ainda maiores de ausência:

* `id_24` → 96,71%
* `id_25` → 96,44%
* `id_07` → 96,43%
* `id_08` → 96,43%
* `id_21` → 96,42%

Em contrapartida, algumas variáveis apresentam melhor nível de preenchimento, como:

* `DeviceInfo` → 17,73% de valores ausentes.

### Decisão

Os valores ausentes são considerados uma característica do dataset e não um erro de processamento.

Portanto:

* nenhuma coluna será removida durante a ingestão dos dados;
* todas as informações serão preservadas nas camadas **Raw** e **Staging**;
* o tratamento será definido individualmente durante a etapa de preparação dos dados para análise e modelagem.

---

## 4.2 Unicidade

Não foram identificados registros duplicados em nenhum dos arquivos analisados.

### Decisão

Não será implementada etapa de remoção de registros duplicados no processo de ETL.

---

## 4.3 Integridade

A validação da chave `TransactionID` confirmou que:

* a chave é única nas tabelas de transações e identidade;
* o relacionamento entre `train_transaction` e `train_identity` é do tipo **1:1 opcional**.

Foi observado que:

* **590.540** transações compõem o conjunto de treinamento;
* **144.233** possuem informações complementares de identidade (**24,42%**);
* **446.307** não possuem registro correspondente (**75,58%**).

### Decisão

O processo de integração utilizará **LEFT JOIN**, preservando todas as transações, independentemente da existência de informações de identidade.

---

## 4.4 Consistência

Os conjuntos de treinamento e teste apresentam estruturas compatíveis, permitindo a aplicação das mesmas regras de transformação durante o pipeline de ETL.

### Decisão

As regras de limpeza e transformação serão padronizadas entre os conjuntos de treinamento e teste, respeitando apenas as diferenças inerentes à presença da variável alvo (`isFraud`).

---

## 4.5 Variabilidade

A variável `V107` apresentou comportamento de baixa variabilidade:

* no conjunto de treinamento, mais de 99,9% dos registros possuem valor **1.0**;
* no conjunto de teste, todos os registros apresentam valor **1.0**.

### Decisão

A permanência dessa variável será avaliada durante a etapa de seleção de atributos para Machine Learning. Nesta fase, nenhuma remoção será realizada.

---

## 4.6 Balanceamento da Variável Alvo

A distribuição da variável `isFraud` é:

| Classe         | Quantidade | Percentual |
| -------------- | ---------: | ---------: |
| Não fraude (0) |    569.877 |      96,5% |
| Fraude (1)     |     20.663 |       3,5% |

### Decisão

O desbalanceamento será tratado exclusivamente durante o treinamento dos modelos de Machine Learning.

Os dados armazenados nas camadas Raw, Staging, ODS e Data Warehouse permanecerão inalterados, preservando a distribuição original do dataset.

---

# 5. Matriz de Qualidade dos Dados

| Dimensão      | Situação Encontrada                                     | Estratégia Adotada                                             |
| ------------- | ------------------------------------------------------- | -------------------------------------------------------------- |
| Completude    | Alto percentual de valores ausentes em diversas colunas | Preservar os dados; definir tratamento específico por variável |
| Unicidade     | Nenhum registro duplicado                               | Não aplicar deduplicação                                       |
| Integridade   | Relacionamento 1:1 opcional por `TransactionID`         | Utilizar `LEFT JOIN`                                           |
| Consistência  | Estruturas compatíveis entre treino e teste             | Padronizar regras de transformação                             |
| Variabilidade | Variável `V107` com baixa variabilidade                 | Avaliar na seleção de atributos                                |
| Balanceamento | Apenas 3,5% das transações são fraudulentas             | Tratar somente na etapa de Machine Learning                    |

---

# 6. Conclusão

A avaliação de qualidade demonstrou que o dataset apresenta estrutura consistente e adequada para o desenvolvimento do projeto.

Os principais desafios concentram-se na elevada quantidade de valores ausentes e no forte desbalanceamento da variável alvo, características comuns em bases reais de detecção de fraude.

As decisões registradas neste documento servirão como referência para a implementação do pipeline de ETL, garantindo que as transformações sejam executadas de forma padronizada e alinhada aos objetivos do projeto.

---

# 7. Próximos Passos

Com a conclusão desta etapa, o projeto seguirá para:

1. Exploratory Data Analysis (EDA);
2. Data Dictionary;
3. implementação do pipeline de ETL;
4. modelagem do Data Warehouse;
5. desenvolvimento dos modelos de Machine Learning.
