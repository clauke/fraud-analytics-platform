# Exploratory Data Analysis (EDA)

**Projeto:** Fraud Analytics Platform

**Documento:** 08_Exploratory_Data_Analysis.md

**Versão:** 0.1

**Status:** Concluído

---

# 1. Objetivo

Este documento apresenta os principais resultados da **Exploratory Data Analysis (EDA)** realizada sobre o dataset **IEEE-CIS Fraud Detection**.

O objetivo da análise foi identificar padrões associados às transações fraudulentas, avaliar o comportamento das principais variáveis de negócio e selecionar os atributos com maior potencial para as etapas de Engenharia de Atributos e Machine Learning.

As análises foram conduzidas utilizando Python (Pandas e Matplotlib) e estão documentadas no notebook **02_Exploratory_Data_Analysis.ipynb**.

---

# 2. Escopo da Análise

A EDA concentrou-se nas variáveis de negócio com maior interpretabilidade:

* `TransactionAmt`
* `ProductCD`
* `card4`
* `card6`
* `TransactionHour`
* `DeviceType`
* `DeviceInfo`

O foco foi avaliar a **taxa de fraude** por categoria e identificar variáveis com capacidade de diferenciar transações legítimas e fraudulentas.

---

# 3. Principais Resultados

## 3.1 TransactionAmt

A distribuição dos valores das transações apresentou forte assimetria à direita, com grande concentração de transações de baixo valor e presença de outliers.

As transações fraudulentas apresentaram valores ligeiramente superiores às legítimas:

* média: **R$ 149,24** (fraudes) vs **R$ 134,51** (não fraudes);
* mediana: **R$ 75,00** vs **R$ 68,50**.

A análise por faixas de valor mostrou que a taxa de fraude varia de forma não linear.

| Faixa de valor | Taxa de fraude |
| -------------- | -------------: |
| ≤ R$ 50        |          3,83% |
| R$ 50–100      |          2,92% |
| R$ 100–250     |          3,07% |
| R$ 250–500     |      **5,37%** |
| > R$ 500       |          4,41% |

A maior incidência foi observada na faixa entre **R$ 250 e R$ 500**.

### Conclusão

`TransactionAmt` possui potencial preditivo, mas deve ser analisada em conjunto com outras variáveis.

---

## 3.2 ProductCD

A variável `ProductCD` apresentou o maior poder discriminatório entre todas as variáveis analisadas.

| Categoria | Taxa de fraude |
| --------- | -------------: |
| C         |     **11,69%** |
| S         |          5,90% |
| H         |          4,77% |
| R         |          3,78% |
| W         |      **2,04%** |

A categoria **C** apresentou taxa de fraude aproximadamente **3,3 vezes superior** à média do dataset.

A análise conjunta com `TransactionAmt` mostrou que esse risco elevado ocorre mesmo em transações de baixo valor, indicando que a categoria possui um **perfil de risco próprio**.

### Conclusão

`ProductCD` será considerada uma variável prioritária para Engenharia de Atributos.

---

## 3.3 card4 (bandeira do cartão)

Foram observadas diferenças relevantes entre as bandeiras.

| Bandeira         | Taxa de fraude |
| ---------------- | -------------: |
| Discover         |      **7,73%** |
| Visa             |          3,48% |
| Mastercard       |          3,43% |
| American Express |          2,87% |

A bandeira **Discover** apresentou a maior taxa de fraude, embora com menor volume de transações.

### Conclusão

A variável `card4` será mantida para modelagem, com atenção ao volume reduzido de algumas categorias.

---

## 3.4 card6 (tipo do cartão)

A variável `card6` demonstrou forte capacidade discriminatória.

| Tipo    | Taxa de fraude |
| ------- | -------------: |
| Crédito |      **6,68%** |
| Débito  |      **2,43%** |

Transações realizadas com cartões de crédito apresentaram probabilidade de fraude aproximadamente **2,7 vezes maior** que transações com cartões de débito.

### Conclusão

`card6` será considerada uma variável prioritária para os modelos de Machine Learning.

---

## 3.5 TransactionHour

A análise temporal revelou um padrão de fraude altamente concentrado em determinados horários.

A taxa de fraude atingiu seu pico às **7h**, com **10,61%**, enquanto o menor valor foi observado às **13h**, com **2,29%**.

O aumento do risco entre **4h e 9h** ocorreu mesmo em períodos de baixo volume de transações.

### Conclusão

A variável `TransactionHour` possui elevado potencial preditivo e será transformada em atributo permanente para modelagem.

---

## 3.6 DeviceType

A variável `DeviceType` apresentou uma das maiores diferenças de risco da análise.

| Tipo de dispositivo | Taxa de fraude |
| ------------------- | -------------: |
| Mobile              |     **10,17%** |
| Desktop             |          6,52% |
| Desconhecido        |          2,10% |

Dispositivos móveis apresentaram taxa de fraude aproximadamente **4,8 vezes maior** que transações sem informação de dispositivo.

### Conclusão

`DeviceType` será considerada variável prioritária para Engenharia de Atributos.

---

## 3.7 DeviceInfo

A análise de `DeviceInfo` identificou dispositivos específicos com taxas elevadas de fraude, superiores a **10%** em alguns casos.

Entretanto, muitas dessas categorias possuem baixo volume de observações.

Entre os dispositivos mais representativos:

* Windows: **6,54%**
* iOS Device: **6,27%**
* MacOS: **2,21%**

### Conclusão

A variável `DeviceInfo` será utilizada em versões consolidadas (família do dispositivo ou sistema operacional), evitando excesso de categorias de baixa frequência.

---

# 4. Ranking das Variáveis por Poder Discriminatório

A comparação das taxas de fraude identificou as seguintes variáveis como mais relevantes:

| Variável                | Maior taxa | Menor taxa |     Diferença |
| ----------------------- | ---------: | ---------: | ------------: |
| ProductCD               | **11,69%** |      2,04% | **9,65 p.p.** |
| TransactionHour         | **10,61%** |      2,29% | **8,32 p.p.** |
| DeviceType              | **10,17%** |      2,10% | **8,07 p.p.** |
| card4                   |      7,73% |      2,87% |     4,86 p.p. |
| card6                   |      6,68% |      2,43% |     4,25 p.p. |
| TransactionAmt (faixas) |      5,37% |      2,92% |     2,45 p.p. |

---

# 5. Variáveis Prioritárias para Engenharia de Atributos

Com base nos resultados da EDA, as seguintes variáveis serão priorizadas nas próximas etapas:

### Alta prioridade

* ProductCD
* TransactionHour
* DeviceType
* card6

### Média prioridade

* TransactionAmt
* card4
* DeviceInfo (versão consolidada)

Também serão avaliadas interações entre variáveis, especialmente:

* ProductCD × TransactionAmt
* ProductCD × DeviceType
* TransactionHour × DeviceType

---

# 6. Conclusão

A análise exploratória identificou padrões claros de risco associados ao **tipo de produto**, **horário da transação**, **tipo de dispositivo** e **tipo do cartão**.

Os resultados demonstram que o risco de fraude é influenciado por múltiplos fatores e que a combinação dessas variáveis possui elevado potencial para melhorar o desempenho dos modelos de Machine Learning.

As evidências obtidas nesta etapa servirão como base para a **Sprint 3 – Engenharia de Dados (ETL)** e para a **Sprint 4 – Engenharia de Atributos**, onde essas variáveis serão transformadas em atributos analíticos para o treinamento dos modelos preditivos.

---

# 7. Próximos Passos

As próximas atividades previstas são:

1. elaboração do **Data Dictionary**;
2. implementação do pipeline de ETL em Python, SQL e SSIS;
3. construção das camadas Staging, ODS e Data Warehouse;
4. Engenharia de Atributos;
5. desenvolvimento dos modelos de Machine Learning.
