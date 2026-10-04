import pickle
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# ============================================================
# CAMINHOS
# ============================================================

# Pasta onde este arquivo implementacao.py está localizado
PASTA = Path(__file__).resolve().parent

BASE_REGRESSAO = (
    PASTA / "datasets" / "dados_tratados.csv"
)

BASE_CLASSIFICACAO = (
    PASTA / "datasets" / "dados_tratados_classificacao.csv"
)

MODELO_REGRESSAO = (
    PASTA / "Regressão" / "modelo_ideb.pkl"
)

MODELO_CLASSIFICACAO = (
    PASTA
    / "Classificação"
    / "orange"
    / "GB_model.pkcls"
)


# ============================================================
# FAIXAS DO IDEB
# ============================================================

FAIXAS = {
    "II": ("Inferior", "0,0 a 2,9"),
    "MI": ("Médio Inferior", "3,0 a 4,9"),
    "MM": ("Médio", "5,0 a 6,9"),
    "MS": ("Médio Superior", "7,0 a 8,9"),
}


# ============================================================
# AVISO
# ============================================================

AVISO = (
    "Obs.: esta escola faz parte da base usada para desenvolver "
    "os modelos.\n"
    "O resultado serve para consulta e não mede a qualidade do modelo."
)


# ============================================================
# CARREGAMENTO DOS MODELOS
# ============================================================

def carregar_modelo_regressao():
    """Carrega o modelo de regressão."""

    if not MODELO_REGRESSAO.exists():
        raise FileNotFoundError(
            f"Modelo de regressão não encontrado:\n"
            f"{MODELO_REGRESSAO}"
        )

    # O modelo foi salvo com outra versão do scikit-learn,
    # por isso o aviso é ignorado somente durante o carregamento.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return joblib.load(MODELO_REGRESSAO)


def carregar_modelo_classificacao():
    """Carrega o modelo de classificação salvo pelo Orange."""

    if not MODELO_CLASSIFICACAO.exists():
        raise FileNotFoundError(
            f"Modelo de classificação não encontrado:\n"
            f"{MODELO_CLASSIFICACAO}"
        )

    # O Orange precisa estar instalado para carregar
    # corretamente o modelo salvo.
    import Orange

    with open(MODELO_CLASSIFICACAO, "rb") as arquivo:
        return pickle.load(arquivo)


# ============================================================
# PREVISÃO — REGRESSÃO
# ============================================================

def prever_regressao(modelo, escola):
    """
    Faz a previsão do IDEB utilizando regressão.

    O modelo guarda os nomes das colunas utilizadas durante
    o treinamento. Usamos essas mesmas colunas e na mesma ordem.
    """

    colunas = list(modelo.feature_names_in_)

    # Verifica se todas as features necessárias existem
    # na escola.
    faltantes = [
        coluna
        for coluna in colunas
        if coluna not in escola.columns
    ]

    if faltantes:
        raise KeyError(
            "Features utilizadas pelo modelo não encontradas "
            f"na base: {faltantes}"
        )

    dados = escola[colunas]

    previsao = modelo.predict(dados)

    return float(previsao[0])


# ============================================================
# AUXILIAR — CATEGORIAS DO ORANGE
# ============================================================

def posicao_da_categoria(variavel, valor):
    """
    Encontra a posição de uma categoria dentro das categorias
    utilizadas pelo Orange.

    O Orange pode guardar categorias como texto enquanto o CSV
    pode trazer o mesmo valor como número.
    """

    for posicao, rotulo in enumerate(variavel.values):

        if rotulo == str(valor):
            return posicao

        try:
            if float(rotulo) == float(valor):
                return posicao

        except (ValueError, TypeError):
            pass

    # Categoria desconhecida
    return np.nan


# ============================================================
# PREVISÃO — CLASSIFICAÇÃO
# ============================================================

def prever_classificacao(modelo, escola):
    """
    Faz a previsão da faixa de IDEB utilizando o modelo
    de classificação do Orange.
    """

    from Orange.data import DiscreteVariable, Table

    # O domínio original contém as variáveis utilizadas
    # pelo modelo durante o treinamento.
    dominio = modelo.original_domain

    valores = []

    for variavel in dominio.attributes:

        if variavel.name not in escola.columns:
            raise KeyError(
                f"A coluna '{variavel.name}' não existe na base."
            )

        dado = escola[variavel.name].iloc[0]

        if isinstance(variavel, DiscreteVariable):

            valores.append(
                posicao_da_categoria(
                    variavel,
                    dado
                )
            )

        else:

            valores.append(
                float(dado)
            )

    # A classe é justamente o que queremos prever,
    # portanto ela recebe NaN.
    tabela = Table.from_numpy(
        dominio,
        np.array([valores]),
        np.array([np.nan])
    )

    # Retorna a classe prevista e as probabilidades.
    posicao, probabilidades = modelo(
        tabela,
        ret=modelo.ValueProbs
    )

    classes = list(
        modelo.domain.class_var.values
    )

    faixa = classes[int(posicao[0])]

    probabilidades = dict(
        zip(
            classes,
            probabilidades[0]
        )
    )

    return faixa, probabilidades


# ============================================================
# EXIBIÇÃO DOS RESULTADOS
# ============================================================

def mostrar_resultado(
    codigo,
    escola_regressao,
    escola_classificacao,
    previsto,
    faixa,
    probabilidades
):
    """Mostra os resultados dos dois modelos."""

    nome = escola_regressao["NO_ENTIDADE"].iloc[0]
    uf = escola_regressao["SG_UF"].iloc[0]

    ideb_real = escola_regressao[
        "IDEB_2025"
    ].iloc[0]

    real = escola_classificacao[
        "ROTULO_IDEB"
    ].iloc[0]

    nome_faixa, intervalo = FAIXAS[faixa]

    print("\n")
    print("=" * 65)
    print("                 RESULTADO DA PREVISÃO")
    print("=" * 65)

    print(f"Escola:       {nome} ({uf})")
    print(f"Código INEP:  {codigo}")

    # --------------------------------------------------------
    # REGRESSÃO
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("REGRESSÃO")
    print("-" * 65)

    print(f"IDEB previsto: {previsto:.2f}")

    # --------------------------------------------------------
    # CLASSIFICAÇÃO
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("CLASSIFICAÇÃO")
    print("-" * 65)

    print(
        f"Faixa prevista: {faixa} - "
        f"{nome_faixa} "
        f"(IDEB {intervalo})"
    )

    print("\nProbabilidade de cada faixa:")

    for sigla, probabilidade in sorted(
        probabilidades.items(),
        key=lambda item: -item[1]
    ):
        nome_categoria, intervalo_categoria = FAIXAS.get(
            sigla,
            ("Desconhecida", "")
        )

        print(
            f"  {sigla} - "
            f"{nome_categoria:<17} "
            f"{probabilidade * 100:5.1f}%"
        )

    # --------------------------------------------------------
    # VALOR REAL DA BASE
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("COMPARAÇÃO COM A BASE")
    print("-" * 65)

    print(
        f"IDEB na base:  {ideb_real:.1f}"
    )

    print(
        f"Faixa na base: {real}"
    )

    # Diferença entre previsão de regressão e IDEB real
    diferenca = abs(
        previsto - float(ideb_real)
    )

    print(
        f"Erro absoluto da regressão: {diferenca:.2f}"
    )

    if faixa == real:
        print(
            "\nClassificação: ACERTOU a faixa desta escola."
        )
    else:
        print(
            "\nClassificação: ERROU a faixa desta escola."
        )

    print("\n" + "-" * 65)
    print(AVISO)

    print("=" * 65)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 65)
    print(
        "       SISTEMA DE PREVISÃO DO IDEB - ENSINO MÉDIO PÚBLICO"
    )
    print("=" * 65)

    # --------------------------------------------------------
    # Carregar as bases
    # --------------------------------------------------------

    try:

        base_regressao = pd.read_csv(
            BASE_REGRESSAO,
            sep=";",
            encoding="utf-8-sig"
        )

        base_classificacao = pd.read_csv(
            BASE_CLASSIFICACAO,
            sep=";",
            encoding="utf-8-sig"
        )

    except FileNotFoundError as erro:

        print(
            f"\nArquivo não encontrado: {erro.filename}"
        )

        return

    except Exception as erro:

        print(
            f"\nErro ao carregar as bases: {erro}"
        )

        return

    # --------------------------------------------------------
    # Modelos
    # --------------------------------------------------------

    modelo_regressao = None
    modelo_classificacao = None

    # --------------------------------------------------------
    # Loop principal
    # --------------------------------------------------------

    while True:

        print("\n" + "-" * 65)
        print(
            "Digite o código INEP da escola."
        )
        print(
            "Digite 'sair' para encerrar."
        )

        texto = input(
            "\nCódigo INEP: "
        ).strip()

        # ----------------------------------------------------
        # Sair
        # ----------------------------------------------------

        if texto.lower() in (
            "sair",
            "exit",
            "q"
        ):

            break

        # ----------------------------------------------------
        # Validar código
        # ----------------------------------------------------

        if not texto.isdigit():

            print(
                "\nCódigo inválido."
                "\nDigite somente números."
            )

            continue

        if len(texto) != 8:

            print(
                "\nCódigo inválido."
                "\nO código INEP deve ter exatamente 8 números."
            )

            continue

        codigo = int(texto)

        # ----------------------------------------------------
        # Buscar escola na base de regressão
        # ----------------------------------------------------

        escola_regressao = base_regressao[
            base_regressao["CO_ENTIDADE"] == codigo
        ]

        if escola_regressao.empty:

            print(
                "\nEscola não encontrada."
                "\nA base contém somente escolas públicas "
                "de ensino médio."
            )

            continue

        # ----------------------------------------------------
        # Buscar escola na base de classificação
        # ----------------------------------------------------

        escola_classificacao = base_classificacao[
            base_classificacao["CO_ENTIDADE"] == codigo
        ]

        if escola_classificacao.empty:

            print(
                "\nA escola foi encontrada na base de regressão,"
                " mas não foi encontrada na base de classificação."
            )

            continue

        # ----------------------------------------------------
        # Executar os dois modelos
        # ----------------------------------------------------

        try:

            # ================================================
            # REGRESSÃO
            # ================================================

            if modelo_regressao is None:

                print(
                    "\nCarregando modelo de regressão..."
                )

                modelo_regressao = (
                    carregar_modelo_regressao()
                )

            previsto = prever_regressao(
                modelo_regressao,
                escola_regressao
            )

            # ================================================
            # CLASSIFICAÇÃO
            # ================================================

            if modelo_classificacao is None:

                print(
                    "Carregando modelo de classificação..."
                )

                modelo_classificacao = (
                    carregar_modelo_classificacao()
                )

            faixa, probabilidades = (
                prever_classificacao(
                    modelo_classificacao,
                    escola_classificacao
                )
            )

            # ================================================
            # MOSTRAR RESULTADOS
            # ================================================

            mostrar_resultado(
                codigo,
                escola_regressao,
                escola_classificacao,
                previsto,
                faixa,
                probabilidades
            )

        # ----------------------------------------------------
        # Tratamento de erros
        # ----------------------------------------------------

        except FileNotFoundError as erro:

            print(
                f"\nModelo não encontrado:"
                f"\n{erro}"
            )

        except ImportError:

            print(
                "\nO Orange não está instalado."
                "\nInstale com:"
                "\n  pip install orange3"
            )

        except KeyError as erro:

            print(
                f"\nColuna não encontrada:"
                f"\n{erro}"
            )

        except Exception as erro:

            print(
                f"\nErro inesperado:"
                f"\n{type(erro).__name__}: {erro}"
            )

        # ----------------------------------------------------
        # Próxima escola
        # ----------------------------------------------------

        resposta = input(
            "\nPressione ENTER para consultar outra escola "
            "ou digite 'sair' para encerrar: "
        ).strip()

        if resposta.lower() in (
            "sair",
            "exit",
            "q"
        ):

            break

    print(
        "\nPrograma encerrado."
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except (KeyboardInterrupt, EOFError):

        print(
            "\n\nPrograma encerrado."
        )
