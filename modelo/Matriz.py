import numpy as np
import copy

class Matriz:
    def __init__(self, header, columna_xb, matrix, metodo, FO):
        self._header = header
        self._FO = FO
        self._matrix = np.array(matrix)
        self.columna_xb = columna_xb
        self.columna_zj = []
        self.fila_cj = []
        self._metodo = metodo
        self._setFilaCj()
        self._renglonPivote = None
        self._columnaPivote = None
        self._Z = None
        self._setNewZj()
        self._setZ()
        self._generateZjCj()

    def getZ(self):
        return round(self._Z,3)
    def getZjCj(self):
        for idx, value in enumerate(self._ZjCj):
            self._ZjCj[idx]=round(value,3)
        return self._ZjCj
    def getHeader(self):
        return self._header
    def getFilaCj(self):
        return self.fila_cj
    def getColumnaXb(self):
        return self.columna_xb
    def getMatriz(self):
        return self._matrix
    def getColumnaZj(self):
        return self.columna_zj
    def getColumnaPivote(self):
        return self._columnaPivote
    def getRenglonPivote(self):
        return self._renglonPivote

    def fase1(self):
        matrices_fase1 = []
        while(self._Z != 0.0 and self._continua()):
            self._columnaPivoteFunc()
            self._filaPivoteFunc()
            matrices_fase1.append(copy.deepcopy(self))
            self._setNewXb()
            self._setNewZj()
            self._inverso()
            self._sumarFilas()
            self._setZ()
            self._generateZjCj()
        matrices_fase1.append(copy.deepcopy(self))
        return matrices_fase1

    def datosDeFilaMatriz(self,i):
        fila=[self.columna_zj[i]]
        for idx,valor in enumerate(self._matrix[i]):
            if(idx == (self._matrix[i].size-1)):
                fila.append(self.columna_xb[i])
                fila.append(round(valor,3))
            else:
                fila.append(round(valor,3))
        return fila

    def fase2(self):
        matrices_fase2=[]
        self._eliminarColumnasR()
        self._eliminarFilasR()
        self._setFilaCj(True)
        self._setNewZj()
        self._generateZjCj()
        self._setZ()
        self.imprimir()
        while(self._continua()):
            self._columnaPivoteFunc()
            self._filaPivoteFunc()
            matrices_fase2.append(copy.deepcopy(self))
            self._setNewXb()
            self._setNewZj()
            self._inverso()
            self._sumarFilas()
            self._setZ()
            self._generateZjCj()
        matrices_fase2.append(copy.deepcopy(self))
        return matrices_fase2

    def _continua(self):
        band = False
        for valor in self._ZjCj:
            if self._metodo == "min":
                if valor > 0:
                    band = True
                    break
            else:
                if valor < 0:
                    band = True
                    break
        return band

    def _setFilaCj(self, fase= False):
        if not fase:
            for val in self._header:
                if 'R' in val:
                    self.fila_cj.append(1.0 if self._metodo == "min" else -1.0)
                elif val != 'Y':
                    self.fila_cj.append(0.0)
        else:
            self.fila_cj=[]
            for val in self._header:
                if val !='Y':
                    self.fila_cj.append(float(self._FO[val]) if val in self._FO.keys() else 0.0)

    def _generateZjCj(self):
        self._ZjCj = []
        for i in range(0, len(self._matrix[0])-1):
            dot = np.array(self.columna_zj) * self._matrix[0:,i]
            res = np.sum(dot, axis=0)
            self._ZjCj.append(res - self.fila_cj[i])

    def _setZ(self):
        self._Z = -1
        dot = np.array(self.columna_zj) * self._matrix[0:,-1]
        self._Z = np.sum(dot, axis=0)

    def _sumar(self, fila, times = 1):
        for idx, value in enumerate(self._matrix[fila]):
            self._matrix[fila][idx] = round(value,10) + round((self._matrix[self._renglonPivote][idx] * ((-1) *times)),10)

    def _inverso(self):
        celdaPivote = self._matrix[self._renglonPivote][self._columnaPivote]  
        a = self._matrix[self._renglonPivote] * float(1/celdaPivote)
        self._matrix[self._renglonPivote, :] = a    

    def _filaPivoteFunc(self):
        columnaPivote = self._matrix[0:, self._columnaPivote]
        y = self._matrix[0:,-1]
        res = np.divide(y, columnaPivote, out=np.zeros_like(y), where=columnaPivote!=0)
        valorMax = np.where(res==np.max(res))[0]
        indice = int(valorMax[0] if np.size(valorMax) > 1 else valorMax)

        for i, e in enumerate(res):
            if (e < res[indice] and e > 0):
                indice = i
        self._renglonPivote = indice
    
    # Selecciona el mas positivo del R0 para escoger la columna pivote
    def _columnaPivoteFunc(self):
        res = None
        if(self._metodo == "min"):
            res = max(self._ZjCj)
        else:
            res = min(self._ZjCj)

        self._columnaPivote = self._ZjCj.index(res)
        
    def _sumarFilas(self):
        for idx, fila in enumerate(self._matrix):
            if(idx != self._renglonPivote):
                self._sumar(idx, self._matrix[idx][self._columnaPivote])

    def _setNewXb(self):
        self.columna_xb[self._renglonPivote] = self._header[self._columnaPivote]

    def _setNewZj(self):
        self.columna_zj = [self.fila_cj[self._header.index(value)] for idx, value in enumerate(self.columna_xb) if value in self._header]

    def _eliminarFilasR(self):
        vec_idx=[]
        for idx, valor in enumerate(self.columna_xb):
            if("R" in valor):               
                vec_idx.append(idx)
        for idx, value in enumerate(vec_idx):
            self.columna_xb.pop(value-idx)
            self._matrix = np.delete(self._matrix,(value-idx),axis=0)

    def _eliminarColumnasR(self):
        vec_idx = []
        for idx, valor in enumerate(self._header): 
            if("R" in valor):
                vec_idx.append(idx)
        for idx, value in enumerate(vec_idx):
            self._header.pop(value-idx)
            self._matrix = np.delete(self._matrix,(value-idx),axis=1)

    def estandarizacionFO(self):
        string_R = ''

        for index, value in enumerate(self._header):
            if 'R' in value:
                if self.fila_cj[index] > 0 and index == 0:
                    string_R += value
                elif  self.fila_cj[index] > 0 :
                    string_R += '+' + value
                else:
                    string_R += '-' + value
        return string_R
    
    def respuestaFinal(self):
        responseFinal = []
        for index, value in enumerate(self.columna_xb):
            responseFinal.append([value.upper(), round(self._matrix[index,-1], 3)])
        responseFinal.append(['Z', round(self._Z, 3)])
        return responseFinal
                
    def imprimir(self):
        print(self.fila_cj)
        print(self._header)
        print(self._matrix)
        print(self.columna_xb)
        print(self.columna_zj)
        print(self._ZjCj)
        print(self._Z)
        self.respuestaFinal()
        