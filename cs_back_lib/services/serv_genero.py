from entity.genero import Genero
from utils.constants import Constants

class ServGenero:
    def __init__(self, conn):
        self.conn = conn
     
    def get_generos(self):
        generos = []
        
        query = """
            SELECT
                g.id,
                g.nombre
            FROM genero AS g
            WHERE g.flag = true;
        """
        
        try:
            resultado = self.conn.execute(query)
            for registro in resultado:
                generos.append(Genero(registro[0], registro[1]))
        except Exception as e:
            print("Error al seleccionar los generos:", e)
            
        return generos
            
    
    def get_genero(self, id):
        genero = None
        
        query = """
            SELECT
                g.id,
                g.nombre
            FROM genero AS g
            WHERE g.flag = true and g.id = %s;
        """
        
        try:
            resultado = self.conn.execute(query, args=(id,))
            if resultado:
                for registro in resultado:
                    genero = Genero(registro[0], registro[1])
        except Exception as e:
            print("Error al seleccionar el genero:", e)
        
        return genero
        
    
    def update_genero(self, id, nombre, flag):
        query = """
            UPDATE genero
            SET nombre = %s,
                flag = %s
            WHERE id = %s
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(nombre, flag, id), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id)
            
            return Constants.actualizacion_correcta
        except Exception as e:
            message = f"Error al actualizar genero: {e}"
            print(message)
            return message
    
    
    def insert_genero(self, nombre):
        query = """
            INSERT INTO genero (nombre) VALUES
            (%s);
        """
        try:
            self.conn.execute(query, args=(nombre,), commit=True)
            return Constants.insercion_correcta
        except Exception as e:
            message = f"Error al insertar el genero: {e}"
            print(message)
            return message
    
    
    def delete_genero(self, id):
        query = """
            UPDATE genero
            SET flag = false
            WHERE id = %s
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(id,), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id)
            
            return Constants.eliminacion_correcta
        except Exception as e:
            message = f"Error al eliminar el genero: {e}"
            print(message)
            return message