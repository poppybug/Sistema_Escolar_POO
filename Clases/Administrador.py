from Clases.Usuario import Usuario

class Administrador(Usuario):
    def __init__(self, id_usuario, username, password, correo, nombre_completo="Administrador General"):
        # super() pasa los datos al padre correctamente
        super().__init__(id_usuario, username, password, "Admin", correo, nombre_completo)
            
    def verificar_credenciales(self, user_input, pass_input, lista_global):
        for u in lista_global:
            if (str(u.id_usuario) == user_input or u.correo == user_input) and u.password == pass_input:
                return u
        return None