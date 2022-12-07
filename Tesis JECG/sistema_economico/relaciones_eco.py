class relaciones_econ(object):
    """Sistema de relacione economicas del modelo"""

    def ingresoGlobal(self):
        """ingreso global igual a la demanda de trabajo"""
        self.y = self.lc + self.li


    def ofertaGlobal(self):
        """oferta global del sistema economico"""
        self.z = self.zi + self.zc


    def consumoEfectivo(self):
        """demanda de consumo efectiva"""

        # determinacion del ingreso disponible
        self.ingresoGlobal()

        # determinacion del consumo autonomo

        self.consaut = self.rng.uniform(
            low=self.gsave*self.save, high=self.save)

        if self.consaut < 0:
            self.consaut = 0

        self.c = (self.x * (self.y)) + self.consaut  # consumo total

    # <<<< FUNCION [AHORRO SISTEMA] >>>> #

    def ahorroGlobal(self):
        inventarios = self.zc - self.c
        ahorroIngreso = self.y - (self.x * (self.y))
        self.save += (inventarios + ahorroIngreso) - self.consaut


    def demandaCapital(self):
        """demanda de capital"""
        # el capital se determina al cierre
        # del ejercicio con base en los resultados
        # la demanda de capital solo se calcula para el sector
        # de bienes de consumo.
        self.kg = self.kc + self.kinv
        kn = (self.deco * (self.r / self.per) * self.per)
        diffk = kn - self.kc
        if diffk < 0:
            diffk = 0
        self.diffk = diffk
        self.decinv = (self.kg * self.ratedep) + diffk
        self.kc = self.kc + diffk - (self.kc * self.ratedep)
        self.kinv = self.kinv + \
            (self.kinv * self.ratedep) - (self.kinv * self.ratedep)
        self.kg = self.kc + self.kinv


    def errorDemandas(self):
        self.epsic = self.c - self.zc
        self.epsii = self.decinv - self.zi
        return self.epsic, self.epsii


    def cambiosPreferencias(self):
        self.xmax = 1
        self.x = self.rng.uniform(low=self.xmin, high=self.xmax)
        self.gsave = self.rng.uniform(low=self.savmin, high=self.savmax)
        self.tin += self.varTin  # 0.05
        self.tc += self.varTcons  # 0.05

