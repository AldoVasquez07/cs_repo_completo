from security.connection import PostgreSQLPool
from entity.usuario import Usuario


class ServUsuario:
    def __init__(self, conn):
        self.conn = conn
        
    def get_usuario(self, name, password):
        usuario = None
        
        query = """
            SELECT nombre, password_user FROM usuario WHERE nombre = %s AND password_user = %s;
        """
        
        try:
            resultado = self.conn.execute(query, args=(name, password))
            
            if resultado:
                for registro in resultado:
                    usuario = Usuario(registro[0], registro[1])
        except Exception as e:
            print("Error al seleccionar el usuario:", e)
        
        return usuario            
            
                