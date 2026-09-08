### 💻  Aprendizado de Máquina Supervisionado
# Projeto: Análise de Dados e Machine Learning (Python / Orange)

> **Trabalho realizado pelos alunos:** Até 4 alunos  
> **Ferramentas sugeridas:** Python (Pandas, Matplotlib, Seaborn, Scikit-Learn) ou Orange Data Mining 

<div style="display: inline-block; background-color: white; padding: 60px; border-radius: 80px;">
  <img align="center" alt="Python" height="250" width="550" src="https://www.databricks.com/sites/default/files/inline-images/Unsupervised-Learning-Diagram.png">  
</div>
---

## 0º Contextualizar o DataSet
* **Objetivo do Dataset:** 
  * [Descrever aqui o problema de negócio ou o propósito analítico do conjunto de dados]
* **Dicionário de Dados (Detalhamento das Colunas):**
 <!--  * `[Nome_Coluna_1]`: [Descrição do tipo de dado, significado e unidade de medida]
  * `[Nome_Coluna_2]`: [Descrição do tipo de dado, significado e unidade de medida]
  * `[Coluna_Alvo / Target]`: [Variável que será prevista ou analisada]-->
---

## 1º Carregar o Dataset
* **Importação dos Dados:** 
  * Realizar a leitura do arquivo `.csv` que está no projeto na pasta `1_DataSet` o arquivo está como `.zip` utilizando bibliotecas adequadas (ex: `pd.read_csv()` no Pandas).
* **Inspeção Inicial:**
  * Verificação das primeiras e últimas linhas (`head()` / `tail()`).
  * Análise preliminar de dimensões (linhas e colunas) e tipos de dados estruturais (`info()`).

---

## 2º Realizar Tratamento de Colunas e Linhas
* **Limpeza de Dados:**
  * Identificação e tratamento de valores ausentes (`NaN`, nulos ou lacunas).
  * Tratamento de linhas duplicadas e registros inconsistentes/inválidos.
* **Ajustes de Tipos:**
  * Conversão de tipos de dados (ex: strings para numéricos, datas, categorias).
* **Seleção de Atributos:**
  * Remoção de colunas irrelevantes, redundantes ou com alta taxa de ruído.

---

## 3º Realizar Análise Gráfica dos Dados (EDA)
* **Visualização Univariada:**
  * Gráficos de distribuição, histogramas e boxplots para entender a dispersão das variáveis numéricas e contagens para as categóricas.
* **Visualização Bivariada / Multivariada:**
  * Matriz de correlação (heatmap) para identificar relações lineares entre variáveis.
  * Gráficos de dispersão (`scatter plots`) cruzando variáveis preditoras com a variável alvo.
* *Ferramentas aplicadas:* Matplotlib, Seaborn, vamos tentar também com os componentes gráficos nativos do Orange (Box Plot, Scatter Plot, Distributions).

---

## 4º Separar os Arquivos de Treino, Teste e Validação
* **Estratificação da Amostra:**
  * Divisão do dataset seguindo a proporção solicitada:
    * **Treino:** 70% dos dados (aprendizado dos padrões pelos algoritmos).
    * **Teste:** 15% dos dados (avaliação de desempenho intermediária/ajuste de hiperparâmetros).
    * **Validação:** 15% dos dados (avaliação final de generalização com dados totalmente blindados).
* *Método:* Utilização de funções de divisão aleatória ou estratificada (ex: `train_test_split` do Scikit-Learn ou no Orange).

---

## 5º Treinar Diferentes Algoritmos de IA Destinados ao Objetivo
* **Modelagem Preditiva / Aprendizado de Máquina:**
  * Seleção e treinamento de múltiplos algoritmos compatíveis com o problema (ex: Regressão Logística, Árvores de Decisão, Random Forest, SVM, KNN, entre outros).
* **Ajuste de Hiperparâmetros:**
  * Otimização inicial dos parâmetros de cada modelo para extrair melhor desempenho dos dados de treino.

---

## 6º Analisar as Métricas dos Algoritmos
* **Avaliação de Desempenho:**
  * Comparação dos resultados obtidos nos conjuntos de teste e validação utilizando métricas adequadas ao tipo de problema (ex: Acurácia, Precisão, Revocação / *Recall*, F1-Score, Matriz de Confusão ou MSE/RMSE para regressão).
* **Seleção do Melhor Modelo:**
  * Justificativa da escolha do algoritmo com base na performance geral e estabilidade frente aos dados de validação.

---

## 7º Implantar em Produção
* **Estratégia de Deploy:**
  * Documentação e estruturação de como o modelo treinado será disponibilizado para uso real (ex: salvamento do modelo com `joblib`/`pickle`, criação de uma API simples via FastAPI/Flask, script automatizado em Python ou fluxo operacional exportado via Orange).
* **Monitoramento:**
  * Considerações para acompanhamento da performance do modelo em ambiente produtivo.