# STG → ODS Load Documentation

**Projeto:** Fraud Analytics Platform  
**Documento:** `13_STG_to_ODS_Load_Documentation.md`  
**Versão:** 1.0  
**Status:** Concluído  
**Camada:** Engenharia de Dados — ETL  
**Tecnologias:** Python, SQL Server, SQLAlchemy, Pandas, SSIS e Visual Studio Community

---

## 1. Objetivo

Documentar a implementação e a validação do processo de carga de dados da camada Staging (STG) para a camada Operational Data Store (ODS) da plataforma Fraud Analytics.

A carga consolida os dados de transações e identidades provenientes das tabelas STG e RAW, preparando uma estrutura integrada para as próximas etapas do Data Warehouse.

A execução do processo é orquestrada por um pacote SSIS, que chama um script Python responsável pela extração, transformação e carga dos dados.

## 2. Arquitetura da solução

O fluxo implementado utiliza os seguintes componentes:

1. **SQL Server:** armazena as tabelas das camadas RAW, STG e ODS.
2. **Python:** executa as consultas, prepara os DataFrames e insere os registros nas tabelas de destino.
3. **SQLAlchemy e PyODBC:** realizam a conexão entre Python e SQL Server.
4. **Pandas:** manipula os dados extraídos e prepara os registros para inserção.
5. **SSIS:** executa e orquestra o script Python por meio de uma tarefa Execute Process Task.

### Fluxo de processamento

```text
SQL Server
    |
    +-- STG: train_transaction
    +-- STG: test_transaction
    |          |
    |          v
    |    Python ETL
    |          |
    |          v
    |    ODS: transactions
    |
    +-- RAW: train_identity
    +-- RAW: test_identity
    |          |
    |          +-- JOIN com as tabelas STG correspondentes
    |          |
    |          v
    |    Python ETL
    |          |
    |          v
    |    ODS: identities

SSIS
  |
  +-- Execute Process Task
          |
          +-- Executa 05_load_ods_data.py
```

## 3. Artefatos implementados

| Artefato | Localização | Responsabilidade |
|---|---|---|
| Script Python | `python/05_load_ods_data.py` | Executar a carga STG/RAW → ODS |
| Script SQL de criação das tabelas | `sql/04_create_ods_tables.sql` | Criar a estrutura das tabelas ODS |
| Projeto SSIS | `ssis/FraudAnalyticsSSIS/` | Organizar a execução do processo |
| Pacote SSIS | `PKG_FraudAnalytics_STG_ODS.dtsx` | Executar o script Python |


## 4. Fontes e destinos

### 4.1. Transações

**Tabelas de origem:**

- `stg.train_transaction`
- `stg.test_transaction`

**Tabela de destino:**

- `ods.transactions`

Os dados das tabelas de treinamento e teste são consolidados em uma única tabela. Para os registros de treinamento, a coluna `isFraud` é obtida da origem. Para os registros de teste, o script atribui `NULL` a essa coluna, pois o rótulo de fraude não está disponível nessa origem.

A carga também registra a origem do conjunto de dados por meio da coluna `data_source`, com os valores `train` ou `test`.

### 4.2. Identidades

**Tabelas de origem:**

- `raw.train_identity`
- `raw.test_identity`
- `stg.train_identity`
- `stg.test_identity`

**Tabela de destino:**

- `ods.identities`

Os dados de identidade são extraídos da camada RAW e combinados com as informações de dispositivo disponíveis na STG por meio de um `LEFT JOIN`, utilizando `TransactionID`.

O script padroniza os nomes das colunas de identidade para o destino ODS e acrescenta os metadados de carga.

## 5. Estratégia de carga

O processo utiliza uma estratégia de recarga completa (*full refresh*).

Antes de inserir os novos registros, o script executa `TRUNCATE TABLE` na tabela de destino correspondente.

Em seguida, os dados são inseridos com `pandas.DataFrame.to_sql()`, utilizando:

- `if_exists="append"`;
- `index=False`;
- `chunksize=5000`;
- `fast_executemany=True` na configuração do engine SQLAlchemy.

A estratégia evita a acumulação de duplicidades entre execuções normais bem-sucedidas, pois as tabelas são esvaziadas antes da recarga.

**Ponto de atenção:** a limpeza e a carga das duas tabelas não estão encapsuladas em uma única transação. Uma falha durante o processo pode deixar uma ou ambas as tabelas parcialmente carregadas. Uma evolução futura deverá avaliar transações, tabelas intermediárias e mecanismos de recuperação.

## 6. Metadados de auditoria

O processo registra metadados para facilitar a rastreabilidade das cargas.

| Coluna | Finalidade |
|---|---|
| `data_source` | Identificar se o registro pertence ao conjunto `train` ou `test` |
| `source_file` | Registrar o nome lógico do arquivo de origem |
| `batch_id` | Identificar a execução da carga |
| `load_date` | Registrar a data e hora da carga |
| `etl_status` | Registrar o estado do processamento |

O `batch_id` é gerado no início da execução por meio de UUID. O status atribuído aos registros carregados é `LOADED`.

Esses metadados permitem acompanhar a origem e a execução associadas aos registros da ODS.

## 7. Implementação do pacote SSIS

Foi criado o projeto `FraudAnalyticsSSIS` no Visual Studio Community, utilizando a extensão SQL Server Integration Services Projects.

O pacote implementado é:

`PKG_FraudAnalytics_STG_ODS.dtsx`

A tarefa **Execute Process Task** foi configurada para chamar o interpretador Python e executar o arquivo `05_load_ods_data.py`.

O diretório de trabalho aponta para a pasta `python` do projeto.

A execução do pacote foi concluída com sucesso, conforme indicado pelo status verde da tarefa no ambiente SSIS.

## 8. Resultados da execução

Após a execução do pacote, foram realizadas consultas de validação no SQL Server.

| Tabela de destino | Registros carregados |
|---|---:|
| `ods.transactions` | 1.097.231 |
| `ods.identities` | 286.140 |
| **Total** | **1.383.371** |

Os valores correspondem às contagens observadas após a execução do pacote.

## 9. Validações realizadas

### 9.1. Contagem de registros

A contagem de registros foi realizada nas duas tabelas ODS.

Resultado: 1.097.231 registros em `ods.transactions` e 286.140 em `ods.identities`.

### 9.2. Unicidade de TransactionID

Foi comparado o total de registros com a quantidade de valores distintos de `TransactionID`.

| Tabela | Total | IDs distintos |
|---|---:|---:|
| `ods.transactions` | 1.097.231 | 1.097.231 |
| `ods.identities` | 286.140 | 286.140 |

Resultado: as contagens são iguais nas duas tabelas, indicando ausência de valores nulos e de duplicidades de `TransactionID` no conjunto consultado.

### 9.3. Metadados ETL

Foram verificados o preenchimento de `batch_id`, `load_date` e o status `LOADED`.

| Tabela | Batch ID preenchido | Load date preenchida | Status LOADED |
|---|---:|---:|---:|
| `ods.transactions` | 1.097.231 | 1.097.231 | 1.097.231 |
| `ods.identities` | 286.140 | 286.140 | 286.140 |

Resultado: todos os registros possuem os campos verificados preenchidos conforme esperado.

### 9.4. Integridade referencial

Foi realizada uma consulta com `LEFT JOIN` entre `ods.identities` e `ods.transactions`, utilizando `TransactionID`.

| Indicador | Resultado |
|---|---:|
| Total de identidades | 286.140 |
| Identidades com transação correspondente | 286.140 |
| Identidades sem transação correspondente | 0 |
| Correspondência | 100% |

Resultado: todas as identidades carregadas possuem uma transação correspondente na tabela de transações.

## 10. Critérios de aceite

| Critério | Resultado |
|---|---|
| Pacote SSIS executado sem erros | Atendido |
| Tabela `ods.transactions` carregada | Atendido |
| Tabela `ods.identities` carregada | Atendido |
| Ausência de duplicidades de `TransactionID` | Atendido |
| Metadados ETL preenchidos | Atendido |
| Correspondência entre identidades e transações | Atendido |

Os critérios acima foram verificados por meio da execução do pacote e das consultas SQL descritas neste documento.

Essas verificações não substituem uma análise completa da qualidade dos atributos, dos valores transformados ou de todos os requisitos de negócio.

## 11. Pontos de atenção e melhorias futuras

As seguintes melhorias podem ser avaliadas em uma próxima iteração:

1. Implementar uma estratégia de recuperação para falhas durante a carga.
2. Avaliar o uso de transações ou tabelas intermediárias para evitar estados parcialmente carregados.
3. Implementar logs persistentes de execução, com status, duração, volumes e mensagens de erro.
4. Validar a qualidade dos atributos e regras de transformação além das contagens e relacionamentos.
5. Avaliar a utilização de restrições de integridade e índices adequados na ODS.
6. Integrar a execução do pacote SSIS ao processo de carga do Data Warehouse, respeitando as dependências entre as etapas.

## 12. Conclusão

A etapa de carga STG → ODS foi implementada e executada com sucesso por meio da integração entre SSIS, Python e SQL Server.

Foram carregados 1.383.371 registros nas tabelas `ods.transactions` e `ods.identities`. As validações confirmaram a unicidade dos identificadores, o preenchimento dos metadados de auditoria e a correspondência de 100% dos registros de identidade com transações existentes.

Com isso, a implementação básica da carga está concluída e validada segundo os critérios descritos neste documento.

A próxima etapa do projeto deverá considerar a integração da camada ODS com o Data Warehouse dimensional e o fortalecimento dos mecanismos de monitoramento e recuperação do ETL.
