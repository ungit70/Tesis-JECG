
class estructura_econ(object):
    """Representacion de relaciones economicas"""

    def focupConsumo(self):
        """funcion de ocupacion de consumo del sistema"""
        # aqui se determina el valor de la demanda de trabajo
        # requerido por el sector productor de bienes de consumo
        # @NOTE:el capital se determina dentro de la dinamica
        # economica
        self.lc = ((self.deco)/(self.tc*(self.kc ** self.alpc))
                   ) ** (1/self.betc)

    def focupInver(self):
        """funcion de ocupacion de inversion del sistema"""
        # aqui se determina el valor de la demanda de trabajo
        # requerido por el sector productor de bienes de capital
        # el capital se determina dentro de la dinamica
        # economico
        self.li = ((self.decinv)/(self.tin*(self.kinv ** self.alpin))) ** (1/self.betin)


    def fprodConsumo(self):
        """funcion de produccion consumo"""
        # la funcion instancia los datos
        # de los parametros de los metodos
        # anteriores
        self.zc = self.tc * (self.kc ** self.alpc) * (self.lc ** self.betc)


    def fprodInver(self):
        """funcion de produccion inversion"""
        # la funcion instancia los datos
        # de los parametros de los metodos
        # anteriores
        self.zi  = self.tin * (self.kinv ** self.alpin) * (self.li ** self.betin)
