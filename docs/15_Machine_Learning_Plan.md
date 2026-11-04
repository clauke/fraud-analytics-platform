# Plano de Machine Learning — Fraud Analytics Platform

**Projeto:** Fraud Analytics Platform  
**Sprint:** 6 — Machine Learning  
**Status:** Em andamento  
**Versão:** 1.0

---

## 1. Objetivo

Desenvolver modelos de Machine Learning capazes de identificar transações potencialmente fraudulentas, utilizando os dados preparados nas camadas ODS e DWH do projeto Fraud Analytics Platform.

O objetivo é construir modelos de classificação, avaliar seu desempenho e identificar quais atributos contribuem de forma mais relevante para a detecção de fraudes.

O desenvolvimento será realizado de forma incremental, começando por um modelo baseline e evoluindo para modelos mais sofisticados.

## 2. Problema de Negócio

Instituições financeiras precisam identificar transações fraudulentas com rapidez e precisão, reduzindo perdas financeiras e minimizando o impacto sobre clientes legítimos.

O modelo deverá auxiliar na identificação de transações suspeitas, buscando equilíbrio entre:

- Detectar o maior número possível de fraudes.
- Reduzir a quantidade de transações legítimas classificadas incorretamente como fraudulentas.
- Oferecer resultados que possam apoiar decisões de prevenção a fraudes.

## 3. Fontes de Dados

Serão utilizadas as tabelas da camada ODS do SQL Server:

### 3.1. ods.transactions

Contém os dados das transações financeiras, incluindo:

- TransactionID
- TransactionDT
- TransactionAmt
- ProductCD
- card1 a card6
- addr1 e addr2
- dist1 e dist2
- P_emaildomain
- R_emaildomain
- isFraud

### 3.2. ods.identities

Contém informações complementares relacionadas à identidade e aos dispositivos utilizados nas transações:

- id_01 a id_38
- DeviceType
- DeviceInfo
- TransactionID

### 3.3. Volume de dados

A base de treinamento apresenta os seguintes volumes:

| Conjunto | Registros | Fraudes identificadas |
|---|---:|---:|
| Train | 590.540 | 20.663 |
| Test | 506.691 | Não disponível |

O conjunto de teste não possui valores para a variável `isFraud`. Portanto, não será utilizado na avaliação supervisionada dos modelos nesta etapa.

## 4. Variável-Alvo (Target)

A variável-alvo será:

**isFraud**

- `1`: transação fraudulenta.
- `0`: transação legítima.

Essa variável será utilizada exclusivamente como alvo de treinamento e avaliação, não podendo ser utilizada como variável preditora.

## 5. Seleção de Variáveis (Features)

A seleção das variáveis será realizada de forma incremental.

### 5.1. Variáveis iniciais — Transações

Serão consideradas inicialmente:

- TransactionDT
- TransactionAmt
- ProductCD
- card1 a card6
- addr1 e addr2
- dist1 e dist2
- P_emaildomain
- R_emaildomain

O campo `TransactionID` será mantido para identificação e integração dos dados, mas não será utilizado inicialmente como variável preditora.

A variável `TransactionDT` será avaliada considerando seu comportamento temporal e os possíveis impactos sobre a generalização dos modelos.

### 5.2. Variáveis complementares — Identidade e dispositivo

Em uma segunda etapa, serão avaliadas:

- id_01 a id_38
- DeviceType
- DeviceInfo

Essas variáveis serão incorporadas em um experimento separado, permitindo comparar o desempenho dos modelos com e sem informações de identidade e dispositivo.

A ausência de informações de identidade não será motivo para excluir transações da base.

### 5.3. Variáveis excluídas

Não serão utilizadas como variáveis preditoras:

- isFraud, por ser a variável-alvo.
- TransactionID, inicialmente.
- data_source.
- source_file.
- batch_id.
- load_date.
- etl_status.

Os campos de controle do processo ETL não representam características legítimas da transação para fins de previsão.

## 6. Preparação dos Dados

A preparação dos dados será realizada em Python, utilizando principalmente Pandas e Scikit-learn.

As atividades previstas são:

1. Carregar os dados preparados em `data/processed/fraud_ml_train.csv`.
2. Separar as variáveis preditoras da variável-alvo.
3. Verificar tipos de dados e valores ausentes.
4. Tratar valores ausentes por meio de estratégias adequadas de imputação.
5. Codificar variáveis categóricas.
6. Aplicar normalização ou padronização às variáveis numéricas quando necessário.
7. Preparar os conjuntos de treinamento e validação.
8. Garantir que as transformações sejam ajustadas somente com os dados de treinamento, evitando vazamento de informações (*data leakage*).

A integração entre transações e identidades será realizada por meio de `TransactionID` e `data_source`, utilizando `LEFT JOIN`.

Essa estratégia preserva todas as transações, inclusive aquelas sem informações complementares de identidade.

A análise de qualidade confirmou que não existem duplicidades de `TransactionID` na tabela de identidades dentro de cada origem de dados, permitindo essa integração sem multiplicação de registros.

## 7. Estratégia de Modelagem

O desenvolvimento dos modelos será realizado em etapas.

### 7.1. Modelo Baseline

Será desenvolvido inicialmente um modelo de referência utilizando as variáveis das transações.

O primeiro algoritmo considerado será a Regressão Logística (*Logistic Regression*).

Esse modelo permitirá estabelecer uma referência de desempenho para as próximas experiências.

### 7.2. Modelo com informações complementares

Após a avaliação do baseline, serão incorporadas as variáveis de identidade e dispositivo.

O objetivo será verificar se essas informações aumentam a capacidade de identificação de fraudes.

### 7.3. Modelos adicionais

Após os experimentos iniciais, poderão ser avaliados outros algoritmos, como:

- Random Forest.
- Gradient Boosting.

A escolha dos modelos seguintes será orientada pelos resultados obtidos nas etapas anteriores.

## 8. Estratégia de Validação

A avaliação dos modelos utilizará duas estratégias complementares.

### 8.1. Divisão estratificada

Os dados serão divididos em conjuntos de treinamento e validação, preservando aproximadamente a proporção entre transações legítimas e fraudulentas.

Será utilizada uma semente aleatória fixa para garantir a reprodutibilidade dos experimentos.

Essa estratégia permitirá avaliar o desempenho dos modelos em uma divisão representativa das classes.

### 8.2. Divisão cronológica

Também será realizada uma validação baseada na ordem temporal das transações.

Nesse cenário:

- As transações mais antigas serão utilizadas para treinamento.
- As transações mais recentes serão utilizadas para validação.

Essa estratégia permitirá investigar a capacidade de generalização dos modelos diante de transações futuras.

A análise temporal exploratória identificou taxas de fraude entre 2,57% e 4,12% nos seis períodos avaliados:

| Período | Transações | Fraudes | Taxa de fraude |
|---|---:|---:|---:|
| 0 | 98.424 | 2.529 | 2,57% |
| 1 | 98.423 | 3.306 | 3,36% |
| 2 | 98.423 | 4.059 | 4,12% |
| 3 | 98.423 | 3.686 | 3,75% |
| 4 | 98.423 | 3.686 | 3,75% |
| 5 | 98.424 | 3.397 | 3,45% |

A variação observada justifica investigar a generalização temporal dos modelos.

Os resultados das duas estratégias serão comparados para identificar possíveis diferenças de desempenho.

O conjunto `test`, por não possuir rótulos de fraude, não será utilizado para calcular métricas supervisionadas.

## 9. Métricas de Avaliação

Considerando o objetivo de detectar fraudes, serão utilizadas as seguintes métricas:

- **Recall:** proporção de fraudes reais identificadas corretamente.
- **Precision:** proporção das transações classificadas como fraude que realmente são fraudulentas.
- **F1-score:** equilíbrio entre Precision e Recall.
- **PR-AUC:** avaliação da relação entre Precision e Recall em diferentes limiares de classificação.
- **Matriz de Confusão:** identificação de verdadeiros positivos, verdadeiros negativos, falsos positivos e falsos negativos.

A acurácia (*Accuracy*) também poderá ser apresentada como informação complementar, mas não será utilizada isoladamente para avaliar os modelos.

A escolha do limiar de classificação será analisada considerando o equilíbrio entre detecção de fraudes e falsos alertas.

## 10. Desbalanceamento das Classes

A base de treinamento apresenta forte desbalanceamento entre as classes:

| Classe | Registros | Percentual |
|---|---:|---:|
| Transações legítimas | 569.877 | 96,50% |
| Transações fraudulentas | 20.663 | 3,50% |
| **Total** | **590.540** | **100%** |

Esse cenário caracteriza um problema de classificação desbalanceada.

Por esse motivo, a avaliação dos modelos priorizará métricas como Recall, Precision, F1-score e PR-AUC, evitando que a acurácia elevada esconda uma baixa capacidade de identificação de fraudes.

Serão avaliadas estratégias para lidar com o desbalanceamento, como:

- Ajuste de pesos das classes (*class_weight*).
- Técnicas de reamostragem, caso necessário.

Qualquer técnica de reamostragem será aplicada exclusivamente aos dados de treinamento, evitando interferências no conjunto de validação.

## 11. Reprodutibilidade e Organização

O desenvolvimento será realizado utilizando:

- Python 3.11.7.
- Pandas.
- NumPy.
- Scikit-learn.
- Matplotlib.
- Jupyter Notebook.

Os scripts de preparação e experimentação serão armazenados no diretório `python/` e os notebooks de análise no diretório `notebooks/`.

Os modelos treinados e seus respectivos artefatos serão armazenados no diretório `models/`.

Os resultados dos experimentos e as decisões técnicas serão documentados no diretório `docs/`.

A base processada será mantida localmente, sem inclusão dos arquivos de dados no repositório GitHub.

## 12. Critérios de Conclusão (Definition of Done)

A Sprint 6 será considerada concluída quando:

- [ ] A base de treinamento estiver preparada para modelagem.
- [ ] As variáveis preditoras e a variável-alvo estiverem definidas.
- [ ] O tratamento de valores ausentes estiver implementado.
- [ ] As estratégias de validação estratificada e cronológica estiverem implementadas.
- [ ] O modelo baseline estiver treinado e avaliado.
- [ ] As métricas de avaliação estiverem documentadas.
- [ ] Os experimentos com informações de identidade e dispositivo estiverem realizados.
- [ ] Pelo menos um modelo adicional tiver sido avaliado.
- [ ] Os resultados e as conclusões estiverem documentados.
- [ ] Os scripts, notebooks e artefatos relevantes estiverem organizados no repositório.

## 13. Limitações e Considerações

Durante o desenvolvimento, deverão ser consideradas as seguintes limitações:

- A base apresenta forte desbalanceamento entre as classes.
- As informações de identidade estão disponíveis para apenas parte das transações.
- Existem valores ausentes em diversas variáveis.
- A distribuição temporal das fraudes apresenta variações entre os períodos analisados.
- O desempenho em uma divisão aleatória pode não representar adequadamente o desempenho em transações futuras.
- O conjunto `test` não possui rótulos disponíveis para avaliação supervisionada nesta etapa.

Os resultados obtidos serão considerados experimentais e voltados à construção do portfólio. Um modelo com bom desempenho nos testes não estará automaticamente pronto para implantação em produção.

---

**Documento:** Plano de Machine Learning  
**Projeto:** Fraud Analytics Platform  
**Sprint:** 6 — Machine Learning