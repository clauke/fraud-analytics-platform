# Sprint 6 — Planejamento de Machine Learning

## 1. Objetivo

Desenvolver e avaliar modelos de Machine Learning para detectar transações fraudulentas utilizando os dados da Fraud Analytics Platform.

O objetivo é estabelecer um modelo de referência reproduzível, avaliar sua capacidade de identificar fraudes e investigar se os atributos de identidade e dispositivo melhoram o desempenho preditivo.

## 2. Problema de Negócio

As transações fraudulentas representam uma pequena proporção do volume total de transações. O modelo deverá identificar operações suspeitas, equilibrando a capacidade de detecção de fraudes e a ocorrência de falsos positivos.

A solução deverá apoiar as análises de fraude e fornecer uma base para futura integração com a camada de Business Intelligence.

## 3. Fontes de Dados

Os experimentos iniciais utilizarão as seguintes tabelas do banco de dados `FraudAnalytics`, no SQL Server:

- `ods.transactions`: atributos das transações e variável-alvo.
- `ods.identities`: atributos de identidade e dispositivo que poderão complementar os dados das transações.

A base de treinamento contém 590.540 transações da fonte `train`, sendo:

- 20.663 transações fraudulentas.
- 569.877 transações legítimas.

A fonte `test` contém 506.691 transações sem rótulos de fraude disponíveis. Por esse motivo, não será utilizada para calcular métricas de avaliação supervisionada.

## 4. Variável-Alvo

A variável-alvo será `isFraud`:

- `1`: transação fraudulenta.
- `0`: transação legítima.

A variável-alvo e qualquer informação derivada dela não poderão ser utilizadas como variáveis preditoras.

## 5. Variáveis Candidatas

### 5.1. Atributos das Transações

As variáveis candidatas da tabela `ods.transactions` incluem:

- `TransactionDT`
- `TransactionAmt`
- `ProductCD`
- `card1`, `card2`, `card3`, `card4`, `card5`, `card6`
- `addr1`, `addr2`
- `dist1`, `dist2`
- `P_emaildomain`, `R_emaildomain`

Inicialmente, `TransactionID` será excluída como variável preditora direta, por ser um identificador da transação.

O uso de `TransactionDT` será avaliado considerando seu significado temporal e o risco de vazamento de informação.

### 5.2. Atributos de Identidade e Dispositivo

Os atributos candidatos da tabela `ods.identities` incluem:

- `id_01` até `id_38`
- `DeviceType`
- `DeviceInfo`

Essas variáveis serão avaliadas em um experimento separado para verificar sua contribuição adicional à capacidade preditiva do modelo.

### 5.3. Colunas Excluídas

As colunas de controle operacional do processo de ETL não serão utilizadas como variáveis preditoras:

- `data_source`
- `source_file`
- `batch_id`
- `load_date`
- `etl_status`

A variável-alvo `isFraud` também será excluída da matriz de atributos preditores.

## 6. Preparação dos Dados

O processo de preparação deverá:

1. Selecionar os registros rotulados da fonte `train`.
2. Preservar as transações válidas, evitando excluir registros apenas por possuírem atributos ausentes.
3. Avaliar os valores ausentes e aplicar estratégias adequadas de imputação ou tratamento de categorias ausentes.
4. Codificar as variáveis categóricas e normalizar ou padronizar as numéricas quando necessário para o algoritmo escolhido.
5. Ajustar as transformações utilizando exclusivamente os dados da partição de treinamento, evitando vazamento de informação.
6. Verificar os tipos de dados, duplicidades e distribuição da variável-alvo antes do treinamento.

A tabela `ods.identities` será combinada com `ods.transactions` por meio de `TransactionID` e `data_source`.

Será utilizado `LEFT JOIN` para preservar as transações que não possuam correspondência na tabela de identidades.

## 7. Estratégia de Modelagem

O fluxo inicial de modelagem comparará dois cenários:

1. **Modelo de referência:** utiliza os atributos da tabela `ods.transactions`.
2. **Modelo enriquecido:** incorpora atributos selecionados de identidade e dispositivo da tabela `ods.identities`.

Os algoritmos candidatos serão escolhidos considerando as características dos dados, a interpretabilidade, o custo computacional e os resultados de avaliação.

O primeiro experimento deverá estabelecer uma referência reproduzível antes da introdução de algoritmos mais complexos ou de técnicas adicionais de engenharia de atributos.

## 8. Estratégia de Validação

A base rotulada de treinamento será dividida em partições de treinamento e validação, utilizando divisão estratificada para preservar a proporção de transações fraudulentas.

Será utilizada uma semente aleatória fixa para permitir a reprodução dos experimentos.

Como a dimensão temporal pode ser relevante para a detecção de fraudes, também será considerada uma estratégia de validação cronológica para avaliar o desempenho em transações posteriores ao período de treinamento.

A fonte `test`, por não possuir rótulos disponíveis, não será utilizada para calcular métricas de avaliação supervisionada.

## 9. Métricas de Avaliação

O desempenho dos modelos será avaliado utilizando:

- **Precisão (Precision):** proporção das transações classificadas como fraude que realmente são fraudulentas.
- **Revocação (Recall):** proporção das transações fraudulentas efetivamente identificadas pelo modelo.
- **F1-score:** média harmônica entre precisão e revocação.
- **PR-AUC:** área sob a curva de precisão e revocação, especialmente relevante para problemas de classificação desbalanceados.
- **Matriz de confusão:** apresenta os verdadeiros positivos, falsos positivos, verdadeiros negativos e falsos negativos.

A acurácia poderá ser apresentada como métrica