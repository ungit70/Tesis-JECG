class calendario(object):
    def cambiar_fecha(self, mes):
        self.fechaPeriodo = f'{self.yearPeriodo}-{mes}-01' if \
            len(str(mes)) > 1 else f'{self.yearPeriodo}-0{mes}-01'
        if mes == self.ciclos[-1]:
            self.yearPeriodo +=1
