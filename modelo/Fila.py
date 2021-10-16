import numpy as np

class Fila:
    def __init__(self, name, fila):
        self._name = name
        self._fila = np.array(fila)

    def inverso(self, pivote):
        if pivote == 0:
            return 0 # TODO
        return np.round(self._fila * (1/pivote), 6)

    def sumar(self, fila, times = 1):
        return np.add(self._fila * times, fila)

    @property
    def name(self):
        return self._name
    
    @property
    def fila(self):
        return self._fila

    @name.setter
    def name(self, name):
        self._name = name

    @fila.setter
    def fila(self, fila):
        self._fila = fila

    def __str__(self):
        return "something"