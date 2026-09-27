# Atualizações Recentes do Projeto

**Data:** 22/09/2026  
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

**Status:** ✅ **Pronto para execução após atualização da base tratada.**

O notebook `05.Modelagem_Avaliacao.ipynb` foi criado com a estrutura de código baseada no modelo do professor (CRISP-DM, funções bem definidas, separação treino/teste/validação, avaliação e salvamento do modelo). A execução deve usar o CSV tratado atualizado após a análise visual do notebook `04.Visualizacao_dos_dados.ipynb`.

### Pendências antes da execução:

As pendências abaixo foram verificadas e tratadas:

1. **Análise visual das variáveis** — distribuições, histogramas e boxplots adicionados ao notebook 04.
2. **Identificação e remoção de outliers** — removidas linhas com código sentinela `88888` e indicadores `IN_*` fora do domínio binário `0/1`.
3. **Identificação e remoção de colunas desnecessárias** — removidas variáveis de baixa variância, alta redundância e identificadores/textos que não entram diretamente no modelo.

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


**Importante:** as remoções de outliers e colunas foram aplicadas no notebook `02.Preparacao_dos_dados.ipynb`, garantindo que o CSV `dados_tratados.csv` esteja atualizado com os dados já filtrados. O notebook 04 usa o snapshot `dados_tratados_pre_eda.csv` para manter a análise pré-limpeza reproduzível.

### Resultado da limpeza aplicada

| Item | Resultado |
|---|---|
| Shape pré-limpeza | 17.583 linhas × 227 colunas |
| Linhas removidas por código `88888` | 1.326 |
| Linhas removidas por `IN_*` fora de `0/1` | 332 |
| Colunas removidas por baixa variância, redundância ou identificação | 38 |
| Shape final de `dados_tratados.csv` | 15.925 linhas × 189 colunas |
| Colunas não numéricas restantes | 0 |
| NaN restantes | 0 |
| Códigos `88888` restantes | 0 |

### Ajuste adicional no notebook 05

Durante a verificação pré-execução, foi identificado que a estratificação por faixas fixas do IDEB poderia gerar uma faixa com apenas 1 escola, causando erro no `train_test_split`. A divisão do notebook `05.Modelagem_Avaliacao.ipynb` foi ajustada para usar quantis (`pd.qcut`) como bins de estratificação.

Com o CSV limpo, a separação foi validada sem treinar os modelos:

| Conjunto | Registros | Features |
|---|---:|---:|
| Treino | 11.147 | 188 |
| Teste | 2.389 | 188 |
| Validação | 2.389 | 188 |

---

## 5. Resumo das Ações

| Ação | Status |
|---|---|
| Inclusão dos notebooks 03, 04 e 05 | ✅ Concluído |
| Ajuste de caminhos universais no notebook 02 | ✅ Concluído |
| Análise de adequação do PCA | ✅ Concluído — PCA não se aplica |
| Análise profunda das variáveis (notebook 04) | ✅ Concluído |
| Remoção de outliers e colunas (notebook 02) | ✅ Concluído |
| Execução do notebook 05 (modelagem) | ⏳ Pronto para execução |

---

## 6. Próximos Passos

1. Executar o notebook `05.Modelagem_Avaliacao.ipynb` para treinar e avaliar os modelos.
2. Comparar os resultados e selecionar o melhor modelo.
3. Avaliar se ajustes de hiperparâmetros melhoram o desempenho do modelo selecionado.

---

## 7. Observações

- A decisão de não usar PCA foi baseada em análise estatística (Teste de Bartlett) e no entendimento da natureza dos dados.
- A estrutura do notebook de modelagem segue o padrão CRISP-DM, alinhada com o exemplo do professor (`projeto.py`).
- Todos os notebooks foram pensados para serem **reprodutíveis** por qualquer pessoa com acesso ao repositório.

---

**Fim do relatório de atualizações.**
