from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
from scipy.stats import chi2
import scipy
import numpy as np

def getDatos(path:str, encabezados:list):
    with open(path, 'r', encoding='utf-8') as f:
        datosPol = pd.read_csv(f, sep=',', names=encabezados)
    return datosPol


def makeCompareDf(dataFrameA: object, dataFrameB: object,
                namesA: object, namesB: object, 
                  compareNameA: list, compareNameB: list):
    compare = pd.DataFrame()
    for num, _ in enumerate(compareNameA):
        compare[compareNameA[num]] = dataFrameA[namesA[num]]
    for num, _ in enumerate(compareNameB):
        compare[compareNameB[num]] = dataFrameB[namesB[num]]
    return compare


def ver_componentes(variable: str, datos:object, periodo=12, titulo=None):
    result = seasonal_decompose(
        datos[variable], model='aditive', period=periodo)
    fig = result.plot()
    fig.set_size_inches(18, 10, forward=True)
    if titulo:
        fig.suptitle(titulo, fontsize=30)
    return result


def f_test(x, y):
    x = np.array(x)
    y = np.array(y)
    # calculate F test statistic
    f = np.var(y, ddof=len(y)-1)/np.var(x, ddof=len(x)-1)
    dfn = x.size-1  # define degrees of freedom numerator
    dfd = y.size-1  # define degrees of freedom denominator
    print(np.var(x, ddof=len(x)-1), np.var(y, ddof=len(y)-1), dfn, dfd)
    p = 1-scipy.stats.f.cdf(f, dfn, dfd)  # find p-value of F test statistic
    ftabla = scipy.stats.f.ppf(1-0.05, dfn, dfd)
    return f, p, ftabla


def diffvarchi(comparacion, base, alpha=0.05):
    if len(comparacion) != len(base):
        return 'No se pueden comparar datos'
    else:
        varBase = np.var(base)
        varcomparacion = np.var(comparacion)
        print(varcomparacion, varBase)
        freedgrComp = len(comparacion) - 1
        freedgrBase = len(base) - 1
        chiBase = chi2.ppf(1-alpha, freedgrBase)
        chiComp = (freedgrComp*varcomparacion)/varBase

        if chiBase > chiComp:
            return f'{chiBase} > {chiComp}'
        else:
            return f'{chiBase} < {chiComp}'


def diferencia_medias_krwall(dataFrameDatos: object, lisTupVarsComparar: list):
    resultados = {}
    for tupla in lisTupVarsComparar:
        resultados[f'Prueba KW de media \n \
        para variables {tupla}'] = stats.kruskal(dataFrameDatos[tupla[0]],
                                dataFrameDatos[tupla[1]])
        print(f'{tupla[0]}:Media:{dataFrameDatos[tupla[0]].mean()}')
        print(f'{tupla[0]}:Varianza:{dataFrameDatos[tupla[0]].var()}')
        print(f'{tupla[1]}:Media: {dataFrameDatos[tupla[1]].mean()}')
        print(f'{tupla[1]}:Varianza: {dataFrameDatos[tupla[1]].var()}')
        print('---------------')
    return resultados


def graficas_comparacion(dataFrameDatos: object, lisVarsComparar: list, datosTexto: dict):
    titulo = datosTexto.get('titulo')
    xname = datosTexto.get('xname')
    yname = datosTexto.get('yname')
    serieName1 = datosTexto.get('serie1')
    serieName2 = datosTexto.get('serie2')

    fig, ax = plt.subplots(figsize=(25, 12))
    fig.suptitle(
        titulo, fontsize=25)
    dataFrameDatos[lisVarsComparar][:].plot(ax=ax, 
            fontsize=16)
    ax.set_xlabel(xname, fontweight='bold')
    ax.set_ylabel(yname, fontweight='bold')

    L = plt.legend()
    L.get_texts()[0].set_text(serieName1)
    L.get_texts()[1].set_text(serieName2)
    return plt


def graficar_comparacion(dataFrame: object, variablesComparar: list, textoTitulo: str):
    fig, ax = plt.subplots(figsize=(20, 10))
    fig.suptitle(
        textoTitulo, fontsize=16)
    dataFrame[variablesComparar][:
                                ].plot(ax=ax, fontsize=16)
    return plt


def espacio_valido():
    rng = np.random.RandomState(2021)
    numGenesAlpBet = 2
    numGenesRate = 1
    poblacionBase = 4000
    elementoRate = (poblacionBase, numGenesRate)
    elementosAphjBet = (poblacionBase, numGenesAlpBet)
    genesAlphaBetha = rng.uniform(0.01, 1.0, size=elementosAphjBet)
    genesRate = rng.uniform(low=0.01, high=0.5, size=elementoRate)
    poblacion = np.concatenate((genesRate, genesAlphaBetha), axis=1)
    df = pd.DataFrame(poblacion, columns=['Tasa', 'Alpha', 'Beta'])
    fig = plt.figure(figsize=(20, 12))
    ax = plt.axes(projection='3d')
    plt.title("Region aceptable de parámetros", fontweight="bold", fontsize=20)
    ax.set_xlabel('Parámetro Alpha', fontweight='bold')
    ax.set_ylabel('Parámetro Beta', fontweight='bold')
    ax.set_zlabel('Tasa de interés', fontweight='bold')

    ax.scatter3D(df.Alpha, df.Beta, df.Tasa, color='Black')
    ax.yaxis.label.set_color('Black')
    ax.xaxis.label.set_color('Red')
    ax.zaxis.label.set_color('Blue')
    return ax
