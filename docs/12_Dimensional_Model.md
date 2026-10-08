# Modelagem Dimensional do Data Warehouse

**Projeto:** Fraud Analytics Platform
**Documento:** 12_Dimensional_Model.md
**Versão:** 0.1
**Status:** Em desenvolvimento

# 12 - Dimensional Model

## 1. Objetivo

Este documento define o modelo dimensional da camada Data Warehouse (DWH) da plataforma **Fraud Analytics Platform**.

O objetivo do DWH é transformar os dados integrados da camada ODS em uma estrutura orientada à análise, permitindo o desenvolvimento de indicadores de fraude, análises exploratórias e consumo posterior por ferramentas de Business Intelligence.

A camada DWH não tem como objetivo simplesmente reproduzir a estrutura da ODS. Ela organiza os dados segundo conceitos dimensionais, priorizando:

* análise de transações;
* identificação de padrões de fraude;
* análise temporal;
* análise por produto;
* análise por cartão;
* análise por dispositivo;
* análise por características de identidade;
* análise por endereço e distância;
* rastreabilidade dos dados de origem.

---

## 2. Estratégia de Modelagem

Será adotado um modelo dimensional do tipo **Star Schema**, tendo a transação como evento central do modelo.

A tabela fato armazenará os eventos transacionais e suas principais medidas e indicadores, enquanto as dimensões fornecerão os contextos necessários para análise.

A estrutura proposta é:

```text
                         ┌─────────────────┐
                         │    dim_date     │
                         └────────┬────────┘
                                  │
                                  │
┌─────────────────┐      ┌────────▼────────┐      ┌─────────────────┐
│   dim_product   │──────│ fact_transaction│──────│    dim_card     │
└─────────────────┘      └────────┬────────┘      └─────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
             ┌────────────┐ ┌────────────┐ ┌────────────┐
             │dim_identity│ │dim_device  │ │dim_address │
             └────────────┘ └────────────┘ └────────────┘
```

---

## 3. Grão da Tabela Fato

O grão da tabela `fact_transaction` será:

> **Uma linha representa uma transação individual identificada por `TransactionID`.**

Esse grão mantém a granularidade original do evento transacional e permite análises agregadas por diferentes dimensões.

Exemplos de análises possíveis:

* quantidade de transações;
* valor total transacionado;
* quantidade de transações fraudulentas;
* valor associado a fraudes;
* taxa de fraude;
* fraude por produto;
* fraude por cartão;
* fraude por dispositivo;
* fraude por período;
* fraude por endereço e distância.

---

## 4. Tabela Fato

### 4.1 `dwh.fact_transaction`

A tabela fato será o núcleo do Data Warehouse.

### Chaves

| Campo          | Tipo conceitual | Descrição                              |
| -------------- | --------------- | -------------------------------------- |
| TransactionKey | Surrogate Key   | Identificador técnico da linha da fato |
| TransactionID  | Business Key    | Identificador original da transação    |
| DateKey        | Foreign Key     | Referência à dimensão de data          |
| ProductKey     | Foreign Key     | Referência à dimensão de produto       |
| CardKey        | Foreign Key     | Referência à dimensão de cartão        |
| IdentityKey    | Foreign Key     | Referência à dimensão de identidade    |
| DeviceKey      | Foreign Key     | Referência à dimensão de dispositivo   |
| AddressKey     | Foreign Key     | Referência à dimensão de endereço      |

### Atributos e medidas

| Campo          | Origem             | Função                                |
| -------------- | ------------------ | ------------------------------------- |
| TransactionDT  | `ods.transactions` | Timestamp/tempo relativo da transação |
| TransactionAmt | `ods.transactions` | Valor da transação                    |
| IsFraud        | `ods.transactions` | Indicador de fraude                   |

`TransactionAmt` será a principal medida monetária da fato.

`IsFraud` será utilizado como indicador para cálculo de quantidade e taxa de fraude.

Exemplo conceitual:

```text
Fraud Count = SUM(IsFraud)

Transaction Count = COUNT(TransactionID)

Fraud Rate = Fraud Count / Transaction Count
```

---

## 5. Dimensão de Data

### `dwh.dim_date`

A dimensão de data será utilizada para análises temporais.

Ela será derivada do atributo `TransactionDT` da origem.

A dimensão poderá conter:

| Campo     | Descrição                    |
| --------- | ---------------------------- |
| DateKey   | Chave substituta da data     |
| FullDate  | Data completa                |
| Year      | Ano                          |
| Quarter   | Trimestre                    |
| Month     | Número do mês                |
| MonthName | Nome do mês                  |
| Day       | Dia                          |
| DayOfWeek | Número do dia da semana      |
| DayName   | Nome do dia                  |
| IsWeekend | Indicador de final de semana |

A dimensão será utilizada principalmente pelo Power BI e demais consumidores analíticos.

---

## 6. Dimensão de Produto

### `dwh.dim_product`

Origem principal:

```text
ods.transactions.ProductCD
```

A dimensão representa o tipo de produto associado à transação.

### Atributos

| Campo      | Origem                       |
| ---------- | ---------------------------- |
| ProductKey | Surrogate Key                |
| ProductCD  | `ods.transactions.ProductCD` |

Essa dimensão permitirá análises como:

* quantidade de transações por produto;
* valor transacionado por produto;
* quantidade de fraudes por produto;
* taxa de fraude por produto.

---

## 7. Dimensão de Cartão

### `dwh.dim_card`

A dimensão de cartão agrupará os atributos relacionados ao cartão presentes na origem.

### Atributos

| Campo   | Origem                   |
| ------- | ------------------------ |
| CardKey | Surrogate Key            |
| card1   | `ods.transactions.card1` |
| card2   | `ods.transactions.card2` |
| card3   | `ods.transactions.card3` |
| card4   | `ods.transactions.card4` |
| card5   | `ods.transactions.card5` |
| card6   | `ods.transactions.card6` |

Não serão criadas dimensões separadas para cada atributo de cartão.

O conjunto será tratado como uma única dimensão de contexto do cartão.

---

## 8. Dimensão de Endereço

### `dwh.dim_address`

A dimensão representa os atributos relacionados a endereço e distância disponíveis na fonte.

### Atributos

| Campo      | Origem                   |
| ---------- | ------------------------ |
| AddressKey | Surrogate Key            |
| addr1      | `ods.transactions.addr1` |
| addr2      | `ods.transactions.addr2` |
| dist1      | `ods.transactions.dist1` |
| dist2      | `ods.transactions.dist2` |

Esses atributos poderão ser utilizados para investigar relações entre localização, distância e ocorrência de fraude.

Devido ao elevado volume de valores ausentes em alguns atributos, o modelo deverá utilizar uma estratégia explícita para valores desconhecidos.

---

## 9. Dimensão de Dispositivo

### `dwh.dim_device`

A dimensão representa as informações de dispositivo disponíveis na tabela `ods.identities`.

### Atributos

| Campo      | Origem                      |
| ---------- | --------------------------- |
| DeviceKey  | Surrogate Key               |
| DeviceType | `ods.identities.DeviceType` |
| DeviceInfo | `ods.identities.DeviceInfo` |

A dimensão permitirá análises como:

* fraude por tipo de dispositivo;
* fraude por informação de dispositivo;
* volume de transações por dispositivo;
* taxa de fraude por dispositivo.

`DeviceInfo` apresenta potencialmente alta cardinalidade e deverá ser avaliado durante a implementação quanto a indexação e desempenho.

---

## 10. Dimensão de Identidade

### `dwh.dim_identity`

A dimensão de identidade será construída a partir dos atributos `id_01` até `id_38` existentes em `ods.identities`.

### Atributos

| Campo       | Origem                 |
| ----------- | ---------------------- |
| IdentityKey | Surrogate Key          |
| id_01       | `ods.identities.id_01` |
| id_02       | `ods.identities.id_02` |
| ...         | ...                    |
| id_38       | `ods.identities.id_38` |

Os atributos `DeviceType` e `DeviceInfo` não serão mantidos nesta dimensão, pois pertencem conceitualmente à dimensão de dispositivo.

### Observação

O dataset não apresenta um identificador explícito de cliente ou pessoa.

Portanto, o modelo **não criará artificialmente uma dimensão de cliente**.

Essa decisão evita atribuir significado de negócio que não esteja presente nos dados de origem.

---

## 11. Chaves Substitutas

As dimensões utilizarão **surrogate keys**, independentes das chaves naturais ou dos valores existentes na origem.

Exemplo:

```text
dim_product
-----------
ProductKey     ← surrogate key
ProductCD      ← business attribute
```

A tabela fato armazenará as surrogate keys das dimensões:

```text
fact_transaction
----------------
TransactionKey
TransactionID
DateKey
ProductKey
CardKey
IdentityKey
DeviceKey
AddressKey
...
```

Essa abordagem reduz a dependência direta da estrutura da origem e facilita futuras evoluções do Data Warehouse.

---

## 12. Tratamento de Valores Desconhecidos

Como o dataset possui uma quantidade significativa de valores ausentes, o DWH adotará uma estratégia explícita para valores desconhecidos.

As dimensões poderão possuir um registro especial:

```text
Key = 0
Description = Unknown
```

Quando uma informação de origem estiver ausente ou não puder ser relacionada a uma dimensão, a fato poderá utilizar a chave correspondente ao registro `Unknown`.

Isso evita valores `NULL` nas foreign keys das dimensões e simplifica as consultas analíticas.

---

## 13. Rastreabilidade

Os dados do DWH deverão manter rastreabilidade até a ODS.

Quando necessário, atributos técnicos poderão ser mantidos para controle de carga, como:

* `batch_id`;
* `load_date`;
* informações de origem.

Esses atributos são considerados **metadados técnicos**, não dimensões de negócio.

---

## 14. Considerações para Machine Learning

O Data Warehouse foi projetado prioritariamente para análise e BI.

Nem todos os atributos disponíveis na ODS precisam ser propagados diretamente para o modelo dimensional.

Entretanto, atributos potencialmente relevantes para Machine Learning não deverão ser descartados da arquitetura.

Em especial:

```text
id_01 ... id_38
card1 ... card6
addr1
addr2
dist1
dist2
DeviceType
DeviceInfo
```

poderão ser utilizados posteriormente na construção de features.

A arquitetura poderá utilizar uma camada específica de preparação de features para Machine Learning, evitando sobrecarregar o modelo dimensional com atributos exclusivamente técnicos ou de modelagem estatística.

---

## 15. Mapeamento ODS → DWH

| ODS                               | DWH                               |
| --------------------------------- | --------------------------------- |
| `ods.transactions.TransactionID`  | `fact_transaction.TransactionID`  |
| `ods.transactions.TransactionDT`  | `fact_transaction.TransactionDT`  |
| `ods.transactions.TransactionAmt` | `fact_transaction.TransactionAmt` |
| `ods.transactions.ProductCD`      | `dim_product.ProductCD`           |
| `ods.transactions.card1-card6`    | `dim_card`                        |
| `ods.transactions.addr1-addr2`    | `dim_address`                     |
| `ods.transactions.dist1-dist2`    | `dim_address`                     |
| `ods.transactions.isFraud`        | `fact_transaction.IsFraud`        |
| `ods.identities.id_01-id_38`      | `dim_identity`                    |
| `ods.identities.DeviceType`       | `dim_device.DeviceType`           |
| `ods.identities.DeviceInfo`       | `dim_device.DeviceInfo`           |

Os campos técnicos da ODS, como `source_file`, `batch_id`, `load_date` e `etl_status`, serão tratados como metadados de processo e não como atributos analíticos das dimensões.

---

## 16. Modelo Final Proposto

```text
                         ┌─────────────────────┐
                         │      dim_date       │
                         │─────────────────────│
                         │ DateKey             │
                         │ FullDate            │
                         │ Year                │
                         │ Quarter             │
                         │ Month               │
                         │ MonthName           │
                         │ Day                 │
                         │ DayOfWeek           │
                         │ DayName             │
                         │ IsWeekend           │
                         └──────────┬──────────┘
                                    │
                                    │
┌─────────────────────┐   ┌─────────▼───────────┐   ┌─────────────────────┐
│     dim_product     │   │  fact_transaction   │   │      dim_card       │
│─────────────────────│   │─────────────────────│   │─────────────────────│
│ ProductKey          │   │ TransactionKey      │   │ CardKey             │
│ ProductCD           │   │ TransactionID       │   │ card1               │
└─────────────────────┘   │ DateKey             │   │ card2               │
                          │ ProductKey          │   │ card3               │
                          │ CardKey             │   │ card4               │
                          │ IdentityKey         │   │ card5               │
                          │ DeviceKey           │   │ card6               │
                          │ AddressKey          │   └─────────────────────┘
                          │ TransactionDT      │
                          │ TransactionAmt     │
                          │ IsFraud            │
                          └─────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
       ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
       │  dim_identity   │ │   dim_device    │ │  dim_address    │
       │─────────────────│ │─────────────────│ │─────────────────│
       │ IdentityKey     │ │ DeviceKey       │ │ AddressKey      │
       │ id_01           │ │ DeviceType      │ │ addr1           │
       │ id_02           │ │ DeviceInfo      │ │ addr2           │
       │ ...             │ └─────────────────┘ │ dist1           │
       │ id_38           │                     │ dist2           │
       └─────────────────┘                     └─────────────────┘
```

---

## 17. Próximos Passos

Com o modelo dimensional definido, a implementação do DWH seguirá esta sequência:

1. Criar o schema `dwh`, caso ainda não exista.
2. Criar as dimensões.
3. Criar a tabela fato.
4. Definir primary keys e foreign keys.
5. Implementar os registros `Unknown`.
6. Implementar a carga ODS → dimensões.
7. Implementar a carga ODS → fato.
8. Validar contagens e integridade referencial.
9. Criar consultas de validação analítica.
10. Preparar o modelo para consumo pelo Power BI.
11. Definir posteriormente a estratégia específica de preparação de dados para Machine Learning.

---

## 18. Status

**Status:** Modelagem dimensional definida.

**Próxima etapa:** Implementação física do Data Warehouse no SQL Server.
