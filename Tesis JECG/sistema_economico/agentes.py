class agentes(object):
    # <<<< PARAMETROS DE AGENTES ECONOMICOS >>>> #
    def agenteConsumidor(self, xi):
        """parametros de agente consumidor"""
        # para el consuimidor se determinan las condiociones
        # iniciales de su comportamiento
        # self.x = propencion marginal a consumir (keynes, 1936)
        # self.gsave = propencion marginal a ahorrar ver James Duesenberry
        # self.consaut = consumo autonomo
        # self.deco = demanda de consumo esperada inicial
        self.x = xi
        self.gsave = 1 - xi


    def agenteprodConsumo(self, alpci = 0.30, tci = 2, deci = 12):
        """parametros de agente productor"""
        # para el consuimidor se determinan las condiociones
        # iniciales de su comportamiento
        # self.alpha = coeficiente alpha de produccion 
        # self.beta  = coeficiente beta de produccion
        # self.tecnologia = coeficiente de tecnologia
        # todos los terminos modelan una funcion coob - douglas
        self.alpc = alpci         # alpha
        self.betc = 1 - alpci     # beta
        self.tc = tci             # tecnologia
        self.deco = deci


    def agenteprodInver(self, alpin = 0.30  , tin = 2):
        """parametros de agente productor"""
        # para el consuimidor se determinan las condiociones
        # iniciales de su comportamiento
        # self.alpha = coeficiente alpha de produccion 
        # self.beta  = coeficiente beta de produccion
        # self.tecnologia = coeficiente de tecnologia
        # todos los terminos modelan una funcion coob - douglas
        self.alpin = alpin           #alpha
        self.betin = 1 - alpin       #beta
        self.tin = tin               #tecnologia