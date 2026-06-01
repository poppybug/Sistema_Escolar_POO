from Clases.Usuario import Usuario

class Profesor(Usuario):
    def __init__(self, id_usuario, username, password, correo, nombre_completo, especialidad):
        super().__init__(id_usuario, username, password, "Docente", correo, nombre_completo)
        self.especialidad = especialidad