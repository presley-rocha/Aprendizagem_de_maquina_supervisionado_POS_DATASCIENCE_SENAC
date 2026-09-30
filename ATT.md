---

# Atualizações Recentes do Projeto

**Data:** 27/09/2026
**Responsável:**Clara Cecilia
**Motivo da atualização:** Reestruturação do repositório para suportar os dois tipos de modelo (Regressão e Classificação) e desenvolvimento inicial da pipeline de Classificação no Orange.

---

## Sumário

- [1. Reestruturação das Pastas — Separação Regressão / Classificação](#1-reestruturação-das-pastas--separação-regressão--classificação)
- [2. Novos Arquivos de Dataset](#2-novos-arquivos-de-dataset)
- [3. Pipeline de Classificação — Orange](#3-pipeline-de-classificação--orange)
- [4. Notebook de Tratamento para Classificação](#4-notebook-de-tratamento-para-classificação)
- [5. Notebook de Análise de Resultados — Classificação](#5-notebook-de-análise-de-resultados--classificação)
- [6. Resumo das Ações](#6-resumo-das-ações)
- [7. Próximos Passos](#7-próximos-passos)
- [8. Observações](#8-observações)

---

## 1. Reestruturação das Pastas — Separação Regressão / Classificação

O repositório foi reorganizado para separar claramente os artefatos de cada tipo de modelo, evitando mistura de arquivos e facilitando a manutenção paralela das duas abordagens.

### Estrutura anterior
4_Projeto_Orange/
Workflow_data_treinig_teste.ows
Workflow_treinando_model.ows
datasets/
treining_data.tab
teste_data.tab
datasets/
modelo_ideb.pkl
dados_tratados_pre_eda.csv


### Estrutura atual

Regressão/
modelo_ideb.pkl
4_Projeto_Orange/
W_regressao_data_treinig_teste.ows
W_regressao_treinando_model.ows
datasets/
treining_data.tab
teste_data.tab

Classificação/
tratamento_para_classificação.ipynb
Analise_de_resultados.ipynb
orange/
W_classificacao_split.ows
W_regressao_treinando_model.ows ← workflow de classificação no Orange
GB_model.pkcls ← modelo Gradient Boosting serializado
data/
dados_treino_classificacao.tab
dados_teste_classificacao.tab
dados__resultados_teste_classificacao.csv


### O que mudou por arquivo

| Arquivo / Pasta | Ação |
|---|---|
| `4_Projeto_Orange/` (raiz) | Movida para `Regressão/4_Projeto_Orange/` |
| `Workflow_data_treinig_teste.ows` | Renomeado para `W_regressao_data_treinig_teste.ows` |
| `Workflow_treinando_model.ows` | Renomeado para `W_regressao_treinando_model.ows` |
| `datasets/modelo_ideb.pkl` | Movido para `Regressão/modelo_ideb.pkl` |
| `datasets/dados_tratados_pre_eda.csv` | Renomeado para `datasets/dados_brutos.csv` |
| `Classificação/` | Criada — contém todos os artefatos da pipeline de classificação |

> **Importante:** os notebooks comuns (`02`, `03`, `04`) e os datasets base (`dados_tratados.csv`, ZIPs originais) permanecem em `2_NoteBooks_Etapas_Projeto/` e `datasets/`, sem alteração de localização. Os notebooks comuns não foram modificados em conteúdo — apenas ajustes cosméticos menores (espaçamento entre células).

---

## 2. Novos Arquivos de Dataset

Três novos arquivos foram adicionados à pasta `datasets/`:

| Arquivo | Descrição |
|---|---|
| `dados_brutos.csv` | Renomeação de `dados_tratados_pre_eda.csv`. Mesmo conteúdo (17.583 linhas × 227 colunas) — snapshot anterior às limpezas orientadas pela EDA. O nome novo descreve melhor o papel do arquivo no fluxo. |
| `dados_tratados_classificacao.csv` | Dataset derivado de `dados_tratados.csv` com a coluna `ROTULO_IDEB` adicionada. Gerado pelo notebook `tratamento_para_classificação.ipynb`. Contém 17.583 linhas × 228 colunas (227 features + target discretizado). |
| `notas_IDEB_anteriores.xlsx` | Planilha com histórico de notas IDEB das escolas de ensino médio nas edições de 2017, 2019, 2021 e 2023. Contém aproximadamente 22.185 registros e 60 colunas. Incluída como referência de contexto histórico para análises futuras — não é usada no treinamento dos modelos atuais. |

---

## 3. Pipeline de Classificação — Orange

Foi desenvolvida a pipeline de Classificação no Orange Data Mining, composta por dois workflows e um modelo treinado:

### `W_classificacao_split.ows`

Responsável pela geração e exportação dos conjuntos de treino e teste para classificação.

- Lê `dados_tratados_classificacao.csv` (com `ROTULO_IDEB` como target)
- Aplica `Data Sampler` para divisão treino/teste estratificada
- Exporta `dados_treino_classificacao.tab` e `dados_teste_classificacao.tab`

### `W_regressao_treinando_model.ows` (dentro de `Classificação/orange/`)

Apesar do nome, este workflow **treina e avalia classificadores**, não regressores. O nome é um resquício da origem do workflow e deve ser corrigido em uma próxima atualização.

Algoritmos testados:

| Algoritmo | Tipo |
|---|---|
| Naive Bayes | Classificação |
| SVM | Classificação |
| Random Forest | Classificação |
| Neural Network | Classificação |
| Gradient Boosting | Classificação |

A avaliação usa `Test and Score` (com métricas de classificação) e `Confusion Matrix`. O melhor modelo (Gradient Boosting) foi salvo em `GB_model.pkcls`.

### `dados__resultados_teste_classificacao.csv`

Arquivo de saída do Orange com as probabilidades previstas pelo Gradient Boosting para cada escola do conjunto de teste. Contém as colunas `ROTULO_IDEB` (real), `Gradient Boosting (II)`, `(MI)`, `(MM)` e `(MS)`. Usado como entrada do notebook `Analise_de_resultados.ipynb`.

> **Observação:** As classes `SS` (Superior, IDEB 9,0–10) e `SR` (Sem Rendimento) não aparecem nos resultados de probabilidade porque não existem registros suficientes dessas faixas no dataset para o modelo aprendê-las. As classes presentes no modelo são: `II`, `MI`, `MM`, `MS`.

---

## 4. Notebook de Tratamento para Classificação

**Arquivo:** `Classificação/tratamento_para_classificação.ipynb`

Este notebook transforma o target contínuo `IDEB_2025` em rótulos categóricos e gera visualizações de distribuição das classes.

### Função de discretização

A classificação segue a tabela oficial de rendimento escolar:

| Rótulo | Significado | Faixa IDEB |
|---|---|---|
| SS | Superior | 9,0 a 10 |
| MS | Médio Superior | 7,0 a 8,9 |
| MM | Médio | 5,0 a 6,9 |
| MI | Médio Inferior | 3,0 a 4,9 |
| II | Inferior | 0,0 a 2,9 |
| SR | Sem Rendimento | Zero ou nulo |

### Distribuição resultante no dataset

| Rótulo | Quantidade | % |
|---|---:|---:|
| MI | 13.517 | 76,9% |
| MM | 3.756 | 21,4% |
| II | 270 | 1,5% |
| MS | 40 | 0,2% |
| SS | 0 | — |
| SR | 0 | — |

> O dataset é fortemente concentrado nas classes `MI` e `MM`, o que reflete o perfil real das escolas públicas de ensino médio brasileiras na edição IDEB 2025. Isso implica desbalanceamento de classes — ponto a considerar no ajuste de hiperparâmetros futuros.

### Visualizações geradas

- Gráfico de barras com contagem e percentual por rótulo
- Gráfico de pizza com proporção das classes
- Barras empilhadas de distribuição por UF
- Boxplot do `IDEB_2025` por rótulo (validação visual da discretização)
- Resumo estatístico (count, média, mínimo e máximo por classe)

### Saída

Salva `datasets/dados_tratados_classificacao.csv` com a coluna `ROTULO_IDEB` adicionada ao dataset tratado.

---

## 5. Notebook de Análise de Resultados — Classificação

**Arquivo:** `Classificação/Analise_de_resultados.ipynb`

Notebook de avaliação pós-treino, que consome o CSV de resultados gerado pelo Orange e produz análises detalhadas de desempenho do Gradient Boosting.

### Métricas calculadas

- Acurácia global
- F1-score macro e weighted
- Precisão e Recall macro
- Relatório completo por classe (`classification_report`)

### Visualizações

- Matriz de confusão absoluta (heatmap)
- Matriz de confusão normalizada por linha (recall visual, em %)
- Distribuição real vs. prevista por classe (barras agrupadas)
- Distribuição da confiança do modelo (histograma + boxplot por classe)
- Tabela de erros: casos mal classificados com maior confiança

### Métricas gerais (conjunto de teste — 5.274 registros)

| Métrica | Valor |
|---|---:|
| Acurácia | **0.8106** |
| F1 macro | 0.4459 |
| F1 weighted | 0.7870 |
| Precisão macro | 0.5313 |
| Recall macro | 0.4159 |

### Desempenho por classe

| Classe | Suporte real | Previstos | Acertos | Recall | Precisão | F1 | Confiança média |
|---|---:|---:|---:|---:|---:|---:|---:|
| II — Inferior | 81 | 33 | 15 | 18,52% | 45% | 0.26 | 0.7175 |
| MI — Médio Inferior | 4.054 | 4.633 | 3.850 | **94,97%** | 83% | 0.89 | 0.8298 |
| MM — Médio | 1.127 | 595 | 408 | 36,20% | 69% | 0.47 | 0.6878 |
| MS — Médio Superior | 12 | 13 | 2 | 16,67% | 15% | 0.16 | 0.9468 |

### Principais confusões do modelo

| Real → Previsto | Quantidade |
|---|---:|
| MM → MI | 714 |
| MI → MM | 180 |
| II → MI | 66 |
| MI → II | 17 |
| MI → MS | 7 |
| MS → MM | 7 |

> **Interpretação:** O modelo acerta bem a classe dominante `MI` (95% de recall), mas tem dificuldade nas classes minoritárias. A confusão principal é entre `MM` e `MI` — classes adjacentes na escala do IDEB — o que é esperado dado o desbalanceamento acentuado (76,9% dos registros são `MI`). O desempenho nas classes `II` e `MS` é baixo por falta de exemplos de treino suficientes.

---

## 6. Resumo das Ações

| Ação | Status |
|---|---|
| Reestruturação das pastas (Regressão / Classificação) | ✅ Concluído |
| Renomeação dos workflows Orange de Regressão | ✅ Concluído |
| Movimentação do `modelo_ideb.pkl` para `Regressão/` | ✅ Concluído |
| Renomeação de `dados_tratados_pre_eda.csv` → `dados_brutos.csv` | ✅ Concluído |
| Adição de `notas_IDEB_anteriores.xlsx` | ✅ Concluído |
| Notebook de tratamento e discretização para Classificação | ✅ Concluído |
| Geração de `dados_tratados_classificacao.csv` | ✅ Concluído |
| Pipeline Orange de Classificação (split + treino + modelo) | ✅ Concluído |
| Notebook de análise de resultados da Classificação | ✅ Concluído |
| Execução de `Analise_de_resultados.ipynb` e registro de métricas | ✅ Concluído |
---

## 7. Próximos Passos


1. Avaliar o desbalanceamento das classes (`MI` = 76,9%) e decidir se aplicar técnicas de balanceamento (SMOTE, class_weight) antes de uma nova rodada de treino.
2. Desenvolver o notebook Python equivalente ao pipeline Orange de Classificação (`05.Modelagem_Avaliacao_Classificacao.ipynb`) para manter paridade com o notebook de Regressão.

---

## 8. Observações

- O `dados_tratados.csv` **não foi alterado** — continua sendo a base comum para Regressão e Classificação.
- Os notebooks `02`, `03` e `04` **não sofreram alterações de conteúdo** — apenas ajustes cosméticos menores de espaçamento interno que não afetam a execução.
- O modelo Orange de Classificação (`GB_model.pkcls`) é um classificador Gradient Boosting, distinto do modelo de Regressão (`modelo_ideb.pkl`). Os dois não são intercambiáveis.
- A forte concentração nas classes `MI` e `MM` era esperada e reflete o perfil real das escolas públicas brasileiras — não é um problema de preparação dos dados.

---

**Fim do relatório de atualizações.**