class Usuario:
    def __init__(self, id_usuario, username, password, rol, correo, nombre_completo):
        self.id_usuario = id_usuario
        self.username = username
        self.password = password
        self.rol = rol
        self.correo = correo
        self.nombre_completo = nombre_completo
        self.estado_cuenta = "Activo"
        
    def verificar_credenciales(self, user, pwd):
        return self.username == user and self.password == pwd