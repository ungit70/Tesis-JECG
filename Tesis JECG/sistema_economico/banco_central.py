import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
from sistema_economico.genetic_monetary import banqueroGenetico

class banco_central(banqueroGenetico):
    """_representacion de banco central con desicion tomada por Algoritmo Genetico"""
    def politca_monetaria(self, modelo, maxGenBank = None):
        df = pd.DataFrame(list(self.infoPoliticaMonet.items()),
                        columns=['fecha', 'demandaTotal'])
        fechas = df['fecha'].values.tolist()
        index = pd.period_range(fechas[0], fechas[-1], freq='M')
        df.set_index(index, inplace=True)
        
        #print(df)
        # aplicar filtro
        cycle, trend = sm.tsa.filters.hpfilter(df.demandaTotal, 129600)
        gdp_decomp = df[['demandaTotal']]
        gdp_decomp["cycle"] = cycle
        gdp_decomp["trend"] = trend
        
        # gdp_decomp is pd.DF 
        # tendencia producto:
        self.demandaPotencial = gdp_decomp["trend"].mean()
        self.demandaReal = df['demandaTotal'].mean()
        
        # parametros = (None, None, None, None)

        # while parametros[0] is None and parametros[1] is None:
        #     print('calculando')
        #     parametros = self.determinacionPolitica(maxGenBank=maxGenBank)
        #     print(parametros[0])

        parametros = self.determinacionPolitica(modelo, maxGenBank=maxGenBank)
        paramTaylor = list(parametros[0])
        self.r = paramTaylor[0]


    def resumen_comportamiento(self):
        encabezados = ['year', 'periodo', 'demandaTotal',
            'consumo', 'ingreso', 'demandaCapital',
            'consumoAuto', 'ksCon', 'ksInv','ofertaGlob',
            'save', 'tasaInteres']


        with open(self.f_name, 'r', encoding='utf-8') as f:
            datos = pd.read_csv(f, sep=',', names=encabezados)

        fechaFin = self.fechaPeriodo
        index = pd.period_range(self.fechaInicio, fechaFin, freq='M')
        datos.set_index(index, inplace=True)

        # aplicar filtro
        cycle, trend = sm.tsa.filters.hpfilter(datos.ofertaGlob, 129600)
        gdp_decomp = datos[['demandaTotal']]
        gdp_decomp["cycle"] = cycle
        gdp_decomp["trend"] = trend

        fig, ax = plt.subplots(figsize=(20, 10))
        gdp_decomp[["demandaTotal", "cycle", "trend"]
                    ][:].plot(ax=ax, fontsize=16)
        fig.suptitle(
            'Demanda y tendencia de la demanda en todo el periodo', fontsize=20)

        plt.figure(figsize=(20, 10))
        plt.plot(range(len(datos)), datos['tasaInteres'])
        plt.suptitle(
            'Tasas de interes determinadas por Banco Central', fontsize=20)
        plt.show()