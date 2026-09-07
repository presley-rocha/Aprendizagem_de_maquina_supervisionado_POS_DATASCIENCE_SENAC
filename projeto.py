# Projeto apresentado na diciplina
# CRISP-DM: preparação de dados fase 3
import pandas as pd
import numpy as np
import pickle

# CRISP-DM: análise de dados fase 3 - 123
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# CRISO-DM fase 4
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn import svm

# CRISO-DM fase 5
from sklearn.metrics import accuracy_score

NOMEARQUIVO = "Titanic-Dataset.csv"
NOMEMODELO = "titanic-modelo.pickle"


def carregarDados(nomeArquivo):

    dados = None
    try:
        dados = pd.read_csv(nomeArquivo, sep=",")

    except:
        print("Não foi possivel carregar os dados")

    return dados


def prepararDados(dados):

    # retorna dados básicos sobre o arquivo/dataset carregado
    # qtd colunas, qtd registros não nulos, tipo das colunas
    print(dados.info())

    # 5 primeiros registros do dataset
    print(dados.head())

    # 5 ultimos registros do dataset
    print(dados.tail())

    # retorna estatistica básicas dos campos do dadaset
    print(dados.describe())

    # remover os dados duplicados
    # dados = dados.drop_duplicates()
    dados.drop_duplicates(inplace=True)

    # remover as colunas
    dados.drop(columns=['Cabin', 'Name',
               'PassengerId', 'Ticket'], inplace=True)

    # remove todos os dados nulos
    dados.dropna(inplace=True)

    # decodifica dados categoricos em valores numericos
    lb = LabelEncoder()
    dados['Sex'] = lb.fit_transform(dados['Sex'])
    dados['Embarked'] = lb.fit_transform(dados['Embarked'])
    print(dados.info())
    print(dados.head())
    print(dados.shape)
    print(dados.values)

    # mater valores entre 0 e 62 (inclusive)
    dados = dados[dados["Age"].between(0, 60, inclusive="neither")]
    dados = dados[dados["Fare"].between(0, 55, inclusive="neither")]

    return dados


def gerarBoxplot(dados):
    fig, ax = plt.subplots()
    ax.set_ylabel('boxplot variáveis do Titanic')

    for n, col in enumerate(dados.columns):
        if col == 'Age' or col == 'Fare':
            ax.boxplot(dados[col], positions=[n+1])

    plt.title("Boxplot da coluna Age")
    plt.ylabel("Valores")
    plt.show()


def visualizarDados(dados):

    dados['Age'].hist()
    plt.show()

    dados['Embarked'].hist()
    plt.show()

    gerarBoxplot(dados)

    dados['Survived'].hist()
    plt.show()

    graficoBarras(dados)


def contarColunas(dados, coluna, valor):
    # dados[coluna] = (dados[coluna] == valor).count
    return None


def graficoBarras(dados):
    fig, ax = plt.subplots()

    # valor0 = dados.loc(dados['Survived', 'Nome'] == 0).count()
    # valor1 = dados[dados['Survived'] == 1].count()

    fruits = ['0', '1']
    counts = [40, 50]
    bar_labels = ['red', 'blue']
    bar_colors = ['tab:red', 'tab:blue']

    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel('Coluna Survived')
    ax.set_title('Coluna Survived')
    ax.legend(title='Survived')

    plt.show()


def separarDados(dados):
    print("Separar os dados de treino e teste")

    # separando o objetivo de estratificação [0,1] -- lista 70% e 30%
    Y = dados["Survived"]  # variavel dependente/alvo/target
    X = dados.drop(['Survived'], axis=1)  # variaveis independentes/feature

    # dadosTreino, dadosTeste = train_test_split(dados, test_size=0.3, train_size=0.7, stratify=Y)
    x_train, x_test, y_train, y_test = train_test_split(X, Y,
                                                        test_size=0.3,
                                                        train_size=0.7,
                                                        shuffle=True,
                                                        random_state=42,
                                                        stratify=Y)

    return x_train, x_test, y_train, y_test


def treinarModelo(x_train, y_train):
    listaModelos = list()

    # modelos de IA
    listaAlgoritmos = [RandomForestClassifier(n_estimators=100),
                       LogisticRegression(max_iter=1000),
                       GaussianNB(),
                       svm.SVC(),
                       GradientBoostingClassifier(n_estimators=100),
                       MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15, ), max_iter=1000)]

    # treinar modelos de IA
    for algoritmo in listaAlgoritmos:
        try:
            algoritmo.fit(x_train, y_train)
            listaModelos.append(algoritmo)
        except:
            continue

    return listaModelos


def avaliarListaModelos(listaModelos, x_test, y_test):

    listaPredicoes = list()
    listaAcuracia = list()

    # realiza a predição
    for modelo in listaModelos:
        y_pred1 = modelo.predict(x_test)
        listaPredicoes.append(y_pred1)

    # realiza o caluclo da acuracia
    for predModelo in listaPredicoes:
        listaAcuracia.append(accuracy_score(predModelo, y_test))

    print(listaAcuracia)
    print("Melhor Acurácia: "+str(max(listaAcuracia)))

    # modelo de maior acuracia
    modelo = listaAcuracia.index(max(listaAcuracia))

    return listaModelos[modelo]


def salvarModelo(NOMEMODELO, modelo):
    with open(NOMEMODELO, 'wb') as file:
        pickle.dump(modelo, file)


def carregarModelo(NOMEMODELO):
    modelo = None
    with open(NOMEMODELO, 'rb') as file:
        modelo = pickle.load(file)

    return modelo


def validacaoModelo(modelo, x_validacao):
    y_pred = modelo.predict(x_validacao)

    print("Predição:" + str(y_pred))


NOMEARQUIVO = "Titanic-Dataset.csv"

# carregar o conjunto de dados para tretamento - fase 2 do CRISP-DM
dados = carregarDados(NOMEARQUIVO)

if dados is not None:

    # tratamento de dados - fase 3 do CRISP-DM
    dados = prepararDados(dados)

    # visualizar alguns dados de modo gráfico
    visualizarDados(dados)

    # separar os dados de treino e teste
    x_train, x_test, y_train, y_test = separarDados(dados)

    # realizar o treinamento de modelos de IA - Classificacao
    listaModelos = treinarModelo(x_train, y_train)

    # avaliar lista de modelos
    modelo = avaliarListaModelos(listaModelos, x_test, y_test)

    # salvar modelo em formato padronizado
    salvarModelo(NOMEMODELO, modelo)

    # carregar o modelo salvo
    modeloCarregado = carregarModelo(NOMEMODELO)

    # validar o modelo carregado
    x_validacao = x_test  # [0,0,0,0,0,0,0]
    validacaoModelo(modeloCarregado, x_validacao)
