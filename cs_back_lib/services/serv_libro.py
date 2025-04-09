from entity.libro import Libro
from services.serv_genero import ServGenero
from utils.constants import Constants

class ServLibro:
    def __init__(self, conn):
        self.conn = conn
        self.serv_genero = ServGenero(self.conn)
    
    def get_libros(self):
        libros = []
        
        query = """
            SELECT
                l.id,
                l.cod,
                l.titulo
            FROM libro AS l
            WHERE l.flag = true;
        """
        
        try:
            resultado = self.conn.execute(query)
            
            for registro in resultado:
                libros.append(
                    Libro(
                        registro[0],
                        registro[1],
                        registro[2]
                    )
                )
        except Exception as e:
            print("Error al seleccionar libros:", e)
        
        return libros
    
    
    def get_libro(self, id):
        libro = None
        
        query = """
            SELECT
                l.id,
                l.cod,
                l.titulo
            FROM libro AS l
            WHERE l.flag = true and l.id = %s;
        """
        
        try:
            resultado = self.conn.execute(query, args=(id,))
            
            for registro in resultado:
                libro = Libro(
                    registro[0],
                    registro[1],
                    registro[2]
                )
        except Exception as e:
            print("Error al seleccionar el libro:", e)
            
        return libro
        
    
    def update_libro(self, id, cod, titulo, flag):
        query = """
            UPDATE libro
            SET cod = %s,
                titulo = %s,
                flag = %s
            WHERE id = %s
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(cod, titulo, flag, id), commit=True)
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id)
            
            return Constants.actualizacion_correcta
        except Exception as e:
            message = f"Error al actualizar el libro: {e}"
            print(message)
            return message
    
    
    def insert_libro(self, cod, titulo):
        query = """
            INSERT INTO libro (cod, titulo) VALUES
            (%s, %s, %s);
        """
        
        try:
            self.conn.execute(query, args=(cod, titulo), commit=True)
            return Constants.insercion_correcta
        except Exception as e:
            message = f"Error al insertar el libro: {e}"
            print(message)
            return message
    
    
    def delete_libro(self, id):
        query = """
            UPDATE libro
            SET flag = false
            WHERE id = %s
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(id,), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id)
            
            return Constants.eliminacion_correcta
        except Exception as e:
            message = f"Error al eliminar el libro: {e}"
            print(message)
            return message