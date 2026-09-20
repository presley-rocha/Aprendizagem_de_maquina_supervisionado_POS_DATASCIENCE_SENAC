# Atualizações Recentes do Projeto

**Data:** 20/09/2026  
**Responsável:** Clara Cecilia
**Motivo da atualização:** Solicitação do professor e revisão geral do fluxo do projeto
**obs**: esse arquivo deve ser atualizado com as edições mais recentes toda vez que houver uma nova modificação.

---

## Sumário

- [1. Inclusão de Novos Notebooks](#1-inclusão-de-novos-notebooks)
- [2. Ajuste na Preparação dos Dados — Caminhos Universais](#2-ajuste-na-preparação-dos-dados--caminhos-universais)
- [3. Análise do PCA — Resultado: Não se aplica ao Projeto](#3-análise-do-pca--resultado-não-se-aplica-ao-projeto)
- [4. Status do Notebook 05.Modelagem_Avaliacao.ipynb](#4-status-do-notebook-05modelagem_avaliacaoipynb)
- [5. Resumo das Ações](#5-resumo-das-ações)
- [6. Próximos Passos](#6-próximos-passos)
- [7. Observações](#7-observações)

---

## 1. Inclusão de Novos Notebooks

Foram adicionados três novos arquivos ao repositório, estruturando o pipeline do projeto em etapas claras e sequenciais:

| Arquivo | Descrição |
|---|---|
| `03.analise_correlacao_pca.ipynb` | Análise exploratória de correlação entre as variáveis e verificação da adequação do PCA. |
| `04.Visualizacao_dos_dados.ipynb` | Visualização detalhada das variáveis (distribuições, outliers, colunas relevantes). |
| `05.Modelagem_Avaliacao.ipynb` | Estrutura de treinamento, avaliação e persistência dos modelos de regressão. |

Esses notebooks representam a continuidade do fluxo iniciado pelo `02.Preparacao_dos_dados.ipynb`, cobrindo desde a análise das variáveis até a modelagem final.

---

## 2. Ajuste na Preparação dos Dados — Caminhos Universais

O notebook `02.Preparacao_dos_dados.ipynb` foi ajustado para que os **caminhos dos arquivos sejam universais** e funcionem para qualquer pessoa que clone o repositório.

**Antes:** os caminhos eram absolutos ou específicos da máquina local, exigindo que cada usuário baixasse os arquivos manualmente e ajustasse os caminhos.

**Agora:** os caminhos são relativos à raiz do projeto, permitindo que todos com acesso ao Git consigam executar os notebooks sem necessidade de configurações manuais ou downloads adicionais.

---

## 3. Análise do PCA — Resultado: Não se aplica ao Projeto

Foi realizada a análise de adequação do PCA (Análise de Componentes Principais) no notebook `03.analise_correlacao_pca.ipynb`. **Conclusão: o PCA não se aplica a este projeto.**

### Motivos:

1. **Baixa correlação interna entre as variáveis:** O Teste de Bartlett retornou p-valor próximo de 1.0, indicando que as variáveis do Censo Escolar não possuem correlação suficiente para compressão eficiente via PCA.

2. **Variáveis complementares, não redundantes:** As variáveis do Censo Escolar descrevem **dimensões distintas** da realidade escolar (infraestrutura, corpo docente, modalidades, localização, etc.). Cada uma carrega informação única — o PCA, ao buscar redundância, descartaria informação relevante.

3. **Objetivo é predição supervisionada:** Modelos como Random Forest e Gradient Boosting capturam interações complexas entre features sem precisar de redução de dimensionalidade.

**Decisão:** O PCA foi **removido** do pipeline de modelagem. Os modelos serão treinados diretamente sobre as features originais.

---

## 4. Status do Notebook 05.Modelagem_Avaliacao.ipynb

**Status:** ⚠️ **Estruturado, mas ainda não executado.**

O notebook `05.Modelagem_Avaliacao.ipynb` foi criado com a estrutura de código baseada no modelo do professor (CRISP-DM, funções bem definidas, separação treino/teste/validação, avaliação e salvamento do modelo). No entanto, **ele ainda não foi executado** pelos seguintes motivos:

### Pendências antes da execução:

Antes de rodar o modelo, é necessário realizar uma análise aprofundada das variáveis no notebook `04.Visualizacao_dos_dados.ipynb`. Essa análise deve incluir:

1. **Análise visual das variáveis** — distribuições, histogramas, boxplots.
2. **Identificação e remoção de outliers** — valores extremos que podem distorcer o treinamento.
3. **Identificação e remoção de colunas desnecessárias** — variáveis com baixa variância, alta redundância ou que não agregam valor preditivo.

### Fluxo correto antes da execução do modelo:
```
04.Visualizacao_dos_dados.ipynb
        ↓
   Análise das variáveis
   Remoção de outliers
   Remoção de colunas
        ↓
02.Preparacao_dos_dados.ipynb
        ↓
   Atualização do CSV tratado
        ↓
05.Modelagem_Avaliacao.ipynb
        ↓
   Treino e avaliação dos modelos
```


**Importante:** as remoções de outliers e colunas devem ser feitas no notebook `02.Preparacao_dos_dados.ipynb`, para garantir que o CSV `dados_tratados.csv` seja atualizado com os dados já filtrados. Só então o notebook de modelagem pode ser executado com confiança.

---

## 5. Resumo das Ações

| Ação | Status |
|---|---|
| Inclusão dos notebooks 03, 04 e 05 | ✅ Concluído |
| Ajuste de caminhos universais no notebook 02 | ✅ Concluído |
| Análise de adequação do PCA | ✅ Concluído — PCA não se aplica |
| Análise profunda das variáveis (notebook 04) | ⏳ Pendente |
| Remoção de outliers e colunas (notebook 02) | ⏳ Pendente |
| Execução do notebook 05 (modelagem) | ⏳ Aguardando etapas anteriores |

---

## 6. Próximos Passos

1. Executar o notebook `04.Visualizacao_dos_dados.ipynb` e analisar todas as variáveis.
2. Identificar outliers e colunas irrelevantes.
3. Voltar ao notebook `02.Preparacao_dos_dados.ipynb` e aplicar as remoções.
4. Regenerar o arquivo `dados_tratados.csv` com os dados filtrados.
5. Executar o notebook `05.Modelagem_Avaliacao.ipynb` para treinar e avaliar os modelos.
6. Comparar os resultados e selecionar o melhor modelo.

---

## 7. Observações

- A decisão de não usar PCA foi baseada em análise estatística (Teste de Bartlett) e no entendimento da natureza dos dados.
- A estrutura do notebook de modelagem segue o padrão CRISP-DM, alinhada com o exemplo do professor (`projeto.py`).
- Todos os notebooks foram pensados para serem **reprodutíveis** por qualquer pessoa com acesso ao repositório.

---

**Fim do relatório de atualizações.**