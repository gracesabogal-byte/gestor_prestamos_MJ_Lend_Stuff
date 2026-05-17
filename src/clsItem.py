"""
pf_Algoritmos
Modulo: clsItem
Gestion de items del inventario - MJ Lend-Stuff
"""

import json
import os
import random
import string

ARCHIVO_ITEMS = os.path.join(os.path.dirname(__file__), "data", "items.json")

CATEGORIAS = {
    "1": "VJ",   # Videojuegos
    "2": "LB",   # Libros
    "3": "MV",   # Musica y video
    "4": "HE",   # Herramientas
    "5": "DN",   # Dinero
    "6": "MS"    # Miscelaneo y varios
}

NOMBRES_CATEGORIAS = {
    "1": "Videojuegos",
    "2": "Libros",
    "3": "Musica y video",
    "4": "Herramientas",
    "5": "Dinero",
    "6": "Miscelaneo y varios"
}

# Logica difusa para estado del item
ESTADOS_DIFUSOS = {
    "1": ("Excelente",  1.0),
    "2": ("Bueno",      0.75),
    "3": ("Regular",    0.5),
    "4": ("Deteriorado",0.25),
    "5": ("Malo",       0.1)
}


class clsItem:
    """
    Clase para gestionar los items del inventario de MJ.
    pf_Algoritmos
    """

    def __init__(self, nombre, categoria_codigo, precio_compra, estado_codigo, item_id=None, disponible=True):
        self.nombre = nombre
        self.categoria_codigo = categoria_codigo
        self.precio_compra = precio_compra
        self.estado_codigo = estado_codigo
        self.disponible = disponible
        self.item_id = item_id if item_id else self._generar_id(categoria_codigo)

    def _generar_id(self, categoria_codigo):
        prefijo = CATEGORIAS.get(categoria_codigo, "MS")
        aleatorio = ''.join(random.choices(string.digits + string.ascii_uppercase, k=5))
        return f"{prefijo}-{aleatorio}"

    def nombre_categoria(self):
        return NOMBRES_CATEGORIAS.get(self.categoria_codigo, "Desconocido")

    def nombre_estado(self):
        return ESTADOS_DIFUSOS.get(self.estado_codigo, ("Desconocido", 0))[0]

    def valor_difuso_estado(self):
        return ESTADOS_DIFUSOS.get(self.estado_codigo, ("Desconocido", 0))[1]

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "categoria_codigo": self.categoria_codigo,
            "precio_compra": self.precio_compra,
            "estado_codigo": self.estado_codigo,
            "item_id": self.item_id,
            "disponible": self.disponible
        }

    @staticmethod
    def from_dict(data):
        return clsItem(
            data["nombre"],
            data["categoria_codigo"],
            data["precio_compra"],
            data["estado_codigo"],
            data.get("item_id"),
            data.get("disponible", True)
        )

    # ── Validaciones ──────────────────────────────────────────────────────────

    @staticmethod
    def validar_nombre(nombre):
        if len(nombre) < 3:
            return False, "El nombre del item debe tener al menos 3 caracteres."
        return True, ""

    @staticmethod
    def validar_precio(precio_str):
        try:
            precio = float(precio_str)
            if precio <= 0:
                return False, "El precio debe ser mayor a 0."
            return True, precio
        except ValueError:
            return False, "El precio debe ser un numero valido."

    @staticmethod
    def validar_categoria(opcion):
        if opcion not in CATEGORIAS:
            return False, "Opcion de categoria invalida."
        return True, ""

    @staticmethod
    def validar_estado(opcion):
        if opcion not in ESTADOS_DIFUSOS:
            return False, "Opcion de estado invalida."
        return True, ""

    # ── Persistencia ─────────────────────────────────────────────────────────

    @staticmethod
    def _asegurar_directorio():
        os.makedirs(os.path.dirname(ARCHIVO_ITEMS), exist_ok=True)

    @staticmethod
    def cargar_todos():
        clsItem._asegurar_directorio()
        if not os.path.exists(ARCHIVO_ITEMS):
            return []
        with open(ARCHIVO_ITEMS, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [clsItem.from_dict(i) for i in data]

    @staticmethod
    def guardar_todos(items):
        clsItem._asegurar_directorio()
        with open(ARCHIVO_ITEMS, "w", encoding="utf-8") as f:
            json.dump([i.to_dict() for i in items], f, indent=4, ensure_ascii=False)

    @staticmethod
    def buscar_por_id(item_id):
        for item in clsItem.cargar_todos():
            if item.item_id == item_id:
                return item
        return None

    @staticmethod
    def items_disponibles():
        return [i for i in clsItem.cargar_todos() if i.disponible]

    def guardar(self):
        items = clsItem.cargar_todos()
        items.append(self)
        clsItem.guardar_todos(items)

    def actualizar_disponibilidad(self, disponible):
        items = clsItem.cargar_todos()
        for i in items:
            if i.item_id == self.item_id:
                i.disponible = disponible
        clsItem.guardar_todos(items)
        self.disponible = disponible

    # ── Presentacion ─────────────────────────────────────────────────────────

    def __str__(self):
        estado_str = self.nombre_estado()
        difuso = self.valor_difuso_estado()
        disp = "Disponible" if self.disponible else "Prestado"
        return (f"  ID        : {self.item_id}\n"
                f"  Nombre    : {self.nombre}\n"
                f"  Categoria : {self.nombre_categoria()}\n"
                f"  Precio    : ${self.precio_compra:,.0f}\n"
                f"  Estado    : {estado_str} (valor difuso: {difuso})\n"
                f"  Estado    : {disp}")
