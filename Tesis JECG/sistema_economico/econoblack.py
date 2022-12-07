import os
import traceback
import sys
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from sistema_economico.calendario import calendario
from sistema_economico.agentes import agentes
from sistema_economico.estructura_productiva import estructura_econ
from sistema_economico.relaciones_eco import relaciones_econ
from sistema_economico.banco_central import banco_central


class economy(agentes, estructura_econ, relaciones_econ,
            banco_central, calendario):
    """Esta es la clase global de sistema, 
        manda todos los parametros a las funciones"""

    def __init__(self, year=3, cambioPrefe =5,r=0.12, periodo=1, 
                ratedep=0.1, kci=8, kinvi=12, varTcons=0.05, 
                varTin=0.05, xmin=0.18, savmin = 0, savmax = 1):
        # datos de periodo, todas las escalas estan 
        # a un anio
        # 1 = mensual, 2 = trimestral, 3 = semestral 
        self.periodicidad = {1: 13, 2: 4, 3: 3}
        self.finPeriodos = {2: [i for i in range(3, 13, 3)],
                    1: [i for i in range(3, 13, 3)],
                    3: [i for i in range(6, 13, 6)]}

        self.periodosEvaluacion = self.finPeriodos.get(2)
        self.ciclos = [i for i in range(1, self.periodicidad.get(periodo))]
        self.cierres = [i for i in range(1, year+1)]
        # formato fecha yyyy-mm-dd
        
        self.yearInicio = 1870
        self.yearPeriodo = 1870
        self.fechaInicio = '1870-01-01'
        self.years = year
        
        self.infoPoliticaMonet = {}
        self.per = self.periodicidad.get(periodo)
        self.ratedep = ratedep
        self.r = r
        self.save = 0
        self.kc = kci  # capital inicial de consumo
        self.kinv = kinvi  # capital inicial de inversion
        self.cambioPrefe = cambioPrefe
        self.varTcons = varTcons
        self.varTin = varTin
        self.xmin = xmin
        self.savmin = savmin
        self.savmax = savmax


        self.rng = np.random.RandomState(2021)

    def generarSistema(self, freeMarket = None, modelo = 1, maxGenBank = None):
        self.freeMarket = freeMarket
        actividadEcon = []
        try:
            # Nivel de cierre de ciclo (year)
            for cierre in self.cierres:
                
                eCsuma = 0 # error por ciclo de oferta y demanda consumo
                eIsuma = 0 # error por ciclo de oferta y demanda inversion

                # alamcen de informacion de politica monetaria:

                # 1. Calculo de inversion necesaria
                self.demandaCapital()
                # 2. Calculo de ocuipacion necesaria
                self.focupInver() # ocupacion en produccion de bienes de capital
                self.focupConsumo() # ocupacion en produccion de bienes de consumo
                if cierre == 1:
                    self.consaut = self.deco
                    self.save = self.deco
                # Nivel de ciclos productivos (meses)
                for ciclo in self.ciclos:
                    # inicializar / cambiar fechas
                    self.cambiar_fecha(ciclo)

                    # 3. Producir y ofertar
                    # producir bienes de capital
                    self.fprodInver() 
                    # producir bienes de consumo
                    self.fprodConsumo()  
                    #determinar oferta global
                    self.ofertaGlobal() 

                    # 4. Fase de consumo
                    self.consumoEfectivo()

                    # 5. Derterminacion del ahorro total
                    self.ahorroGlobal()

                    # alamcenar resultados del sistema
                    # [year, mes,
                    # demanda total,
                    # consumo, ingreso,
                    # consumo autonomo,
                    # inversion consumo,
                    # inversion capital
                    # oferta global, ahorro]

                    renglonCiclo = [cierre, ciclo, self.c 
                    + self.diffk, self.c, self.y, self.diffk, 
                    self.consaut, self.zc, self.zi, self.z, 
                    self.save, self.r]
                    actividadEcon.insert(len(actividadEcon), renglonCiclo)

                    # guardar informacion para politica monetaria:
                    # la informacion utilizada es trimestral, con
                    # la informacion del trimestre determina si 
                    # es necesario un ajuste de tasas:
                    # la variable es la demanda
                    self.infoPoliticaMonet[self.fechaPeriodo] = self.c + self.diffk
                    #print(ciclo, self.fechaPeriodo, self.infoPoliticaMonet)
                    
                    if not self.freeMarket:
                        if ciclo in self.periodosEvaluacion and cierre != 1:
                            # aplicar politica monetaria el primer 
                            # periodo se toma como informativo
                            self.politca_monetaria(modelo= modelo, maxGenBank= maxGenBank)
                            self.infoPoliticaMonet.clear()

                    # Evaluacion de resultados
                    econs, einver = self.errorDemandas()

                eCsuma += econs
                eIsuma += einver

                # Ajuste de expectativas del ciclo (cierre year)
                self.decinv += eIsuma
                self.deco += eCsuma
                if (cierre + 1) % self.cambioPrefe == 0:
                    self.cambiosPreferencias()

                #descarga de datos del sistema:
                self.f_name = f'{self.ruta}/SISTEMAECOPOLMON.txt' if not self.freeMarket else f'{self.ruta}/SISTEMAECOFREE.txt'
                if os.path.exists(self.f_name):
                    os.remove(self.f_name)
                with open(self.f_name, 'a', newline='') as f:
                    for row in actividadEcon:
                        row = map(str,row)
                        f.write(f"{','.join(row)}\n")
                    #write = csv.writer(f)
                    #write.writerows(actividadEcon)
            print(f'Resultados escritos en {self.ruta}')
            self.resumen_comportamiento()
        except:
            traceback.print_exc(file=sys.stdout)

        