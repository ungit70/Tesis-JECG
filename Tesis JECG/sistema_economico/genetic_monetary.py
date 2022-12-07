import random
import numpy as np


class banqueroGenetico(object):
    """ Metodo de desicion de banco central por Algoritmo Genetico
    genes = [r, p1, p2]
    cromosomas = 46
    poblacionAleatoriaOriginal = []
    """

    def ajusteEntrada(self, sujeto):
        # funcion objetivo
        r = sujeto[0]
        p1 = sujeto[1]
        p2 = sujeto[2]
        demandaCalculada = (self.demandaReal * p1*100) / (r - 2 + 2*p2 + p1*100)
        ajuste = self.demandaPotencial - demandaCalculada
        return abs(ajuste)


    def seleccionar_padres(self, poblacion, ajuste, numProgenitores, maxGenBank):
        # metodo de seleccion de padres
        progenitores = np.zeros((numProgenitores, poblacion.shape[1]))
        asacendencia = 0
        while len(poblacion) > 1:
            renglonCandidato = np.where(ajuste == np.min(ajuste))[0][0]
            progenitores[asacendencia, :] = poblacion[renglonCandidato, :]
            ajuste = np.delete(ajuste, renglonCandidato, 0)
            poblacion = np.delete(poblacion, renglonCandidato, 0)
        return progenitores


    def herencia(self, padres, descendencia):
        # generacion de hijos
        hijos = np.empty(descendencia)
        padreIndex1 = 0
        numIndividuo = 0
        while True:
            padreIndex2 = padreIndex1 + 1
            if padreIndex1 > len(padres)-1 or len(padres) == 1:
                break
            ascendente1 = padres[padreIndex1]
            ascendente2 = padres[padreIndex2]
            hijos[numIndividuo, 0] = min(ascendente1[0], ascendente2[0])
            hijos[numIndividuo, 1] = min(ascendente1[1], ascendente2[1])
            hijos[numIndividuo, 2] = min(ascendente1[2], ascendente2[2])
            numIndividuo += 1
            padreIndex1 += 2
        return hijos

    def determinacionPolitica(self, modelo, poblacionBase=4000, maxGenBank=None):
        # determinacion de politica por caso Algoritmo Genetico
        anterior = None
        gen = 1
        continuarProceso = True
        numGenesAlpBet = 2
        numGenesRate = 1
        comparador1 = np.array([0.01, 0.001, 0.001])

        elementosAphjBet = (poblacionBase, numGenesAlpBet)
        elementoRate = (poblacionBase, numGenesRate)

        # poblacion inicial
        genesAlphaBetha = self.rng.uniform(0.01, 1.0, size=elementosAphjBet)
        genesRate = self.rng.uniform(low=0.01, high=0.5, size=elementoRate)

        poblacion = np.concatenate((genesRate, genesAlphaBetha), axis=1)

        # este es el caso aleatorio
        if modelo == 0:
            # camino opcional:
            # seleccionar al mejor en la poblacion inicial de los 4000
            individuo = random.choice([item for item in range(poblacionBase)])
            parametros = poblacion[individuo]
            anterior = parametros
            renglonStop = parametros
            gen = 1
            return parametros, anterior, renglonStop, gen

        # caso para multiples generaciones
        while continuarProceso:
            numAntecesores = int(len(poblacion)/2)

            # esto retorna los mejores candidatos 
            # de la generacion
            resultadosPoblacionBase = np.apply_along_axis(
                self.ajusteEntrada, -1, poblacion)
            # el numero de progenitores debe ser divisible entre 2
            # seleccionados por ajuste
            padres = self.seleccionar_padres(
                poblacion, resultadosPoblacionBase, numAntecesores, maxGenBank)

            # condicion de salida por numero
            # maximo de generaciones
            if maxGenBank:
                if gen == maxGenBank:
                    #print(padres[0])
                    renglonStop = padres[0]
                    anterior = renglonStop
                    parametros = renglonStop
                    continuarProceso = False
                    return parametros, anterior, renglonStop, gen

            # retorno de hijos con base en mejores genes
            detalleDescendencia = (int(numAntecesores/2), 3)  # numero de hijos
            hijos = self.herencia(padres, detalleDescendencia)
            
            renglonStop = np.where(resultadosPoblacionBase ==
                                np.min(resultadosPoblacionBase))[0][0]
            
            renglonStop = poblacion[renglonStop, :]
            salida = np.logical_or(renglonStop < comparador1[0],
                                    renglonStop < comparador1[1],
                                    renglonStop < comparador1[2])


            # condicion de salida de proceso
            # por restriccion
            if salida.all:
                parametros = renglonStop
                continuarProceso = False
            # continuar proceso 
            elif not salida.all and not maxGenBank:
                poblacion = hijos
                anterior = renglonStop
            gen += 1

        return parametros, anterior, renglonStop, gen