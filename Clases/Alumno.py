from Clases.Usuario import Usuario

class Alumno(Usuario):
    def __init__(self, id_usuario, username, password, correo, nombre_completo, carrera, semestre):
        super().__init__(id_usuario, username, password, "Alumno", correo, nombre_completo)
        self.carrera = carrera
        self.semestre = semestre
        self.calificaciones = []
        
    def calcular_promedio(self):
        if not self.calificaciones:
            return 0
        suma = sum(c.valor_numerico for c in self.calificaciones) 
        return suma / len(self.calificaciones)