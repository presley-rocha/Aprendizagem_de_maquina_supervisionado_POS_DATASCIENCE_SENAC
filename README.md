# Projeto: Análise de Dados e Machine Learning (Python / Orange)

> **Trabalho realizado pelos alunos:**
> * Clara Freitas
> * Flávia Rosa
> * Itagiba Neto 
> * Bruno Presley
> * Leonardo Castro
> 
  **Bibliotecas** (Pandas, Matplotlib, Seaborn, Scikit-Learn)
> **Ferramentas sugeridas:** VS Code, Python, Orange Data Mining

---

## 0º Contextualizar o DataSet
* **Objetivo do Dataset:** 
  * ----- Descrever a contextualização do nosso trabalho com descrição sobre o Censo Escolar e sobre a prova do Ibeb, descrever também sobre o nosso objetivos do trabalho ------

  links para leitura e entendimento do negócio 
  *[Censo Escolar](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-escolar)
  
  *[Avaliação do Ibeb](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb)

* **Dicionário de Dados (Detalhamento das Colunas):**
  * Para entendimento das variáveis do Dataset sobre o Censo Escolar use o Dicionário de dados em anexo ao projeto.
  * [01.Endendimento_dos_dados.md](https://github.com/presley-rocha/Aprendizagem_de_maquina_supervisionado_POS_DATASCIENCE_SENAC/blob/main/2_NoteBooks_Etapas_Projeto/01.Entendimento_dos_dados.md)
---

## 1º Sobre os Datasets
* **Dados compactados**
  *Nesse projeto trabalhamos com dois datasets que estão compactados
  `IBED_Escolas_Ensino_medio_2025.zip` são os dados das escolas de ensino médio e suas respectivas notas no Ideb.
  `Tabela_Escola_2025_INEP.zip` são dados das escolas apartit do Censo Escolar realizado pelo INEP.
* **Importação dos Dados:** 
  * Realizar a leitura dos arquivos `.csv` que estão compactados`.zip` utilizando bibliotecas adequadas (ex: `pd.read_csv()` e zipfile.ZipFile).
* **Inspeção Inicial:**
  * Verificação das primeiras e últimas linhas (`head()` / `tail()`).
  * Análise preliminar de dimensões (linhas e colunas) e tipos de dados estruturais (`info()`).

---

## 2º Realizar Tratamento de Colunas e Linhas (Em construção)
* **Limpeza de Dados:**
  * Identificação e tratamento de valores ausentes (`NaN`, nulos ou lacunas).
  * Tratamento de linhas duplicadas e registros inconsistentes/inválidos.
* **Ajustes de Tipos:**
  * Conversão de tipos de dados (ex: strings para numéricos, datas, categorias).
* **Seleção de Atributos:**
  * Remoção de colunas irrelevantes, redundantes ou com alta taxa de ruído.

---

## 3º Realizar Análise Gráfica dos Dados (EDA) (Em construção)
* **Visualização Univariada:**
  * Gráficos de distribuição, histogramas e boxplots para entender a dispersão das variáveis numéricas e contagens para as categóricas.
* **Visualização Bivariada / Multivariada:**
  * Matriz de correlação (heatmap) para identificar relações lineares entre variáveis.
  * Gráficos de dispersão (`scatter plots`) cruzando variáveis preditoras com a variável alvo.
* *Ferramentas aplicadas:* Matplotlib, Seaborn, vamos tentar também com os componentes gráficos nativos do Orange (Box Plot, Scatter Plot, Distributions).

---

## 4º Separar os Arquivos de Treino, Teste e Validação (Em construção)
* **Estratificação da Amostra:**
  * Divisão do dataset seguindo a proporção solicitada:
    * **Treino:** 70% dos dados (aprendizado dos padrões pelos algoritmos).
    * **Teste:** 15% dos dados (avaliação de desempenho intermediária/ajuste de hiperparâmetros).
    * **Validação:** 15% dos dados (avaliação final de generalização com dados totalmente blindados).
* *Método:* Utilização de funções de divisão aleatória ou estratificada (ex: `train_test_split` do Scikit-Learn ou no Orange).

---

## 5º Treinar Diferentes Algoritmos de IA Destinados ao Objetivo (Em construção)
* **Modelagem Preditiva / Aprendizado de Máquina:**
  * Seleção e treinamento de múltiplos algoritmos compatíveis com o problema (ex: Regressão Logística, Árvores de Decisão, Random Forest, SVM, KNN, entre outros).
* **Ajuste de Hiperparâmetros:**
  * Otimização inicial dos parâmetros de cada modelo para extrair melhor desempenho dos dados de treino.

---

## 6º Analisar as Métricas dos Algoritmos (Em construção)
* **Avaliação de Desempenho:** 
  * Comparação dos resultados obtidos nos conjuntos de teste e validação utilizando métricas adequadas ao tipo de problema (ex: Acurácia, Precisão, Revocação / *Recall*, F1-Score, Matriz de Confusão ou MSE/RMSE para regressão).
* **Seleção do Melhor Modelo:**
  * Justificativa da escolha do algoritmo com base na performance geral e estabilidade frente aos dados de validação.

---

## 7º Implantar em Produção (Em construção)
*Se der tempo tentar implantar algum sistema pequeno que utilize o modelo.