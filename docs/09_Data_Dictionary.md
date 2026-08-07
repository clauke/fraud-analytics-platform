# Data Dictionary

**Projeto:** Fraud Analytics Platform

**Documento:** 09_Data_Dictionary.md

**Versão:** 0.1

**Status:** Concluído

---

# 1. Objetivo

Este documento descreve as principais variáveis utilizadas no projeto **Fraud Analytics Platform**, consolidando as informações obtidas durante as etapas de Data Profiling e Exploratory Data Analysis (EDA).

O objetivo é padronizar o entendimento das variáveis, registrar sua finalidade analítica e indicar sua prioridade para Engenharia de Atributos, Machine Learning e Business Intelligence.

---

# 2. Estrutura do Dataset

O dataset IEEE-CIS Fraud Detection é composto por dois grupos principais de informações:

* **Transações** (`train_transaction.csv`)
* **Identidade do dispositivo e do usuário** (`train_identity.csv`)

As tabelas são relacionadas por meio da chave **TransactionID**.

---

# 3. Variáveis Principais

## TransactionID

| Campo      | Descrição                          |
| ---------- | ---------------------------------- |
| Tipo       | Chave identificadora               |
| Origem     | train_transaction / train_identity |
| Descrição  | Identificador único da transação.  |
| Prioridade | Alta                               |

### Observações

* Utilizada como chave de integração entre as tabelas.
* Não será utilizada como variável preditiva.

---

## isFraud

| Campo      | Descrição                                                |
| ---------- | -------------------------------------------------------- |
| Tipo       | Variável alvo                                            |
| Origem     | train_transaction                                        |
| Descrição  | Indica se a transação é fraudulenta (1) ou legítima (0). |
| Prioridade | Crítica                                                  |

### Observações

* Apresenta forte desbalanceamento (3,5% de fraudes).

---

## TransactionAmt

| Campo      | Descrição                     |
| ---------- | ----------------------------- |
| Tipo       | Numérica contínua             |
| Origem     | train_transaction             |
| Descrição  | Valor monetário da transação. |
| Prioridade | Alta                          |

### Principais achados

* Distribuição fortemente assimétrica.
* Presença de outliers.
* Fraudes apresentam valores médios superiores.

### Uso previsto

* Feature numérica.
* Criação de faixas de valor.
* Possível transformação logarítmica na modelagem.

---

## ProductCD

| Campo      | Descrição                                   |
| ---------- | ------------------------------------------- |
| Tipo       | Categórica                                  |
| Origem     | train_transaction                           |
| Descrição  | Categoria do produto associado à transação. |
| Prioridade | Crítica                                     |

### Principais achados

* Categoria **C** apresentou taxa de fraude de **11,69%**.
* Variável com maior poder discriminatório observado na EDA.

### Uso previsto

* Feature categórica.
* Engenharia de atributos.
* Interações com TransactionAmt.

---

## card4

| Campo      | Descrição           |
| ---------- | ------------------- |
| Tipo       | Categórica          |
| Origem     | train_transaction   |
| Descrição  | Bandeira do cartão. |
| Prioridade | Média               |

### Principais achados

* Discover apresentou maior taxa de fraude (7,73%).

### Uso previsto

* Feature categórica.

---

## card6

| Campo      | Descrição                              |
| ---------- | -------------------------------------- |
| Tipo       | Categórica                             |
| Origem     | train_transaction                      |
| Descrição  | Tipo do cartão (crédito, débito etc.). |
| Prioridade | Alta                                   |

### Principais achados

* Cartões de crédito apresentaram taxa de fraude de **6,68%**.
* Cartões de débito apresentaram **2,43%**.

### Uso previsto

* Feature categórica prioritária.

---

# 4. Variáveis Temporais

## TransactionDT

| Campo      | Descrição                    |
| ---------- | ---------------------------- |
| Tipo       | Numérica (tempo relativo)    |
| Origem     | train_transaction            |
| Descrição  | Tempo relativo da transação. |
| Prioridade | Alta                         |

### Observações

* Não representa uma data de calendário.
* Será utilizada para derivação de atributos temporais.

---

## TransactionHour

| Campo      | Descrição                          |
| ---------- | ---------------------------------- |
| Tipo       | Numérica discreta                  |
| Origem     | Derivada de TransactionDT          |
| Descrição  | Hora relativa da transação (0–23). |
| Prioridade | Crítica                            |

### Principais achados

* Pico de fraude às **7h (10,61%)**.
* Menor risco entre **13h e 17h**.

### Uso previsto

* Feature temporal permanente.

---

## TransactionDay

| Campo      | Descrição                  |
| ---------- | -------------------------- |
| Tipo       | Numérica discreta          |
| Origem     | Derivada de TransactionDT  |
| Descrição  | Dia relativo da transação. |
| Prioridade | Média                      |

### Uso previsto

* Análises temporais.
* Engenharia de atributos.

---

# 5. Variáveis de Dispositivo

## DeviceType

| Campo      | Descrição                                   |
| ---------- | ------------------------------------------- |
| Tipo       | Categórica                                  |
| Origem     | train_identity                              |
| Descrição  | Tipo do dispositivo utilizado na transação. |
| Prioridade | Crítica                                     |

### Principais achados

* Mobile: **10,17%**
* Desktop: **6,52%**
* Desconhecido: **2,10%**

### Uso previsto

* Feature categórica prioritária.

---

## DeviceInfo

| Campo      | Descrição                                            |
| ---------- | ---------------------------------------------------- |
| Tipo       | Categórica (alta cardinalidade)                      |
| Origem     | train_identity                                       |
| Descrição  | Identificação do dispositivo ou sistema operacional. |
| Prioridade | Média                                                |

### Principais achados

* Alguns dispositivos apresentaram taxas superiores a 10%.

### Uso previsto

* Consolidação por família de dispositivo.
* Redução de cardinalidade.

---

# 6. Variáveis Derivadas Planejadas

As seguintes variáveis serão criadas durante a etapa de Engenharia de Atributos:

| Variável             | Origem         | Finalidade                           |
| -------------------- | -------------- | ------------------------------------ |
| TransactionHour      | TransactionDT  | Capturar padrão horário              |
| TransactionDay       | TransactionDT  | Capturar evolução temporal           |
| Faixa_TransactionAmt | TransactionAmt | Segmentação por valor                |
| is_mobile            | DeviceType     | Simplificação do tipo de dispositivo |
| DeviceFamily         | DeviceInfo     | Redução de cardinalidade             |

---

# 7. Ranking de Prioridade Analítica

Com base na EDA, as variáveis foram classificadas conforme seu potencial discriminatório.

## Prioridade crítica

* isFraud
* ProductCD
* TransactionHour
* DeviceType

## Prioridade alta

* TransactionAmt
* card6
* TransactionDT

## Prioridade média

* card4
* DeviceInfo
* TransactionDay

---

# 8. Considerações para o ETL

Durante a implementação do pipeline de ETL:

* os valores originais serão preservados na camada **Raw**;
* as transformações serão aplicadas na camada **Staging**;
* as variáveis derivadas serão armazenadas na **ODS**;
* apenas atributos selecionados serão promovidos ao **Data Warehouse**.

---

# 9. Conclusão

O Data Dictionary consolida o entendimento das variáveis prioritárias do projeto e estabelece uma referência comum para as próximas etapas de Engenharia de Dados e Ciência de Dados.

As variáveis **ProductCD**, **TransactionHour** e **DeviceType** apresentaram os maiores níveis de discriminação entre transações legítimas e fraudulentas e serão o foco principal das etapas de Engenharia de Atributos e modelagem preditiva.

Este documento será atualizado conforme novas variáveis derivadas forem incorporadas ao pipeline analítico do projeto.
