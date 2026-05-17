"""
pf_Algoritmos
Modulo: clsPrestamo
Gestion de prestamos - MJ Lend-Stuff
"""

import json
import os
from datetime import datetime, timedelta

ARCHIVO_PRESTAMOS = os.path.join(os.path.dirname(__file__), "data", "prestamos.json")
CARPETA_DOCS = os.path.join(os.path.dirname(__file__), "documentos")

FORMATO_FECHA = "%Y-%m-%d"


class clsPrestamo:
    """
    Clase para gestionar los prestamos del sistema MJ Lend-Stuff.
    pf_Algoritmos
    """

    def __init__(self, documento_usuario, item_id, fecha_prestamo=None,
                 fecha_devolucion=None, activo=True, vendido=False):
        self.documento_usuario = documento_usuario
        self.item_id = item_id
        self.fecha_prestamo = fecha_prestamo or datetime.now().strftime(FORMATO_FECHA)
        self.fecha_devolucion = fecha_devolucion  # None si no se ha devuelto
        self.activo = activo
        self.vendido = vendido

    def dias_prestado(self):
        inicio = datetime.strptime(self.fecha_prestamo, FORMATO_FECHA)
        fin = datetime.now()
        return (fin - inicio).days

    def esta_vencido_notificacion(self):
        """True si lleva mas de 20 dias prestado."""
        return self.dias_prestado() >= 20

    def esta_vencido_venta(self):
        """True si lleva mas de 30 dias prestado."""
        return self.dias_prestado() >= 30

    def fecha_limite(self, tiempo_prestamo_dias):
        inicio = datetime.strptime(self.fecha_prestamo, FORMATO_FECHA)
        return (inicio + timedelta(days=tiempo_prestamo_dias)).strftime(FORMATO_FECHA)

    def to_dict(self):
        return {
            "documento_usuario": self.documento_usuario,
            "item_id": self.item_id,
            "fecha_prestamo": self.fecha_prestamo,
            "fecha_devolucion": self.fecha_devolucion,
            "activo": self.activo,
            "vendido": self.vendido
        }

    @staticmethod
    def from_dict(data):
        return clsPrestamo(
            data["documento_usuario"],
            data["item_id"],
            data.get("fecha_prestamo"),
            data.get("fecha_devolucion"),
            data.get("activo", True),
            data.get("vendido", False)
        )

    # ── Persistencia ─────────────────────────────────────────────────────────

    @staticmethod
    def _asegurar_directorio():
        os.makedirs(os.path.dirname(ARCHIVO_PRESTAMOS), exist_ok=True)
        os.makedirs(CARPETA_DOCS, exist_ok=True)

    @staticmethod
    def cargar_todos():
        clsPrestamo._asegurar_directorio()
        if not os.path.exists(ARCHIVO_PRESTAMOS):
            return []
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [clsPrestamo.from_dict(p) for p in data]

    @staticmethod
    def guardar_todos(prestamos):
        clsPrestamo._asegurar_directorio()
        with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in prestamos], f, indent=4, ensure_ascii=False)

    def guardar(self):
        prestamos = clsPrestamo.cargar_todos()
        prestamos.append(self)
        clsPrestamo.guardar_todos(prestamos)

    @staticmethod
    def prestamos_activos_de_usuario(documento):
        return [p for p in clsPrestamo.cargar_todos()
                if p.documento_usuario == documento and p.activo]

    @staticmethod
    def prestamos_vencidos_venta():
        return [p for p in clsPrestamo.cargar_todos()
                if p.activo and not p.vendido and p.esta_vencido_venta()]

    @staticmethod
    def todos_activos():
        return [p for p in clsPrestamo.cargar_todos() if p.activo]

    # ── Documentos ───────────────────────────────────────────────────────────

    def registrar_devolucion(self, nombre_usuario):
        """Marca el prestamo como devuelto y genera certificado."""
        prestamos = clsPrestamo.cargar_todos()
        for p in prestamos:
            if p.documento_usuario == self.documento_usuario and p.item_id == self.item_id and p.activo:
                p.activo = False
                p.fecha_devolucion = datetime.now().strftime(FORMATO_FECHA)
                self.fecha_devolucion = p.fecha_devolucion
                self.activo = False
        clsPrestamo.guardar_todos(prestamos)
        self._generar_certificado_devolucion(nombre_usuario)

    def _generar_certificado_devolucion(self, nombre_usuario):
        clsPrestamo._asegurar_directorio()
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"{nombre_usuario}_{fecha_hoy}_{self.item_id}.txt"
        ruta = os.path.join(CARPETA_DOCS, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("       CERTIFICADO DE DEVOLUCION - MJ Lend-Stuff\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Fecha de emision       : {fecha_hoy}\n")
            f.write(f"Usuario                : {nombre_usuario}\n")
            f.write(f"Documento              : {self.documento_usuario}\n")
            f.write(f"Item ID                : {self.item_id}\n")
            f.write(f"Fecha de prestamo      : {self.fecha_prestamo}\n")
            f.write(f"Fecha de devolucion    : {self.fecha_devolucion}\n")
            f.write(f"Dias prestado          : {self.dias_prestado()}\n\n")
            f.write("Por medio del presente certificado se hace constar que\n")
            f.write("el articulo fue devuelto satisfactoriamente.\n\n")
            f.write("=" * 60 + "\n")
            f.write("              MJ Lend-Stuff - Sistema de Prestamos\n")
            f.write("=" * 60 + "\n")
        print(f"\n  [OK] Certificado generado: documentos/{nombre_archivo}")

    def generar_factura_venta(self, nombre_usuario, nombre_item, precio_compra):
        clsPrestamo._asegurar_directorio()
        subtotal = precio_compra
        impuesto = subtotal * 0.23
        total = subtotal + impuesto
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"VENTA_{nombre_usuario}_{self.item_id}.txt"
        ruta = os.path.join(CARPETA_DOCS, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("           FACTURA DE VENTA - MJ Lend-Stuff\n")
            f.write("=" * 60 + "\n\n")
            f.write("MOTIVACION DE LA VENTA:\n")
            f.write("El articulo fue prestado por mas de 30 dias sin ser\n")
            f.write("devuelto. Segun el acuerdo entre las partes, el usuario\n")
            f.write("debe comprar el articulo al precio de adquisicion.\n\n")
            f.write("-" * 60 + "\n")
            f.write(f"Fecha de emision       : {fecha_hoy}\n")
            f.write(f"Usuario                : {nombre_usuario}\n")
            f.write(f"Documento              : {self.documento_usuario}\n")
            f.write(f"Item ID                : {self.item_id}\n")
            f.write(f"Descripcion            : {nombre_item}\n")
            f.write(f"Fecha de prestamo      : {self.fecha_prestamo}\n")
            f.write(f"Dias transcurridos     : {self.dias_prestado()}\n")
            f.write("-" * 60 + "\n")
            f.write(f"Subtotal               : ${subtotal:>12,.0f}\n")
            f.write(f"Impuesto conchudez 23%: ${impuesto:>12,.0f}\n")
            f.write(f"TOTAL A PAGAR          : ${total:>12,.0f}\n")
            f.write("=" * 60 + "\n")
            f.write("        MJ Lend-Stuff - Sistema de Prestamos\n")
            f.write("=" * 60 + "\n")

        # Marcar como vendido
        prestamos = clsPrestamo.cargar_todos()
        for p in prestamos:
            if p.documento_usuario == self.documento_usuario and p.item_id == self.item_id and p.activo:
                p.vendido = True
                p.activo = False
        clsPrestamo.guardar_todos(prestamos)
        print(f"\n  [OK] Factura generada: documentos/{nombre_archivo}")
        return total

    # ── Presentacion ─────────────────────────────────────────────────────────

    def __str__(self):
        estado = "Activo" if self.activo else ("Vendido" if self.vendido else "Devuelto")
        return (f"  Usuario   : {self.documento_usuario}\n"
                f"  Item ID   : {self.item_id}\n"
                f"  Prestado  : {self.fecha_prestamo}\n"
                f"  Dias      : {self.dias_prestado()}\n"
                f"  Estado    : {estado}")
