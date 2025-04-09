from services.serv_libro import ServLibro
from services.serv_genero import ServGenero
from entity.libro_genero import LibroGeneros, GeneroLibros
from utils.constants import Constants


class ServLibroGenero:
    def __init__(self, conn):
        self.conn = conn
        self.serv_libro = ServLibro(conn)
        self.serv_genero = ServGenero(conn)


    def get_libro_generos(self, id):
        generos = []
        
        query = """
            SELECT
                id_libro,
                id_genero
            FROM libro_genero
            WHERE id_libro = %s;
        """
        
        try:
            resultado = self.conn.execute(query, args=(id,))
            for registro in resultado:
                generos.append(
                    self.serv_genero.get_genero(registro[1])
                )    
        except Exception as e:
            print("Error al buscar los generos del libro:", e)
            
        return LibroGeneros(
            self.serv_libro.get_libro(id),
            generos
        )


    def insert_libro_genero(self, id_libro, id_genero):
        if not self.serv_genero.get_genero(id_genero):
            return "El genero que desea connectar no existe"
        
        if not self.serv_libro.get_libro(id_libro):
            return "El libro que desea connectar no existe"
        
        lg = self.get_libro_generos(id_libro)
        
        for genero in lg.generos:
            if id_genero == genero.id:
                return "El libro y el autor ya están conectados"
            
        query = """
        INSERT INTO libro_genero (id_libro, id_genero) VALUES (%s, %s);
        """
        
        try:
            self.conn.execute(query, args=(id_libro, id_genero), commit=True)
            return Constants.insercion_correcta
        except Exception as e:
            message = f"Error al insertar el genero al libro: {e}"
            print(message)
            return message
        
        
    def update_libro_genero(self, id_libro, id_genero, id_genero_nuevo):
        if not self.serv_libro.get_libro(id_libro):
            return "El libro que desea connectar no existe"
        
        if not self.serv_genero.get_genero(id_genero):
            return "El genero que desea connectar no existe"
        
        if not self.serv_genero.get_genero(id_genero_nuevo):
            return "El genero nuevo que desea connectar no existe"
        
        query = """
            UPDATE libro_genero
            SET id_genero = %s
            WHERE id_libro = %s and id_genero = %s;
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(id_genero_nuevo, id_libro, id_genero), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id_libro)
            
            return Constants.actualizacion_correcta
        except Exception as e:
            message = f"Error al actualizar el genero al libro: {e}"
            print(message)
            return message


    def get_genero_libros(self, id):
        libros = []
        
        query = """
            SELECT
                id_libro,
                id_genero
            FROM libro_genero
            WHERE id_genero = %s;
        """
        
        try:
            resultado = self.conn.execute(query, args=(id,))
            for registro in resultado:
                libros.append(
                    self.serv_libro.get_libro(registro[0])
                )
        except Exception as e:
            print("Error al obtener los libros por genero:", e)
        
        return GeneroLibros(
            self.serv_genero.get_genero(id),
            libros
        )
        
    
    def update_genero_libro(self, id_genero, id_libro, id_libro_nuevo):
        if not self.serv_autor.get_autor(id_genero):
            return "El genero que desea actualizar no existe"

        if not self.serv_libro.get_libro(id_libro):
            return "El libro que desea actualizar no existe"
        
        if not self.serv_libro.get_libro(id_libro_nuevo):
            return "El libro nuevo que desea actualizar no existe"
        

        query = """
            UPDATE libro_genero
            SET id_libro = %s
            WHERE id_genero = %s and id_libro = %s;
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(id_libro_nuevo, id_genero, id_libro), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id_genero)
            
            return Constants.actualizacion_correcta
        except Exception as e:
            message = f"Error al actualizar el libro al genero: {e}"
            print(message)
            return message
        
        
    def delete_libro_genero(self, id_libro, id_genero):
        query = """
            DELETE FROM libro_genero
            WHERE id_libro = %s and id_genero = %s;
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(id_libro, id_genero), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + "(" + str(id_libro) + ", " + str(id_genero) + ")"
            
            return Constants.eliminacion_correcta
        except Exception as e:
            message = f"Error al eliminar el autor: {e}"
            print(message)
            return message
    