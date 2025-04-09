from entity.autor import Autor
from utils.constants import Constants

class ServAutor:
    def __init__(self, conn):
        self.conn = conn
        
    def get_autores(self):
        autores = []
        
        query = """
            SELECT
                a.id,
                a.cod,
                (a.nombre || ' ' || a.apellido_paterno || ' ' || a.apellido_materno) AS nombre
            FROM autor AS a
            WHERE a.flag = true;
        """
        
        try:
            resultado = self.conn.execute(query)
                
            if resultado:
                for registro in resultado:
                    autores.append(Autor(registro[0], registro[1], registro[2]))
        except Exception as e:
            print("Error al seleccionar los autores:", e)
        
        return autores
                
    
    def get_autor(self, id):
        autor = None

        query = """
            SELECT
                a.id,
                a.cod,
                (a.nombre || ' ' || a.apellido_paterno || ' ' || a.apellido_materno) AS nombre
            FROM autor AS a
            WHERE a.flag = true AND a.id = %s;
        """
        try:
            resultado = self.conn.execute(query, args=(id,))
            if resultado:
                for registro in resultado:
                    autor = Autor(registro[0], registro[1], registro[2])
        except Exception as e:
            print("Error al seleccionar el autor:", e)
        
        return autor

        
    def update_autor(self, id, cod, nombre, apellido_paterno, apellido_materno, flag):
        query = """
            UPDATE autor
            SET cod = %s,
                nombre = %s,
                apellido_paterno = %s,
                apellido_materno = %s,
                flag = %s
            WHERE id = %s;
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(cod, nombre, apellido_paterno, apellido_materno, flag, id), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id)
            
            return Constants.actualizacion_correcta
        except Exception as e:
            message = f"Error al actualizar autor: {e}"
            print(message)
            return message
    
    
    def insert_autor(self, cod, nombre, apellido_paterno, apellido_materno):
        query = """
            INSERT INTO autor (cod, nombre, apellido_paterno, apellido_materno) VALUES
            (%s, %s, %s, %s);
        """
        
        try:
            self.conn.execute(query, args=(cod, nombre, apellido_paterno, apellido_materno), commit=True)
            return Constants.insercion_correcta
        except Exception as e:
            message = f"Error al insertar el autor: {e}"
            print(message)
            return message
        
        
    def delete_autor(self, id):
        query = """
            UPDATE autor
            SET flag = false
            WHERE id = %s
        """
        try:
            affected_rows = self.conn.execute(query, args=(id,), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id)
            
            return Constants.eliminacion_correcta
        except Exception as e:
            message = f"Error al eliminar el autor: {e}"
            print(message)
            return message
    