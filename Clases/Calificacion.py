from Clases.Materia import Materia

class Calificacion:
    def __init__(self, valor_numerico, objeto_materia: Materia):
        self.valor_numerico = valor_numerico
        self.materia = objeto_materia