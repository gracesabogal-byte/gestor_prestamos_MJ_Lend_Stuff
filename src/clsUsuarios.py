"""
pf_Algoritmos
Modulo: clsUsuarios
Gestion de usuarios del sistema MJ Lend-Stuff
"""

import re
import json
import os

ARCHIVO_USUARIOS = os.path.join(os.path.dirname(__file__), "data", "usuarios.json")

class clsUsuarios:
    """
    Clase para gestionar los usuarios del sistema de prestamos.
    pf_Algoritmos
    """

    def __init__(self, nombre, apellido, documento, correo, tiempo_prestamo):
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.correo = correo
        self.tiempo_prestamo = tiempo_prestamo  # 5, 10, 15 o 30 dias

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "documento": self.documento,
            "correo": self.correo,
            "tiempo_prestamo": self.tiempo_prestamo
        }

    @staticmethod
    def from_dict(data):
        return clsUsuarios(
            data["nombre"],
            data["apellido"],
            data["documento"],
            data["correo"],
            data["tiempo_prestamo"]
        )

    # ── Validaciones ──────────────────────────────────────────────────────────

    @staticmethod
    def validar_nombre(nombre):
        """Minimo 3 letras, sin numeros."""
        if len(nombre) < 3:
            return False, "El nombre debe tener al menos 3 letras."
        if any(c.isdigit() for c in nombre):
            return False, "El nombre no puede contener numeros."
        return True, ""

    @staticmethod
    def validar_apellido(apellido):
        """Minimo 3 letras, sin numeros."""
        if len(apellido) < 3:
            return False, "El apellido debe tener al menos 3 letras."
        if any(c.isdigit() for c in apellido):
            return False, "El apellido no puede contener numeros."
        return True, ""

    @staticmethod
    def validar_documento(documento):
        """Entre 3 y 15 digitos, solo numeros."""
        if not documento.isdigit():
            return False, "El documento solo puede contener numeros."
        if not (3 <= len(documento) <= 15):
            return False, "El documento debe tener entre 3 y 15 digitos."
        return True, ""

    @staticmethod
    def validar_correo(correo):
        """Debe tener @ y terminar en .com"""
        patron = r'^[^@]+@[^@]+\.com$'
        if not re.match(patron, correo):
            return False, "El correo debe tener '@' y terminar en '.com'."
        return True, ""

    @staticmethod
    def validar_tiempo_prestamo(tiempo):
        """Solo 5, 10, 15 o 30 dias."""
        if tiempo not in [5, 10, 15, 30]:
            return False, "El tiempo de prestamo debe ser 5, 10, 15 o 30 dias."
        return True, ""

    # ── Persistencia ─────────────────────────────────────────────────────────

    @staticmethod
    def _asegurar_directorio():
        os.makedirs(os.path.dirname(ARCHIVO_USUARIOS), exist_ok=True)

    @staticmethod
    def cargar_todos():
        clsUsuarios._asegurar_directorio()
        if not os.path.exists(ARCHIVO_USUARIOS):
            return []
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [clsUsuarios.from_dict(u) for u in data]

    @staticmethod
    def guardar_todos(usuarios):
        clsUsuarios._asegurar_directorio()
        with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in usuarios], f, indent=4, ensure_ascii=False)

    @staticmethod
    def buscar_por_documento(documento):
        usuarios = clsUsuarios.cargar_todos()
        for u in usuarios:
            if u.documento == documento:
                return u
        return None

    @staticmethod
    def documento_existe(documento):
        return clsUsuarios.buscar_por_documento(documento) is not None

    def guardar(self):
        usuarios = clsUsuarios.cargar_todos()
        usuarios.append(self)
        clsUsuarios.guardar_todos(usuarios)

    # ── Presentacion ─────────────────────────────────────────────────────────

    def __str__(self):
        return (f"  Nombre    : {self.nombre} {self.apellido}\n"
                f"  Documento : {self.documento}\n"
                f"  Correo    : {self.correo}\n"
                f"  T.Prestamo: {self.tiempo_prestamo} dias")
