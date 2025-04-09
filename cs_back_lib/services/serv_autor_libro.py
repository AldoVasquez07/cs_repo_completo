from services.serv_autor import ServAutor
from services.serv_libro import ServLibro
from entity.autor_libro import AutorLibros, LibroAutores
from utils.constants import Constants


class ServAutorLibro:
    def __init__(self, conn):
        self.conn = conn
        self.serv_autor = ServAutor(conn)
        self.serv_libro = ServLibro(conn)
        
    def get_autor_libros(self, id):
        libros = []
        
        query = """
            SELECT
                id_autor,
                id_libro
            FROM autor_libro
            WHERE id_autor = %s;
        """
        
        try:
            resultado = self.conn.execute(query, args=(id,))
            for registro in resultado:
                libros.append(
                    self.serv_libro.get_libro(registro[1])
                )
        except Exception as e:
            print("Error a buscar los libros por Autor:", e)
        
        return AutorLibros(
            self.serv_autor.get_autor(id),
            libros
        )
        
    
    def insert_libro_autor(self, id_autor, id_libro):
        if not self.serv_autor.get_autor(id_autor):
            return "El autor que desea connectar no existe"

        if not self.serv_libro.get_libro(id_libro):
            return "El libro que desea connectar no existe"
        
        al = self.get_autor_libros(id_autor)

        for libro in al.libros:
            if id_libro == libro.id:
                return "El libro y el autor ya están conectados"
            
        query = """
        INSERT INTO autor_libro (id_autor, id_libro) VALUES (%s, %s);
        """
        
        try:
            self.conn.execute(query, args=(id_autor, id_libro), commit=True)
            return Constants.insercion_correcta
        except Exception as e:
            message = f"Error al insertar el libro al autor: {e}"
            print(message)
            return message
            
        
    def update_libro_autor(self, id_autor, id_libro, id_libro_nuevo):
        if not self.serv_autor.get_autor(id_autor):
            return "El autor que desea actualizar no existe"

        if not self.serv_libro.get_libro(id_libro):
            return "El libro que desea actualizar no existe"
        
        if not self.serv_libro.get_libro(id_libro_nuevo):
            return "El libro nuevo que desea actualizar no existe"
        
        
        al = self.get_autor_libros(id_autor)

            
        query = """
            UPDATE autor_libro
            SET id_libro = %s
            WHERE id_autor = %s and id_libro = %s;
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(id_libro_nuevo, id_autor, id_libro), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id_autor)
            
            return Constants.actualizacion_correcta
        except Exception as e:
            message = f"Error al actualizar el libro al autor: {e}"
            print(message)
            return message
    
    
    def get_libro_autores(self, id):
        autores = []
        
        query = """
            SELECT
                id_autor,
                id_libro
            FROM autor_libro
            WHERE id_libro = %s;
        """
                
        try:
            resultado = self.conn.execute(query, args=(id,))
            for registro in resultado:
                autores.append(
                    self.serv_autor.get_autor(registro[0])
                )
        except Exception as e:
            print("Error al obtener los Autores por libro:", e)
        
        return LibroAutores(
            self.serv_libro.get_libro(id),
            autores
        )
        
    
    def update_autor_libro(self, id_libro, id_autor, id_autor_nuevo):
        if not self.serv_autor.get_autor(id_autor):
            return "El autor que desea actualizar no existe"

        if not self.serv_libro.get_libro(id_libro):
            return "El libro que desea actualizar no existe"
        
        if not self.serv_autor.get_autor(id_autor_nuevo):
            return "El autor nuevo que desea actualizar no existe"
        
        
        al = self.get_libro_autores(id_libro)

        query = """
            UPDATE autor_libro
            SET id_autor = %s
            WHERE id_autor = %s and id_libro = %s
        """
        
        try:
            affected_rows = self.conn.execute(query, args=(id_autor_nuevo, id_autor, id_libro), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id_libro)
            
            return Constants.actualizacion_correcta
        except Exception as e:
            message = f"Error al actualizar el libro al autor: {e}"
            print(message)
            return message
        
        
    def delete_autor_libro(self, id_autor, id_libro):
        query = """
            DELETE FROM autor_libro
            WHERE id_autor = %s and id_libro = %s;
        """
        try:
            affected_rows = self.conn.execute(query, args=(id_autor, id_libro), commit=True)
            
            if affected_rows == 0:
                return Constants.registro_inexistente + str(id_autor) + " " + str(id_libro)
            
            return Constants.eliminacion_correcta
        except Exception as e:
            message = f"Error al eliminar el autor: {e}"
            print(message)
            return message
    