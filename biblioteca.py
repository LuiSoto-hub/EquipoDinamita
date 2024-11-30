from datetime import datetime, timedelta


class Libro:
    def __init__(self, titulo, autor, cantidad_ejemplares):
        self.titulo = titulo
        self.autor = autor
        self.cantidad_ejemplares = cantidad_ejemplares


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.prestamos = []  # Lista de préstamos activos
        self.sancion_hasta = None  # Fecha hasta la que no puede tomar préstamos

    def puede_prestar(self):
        if self.sancion_hasta and self.sancion_hasta > datetime.now():
            return False, f"Sancionado hasta {self.sancion_hasta.strftime('%Y-%m-%d')}"
        if len(self.prestamos) >= 3:
            return False, "Ya tiene el máximo permitido de libros en préstamo"
        return True, "Puede tomar un préstamo"


class Prestamo:
    def __init__(self, usuario, libro, fecha_prestamo):
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_prestamo + timedelta(weeks=1)

    def calcular_retraso(self):
        if datetime.now() > self.fecha_devolucion:
            return (datetime.now() - self.fecha_devolucion).days
        return 0


class Biblioteca:
    def __init__(self):
        self.libros = {}  # Diccionario de libros disponibles
        self.prestamos = []  # Lista de préstamos activos

    def agregar_libro(self, titulo, autor, cantidad_ejemplares):
        if titulo in self.libros:
            self.libros[titulo].cantidad_ejemplares += cantidad_ejemplares
        else:
            self.libros[titulo] = Libro(titulo, autor, cantidad_ejemplares)

    def prestar_libro(self, usuario, titulo):
        # Verificar disponibilidad del libro
        if titulo not in self.libros or self.libros[titulo].cantidad_ejemplares <= 0:
            return f"No hay ejemplares disponibles del libro '{titulo}'"
        
        # Verificar si el usuario puede tomar préstamos
        puede_prestar, mensaje = usuario.puede_prestar()
        if not puede_prestar:
            return mensaje

        # Registrar el préstamo
        libro = self.libros[titulo]
        libro.cantidad_ejemplares -= 1
        prestamo = Prestamo(usuario, libro, datetime.now())
        self.prestamos.append(prestamo)
        usuario.prestamos.append(prestamo)
        return f"Préstamo registrado: {usuario.nombre} tomó '{titulo}'"

    def devolver_libro(self, usuario, titulo):
        for prestamo in usuario.prestamos:
            if prestamo.libro.titulo == titulo:
                # Calcular retraso y sanción
                dias_retraso = prestamo.calcular_retraso()
                if dias_retraso > 0:
                    usuario.sancion_hasta = datetime.now() + timedelta(days=dias_retraso * 3)
                
                # Registrar devolución
                usuario.prestamos.remove(prestamo)
                prestamo.libro.cantidad_ejemplares += 1
                self.prestamos.remove(prestamo)
                return f"Libro '{titulo}' devuelto. Retraso: {dias_retraso} días"
        return f"El usuario no tiene el libro '{titulo}' en préstamo"
