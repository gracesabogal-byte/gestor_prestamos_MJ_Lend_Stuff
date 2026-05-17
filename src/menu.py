"""
pf_Algoritmos
Modulo: menu
Logica de menus y flujo principal - MJ Lend-Stuff
"""

import os
import csv
from datetime import datetime
from clsUsuarios import clsUsuarios
from clsItem import clsItem, CATEGORIAS, NOMBRES_CATEGORIAS, ESTADOS_DIFUSOS
from clsPrestamo import clsPrestamo

# ── Administrador: usuario y clave hardcoded (se puede ampliar a archivo) ───
ADMINS = {
    "admin": "mj2026",
    "mj": "lendstuff"
}

CARPETA_DATA = os.path.join(os.path.dirname(__file__), "data")


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\n  Presione Enter para continuar...")


def separador():
    print("-" * 70)


def titulo(texto):
    cls()
    print("=" * 70)
    print(f"  {texto}")
    print("=" * 70)


# ═══════════════════════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def mostrar_menu_principal():
    while True:
        cls()
        print("=" * 70)
        print("         MJ LEND-STUFF - Gestor de Prestamos")
        print("=" * 70)
        print()
        print("  1. Registrar Usuario")
        print("  2. Registrar Prestamo")
        print("  3. Registrar Devolucion")
        print("  4. Consultar Items con mas de 30 dias (Generar Venta)")
        print("  5. Consultar Articulos Prestados")
        print("  6. Administrador")
        print("  7. Salir")
        print()
        separador()
        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "1":
            menu_registrar_usuario()
        elif opcion == "2":
            menu_registrar_prestamo()
        elif opcion == "3":
            menu_registrar_devolucion()
        elif opcion == "4":
            menu_items_vencidos()
        elif opcion == "5":
            menu_consultar_prestados()
        elif opcion == "6":
            menu_administrador()
        elif opcion == "7":
            cls()
            print("\n  Hasta luego! - MJ Lend-Stuff\n")
            break
        else:
            print("\n  Opcion invalida. Intente de nuevo.")
            pausar()


# ═══════════════════════════════════════════════════════════════════════════
#  REGISTRAR USUARIO
# ═══════════════════════════════════════════════════════════════════════════

def menu_registrar_usuario():
    titulo("REGISTRAR USUARIO")

    # Nombre
    while True:
        nombre = input("  Nombre: ").strip()
        ok, msg = clsUsuarios.validar_nombre(nombre)
        if ok:
            break
        print(f"  [Error] {msg}")

    # Apellido
    while True:
        apellido = input("  Apellido: ").strip()
        ok, msg = clsUsuarios.validar_apellido(apellido)
        if ok:
            break
        print(f"  [Error] {msg}")

    # Documento
    while True:
        documento = input("  Documento: ").strip()
        ok, msg = clsUsuarios.validar_documento(documento)
        if not ok:
            print(f"  [Error] {msg}")
            continue
        if clsUsuarios.documento_existe(documento):
            print("  [Error] Ya existe un usuario con ese documento.")
            continue
        break

    # Correo
    while True:
        correo = input("  Correo electronico: ").strip()
        ok, msg = clsUsuarios.validar_correo(correo)
        if ok:
            break
        print(f"  [Error] {msg}")

    # Tiempo de prestamo
    print("\n  Tiempo de prestamo permitido:")
    print("    1) 5 dias   2) 10 dias   3) 15 dias   4) 30 dias")
    opciones_tiempo = {"1": 5, "2": 10, "3": 15, "4": 30}
    while True:
        op = input("  Seleccione (1-4): ").strip()
        if op in opciones_tiempo:
            tiempo_prestamo = opciones_tiempo[op]
            break
        print("  [Error] Opcion invalida. Seleccione 1, 2, 3 o 4.")

    usuario = clsUsuarios(nombre, apellido, documento, correo, tiempo_prestamo)
    usuario.guardar()

    print("\n" + "=" * 70)
    print("  Usuario registrado exitosamente:")
    print(usuario)
    print("=" * 70)
    pausar()


# ═══════════════════════════════════════════════════════════════════════════
#  REGISTRAR ITEM  (submodulo accesible desde administrador)
# ═══════════════════════════════════════════════════════════════════════════

def menu_registrar_item():
    titulo("REGISTRAR ITEM")

    # Nombre
    while True:
        nombre = input("  Nombre del item: ").strip()
        ok, msg = clsItem.validar_nombre(nombre)
        if ok:
            break
        print(f"  [Error] {msg}")

    # Categoria
    print("\n  Categorias disponibles:")
    for k, v in NOMBRES_CATEGORIAS.items():
        print(f"    {k}) {v}")
    while True:
        cat = input("  Seleccione categoria (1-6): ").strip()
        ok, msg = clsItem.validar_categoria(cat)
        if ok:
            break
        print(f"  [Error] {msg}")

    # Precio
    while True:
        precio_str = input("  Precio de compra ($): ").strip()
        ok, resultado = clsItem.validar_precio(precio_str)
        if ok:
            precio = resultado
            break
        print(f"  [Error] {resultado}")

    # Estado (logica difusa)
    print("\n  Estado del item (logica difusa):")
    for k, (nombre_e, val) in ESTADOS_DIFUSOS.items():
        print(f"    {k}) {nombre_e} (valor: {val})")
    while True:
        estado = input("  Seleccione estado (1-5): ").strip()
        ok, msg = clsItem.validar_estado(estado)
        if ok:
            break
        print(f"  [Error] {msg}")

    item = clsItem(nombre, cat, precio, estado)
    item.guardar()

    print("\n" + "=" * 70)
    print("  Item registrado exitosamente:")
    print(item)
    print("=" * 70)
    pausar()


# ═══════════════════════════════════════════════════════════════════════════
#  REGISTRAR PRESTAMO
# ═══════════════════════════════════════════════════════════════════════════

def menu_registrar_prestamo():
    titulo("REGISTRAR PRESTAMO")

    # Mostrar items disponibles
    disponibles = clsItem.items_disponibles()
    if not disponibles:
        print("  No hay items disponibles para prestar.")
        pausar()
        return

    print("  Items disponibles:\n")
    for item in disponibles:
        print(f"  [{item.item_id}] {item.nombre} - {item.nombre_categoria()} - ${item.precio_compra:,.0f} - Estado: {item.nombre_estado()}")
    print()

    # Seleccionar item
    while True:
        item_id = input("  Ingrese el ID del item a prestar: ").strip().upper()
        item = clsItem.buscar_por_id(item_id)
        if item is None:
            print("  [Error] ID no encontrado.")
            continue
        if not item.disponible:
            print("  [Error] Ese item ya esta prestado.")
            continue
        break

    # Buscar usuario
    while True:
        documento = input("  Documento del usuario: ").strip()
        usuario = clsUsuarios.buscar_por_documento(documento)
        if usuario is None:
            print("  [Error] Usuario no encontrado. Debe registrarlo primero (opcion 1 del menu).")
            pausar()
            return
        break

    # Crear prestamo
    prestamo = clsPrestamo(documento, item.item_id)
    prestamo.guardar()
    item.actualizar_disponibilidad(False)

    print("\n" + "=" * 70)
    print("  Prestamo registrado exitosamente:")
    print(f"  Item      : {item.nombre} [{item.item_id}]")
    print(f"  Usuario   : {usuario.nombre} {usuario.apellido}")
    print(f"  Fecha     : {prestamo.fecha_prestamo}")
    print(f"  Vence en  : {usuario.tiempo_prestamo} dias ({prestamo.fecha_limite(usuario.tiempo_prestamo)})")
    print("=" * 70)
    pausar()


# ═══════════════════════════════════════════════════════════════════════════
#  REGISTRAR DEVOLUCION
# ═══════════════════════════════════════════════════════════════════════════

def menu_registrar_devolucion():
    titulo("REGISTRAR DEVOLUCION")

    documento = input("  Documento del usuario: ").strip()
    usuario = clsUsuarios.buscar_por_documento(documento)
    if usuario is None:
        print("  [Error] Usuario no encontrado en el sistema.")
        pausar()
        return

    prestamos_activos = clsPrestamo.prestamos_activos_de_usuario(documento)
    if not prestamos_activos:
        print(f"  [Info] El usuario {usuario.nombre} {usuario.apellido} no tiene prestamos activos.")
        pausar()
        return

    print(f"\n  Prestamos activos de {usuario.nombre} {usuario.apellido}:\n")
    for i, p in enumerate(prestamos_activos, 1):
        item = clsItem.buscar_por_id(p.item_id)
        nombre_item = item.nombre if item else "Desconocido"
        print(f"  {i}. [{p.item_id}] {nombre_item} - Prestado el {p.fecha_prestamo} ({p.dias_prestado()} dias)")

    while True:
        try:
            seleccion = int(input("\n  Seleccione el numero del prestamo a devolver: "))
            if 1 <= seleccion <= len(prestamos_activos):
                break
            print("  [Error] Numero fuera de rango.")
        except ValueError:
            print("  [Error] Ingrese un numero valido.")

    prestamo = prestamos_activos[seleccion - 1]
    item = clsItem.buscar_por_id(prestamo.item_id)

    prestamo.registrar_devolucion(f"{usuario.nombre}_{usuario.apellido}")
    if item:
        item.actualizar_disponibilidad(True)

    print("\n" + "=" * 70)
    print("  Devolucion registrada exitosamente.")
    print(f"  Item [{prestamo.item_id}] devuelto y disponible de nuevo.")
    print("=" * 70)
    pausar()


# ═══════════════════════════════════════════════════════════════════════════
#  ITEMS VENCIDOS (>30 dias) → GENERAR VENTA
# ═══════════════════════════════════════════════════════════════════════════

def menu_items_vencidos():
    titulo("ITEMS CON MAS DE 30 DIAS - GENERAR VENTA")

    vencidos = clsPrestamo.prestamos_vencidos_venta()
    if not vencidos:
        print("  No hay items con mas de 30 dias de prestamo.")
        pausar()
        return

    print("  Los siguientes items llevan mas de 30 dias prestados:\n")
    for i, p in enumerate(vencidos, 1):
        item = clsItem.buscar_por_id(p.item_id)
        usuario = clsUsuarios.buscar_por_documento(p.documento_usuario)
        nombre_item = item.nombre if item else "Desconocido"
        nombre_usuario = f"{usuario.nombre} {usuario.apellido}" if usuario else p.documento_usuario
        print(f"  {i}. [{p.item_id}] {nombre_item} - Usuario: {nombre_usuario} - Dias: {p.dias_prestado()}")

    while True:
        try:
            seleccion = int(input("\n  Seleccione el numero para generar factura (0 para cancelar): "))
            if seleccion == 0:
                return
            if 1 <= seleccion <= len(vencidos):
                break
            print("  [Error] Numero fuera de rango.")
        except ValueError:
            print("  [Error] Ingrese un numero valido.")

    prestamo = vencidos[seleccion - 1]
    item = clsItem.buscar_por_id(prestamo.item_id)
    usuario = clsUsuarios.buscar_por_documento(prestamo.documento_usuario)

    nombre_usuario = f"{usuario.nombre}_{usuario.apellido}" if usuario else prestamo.documento_usuario
    nombre_item = item.nombre if item else "Desconocido"
    precio = item.precio_compra if item else 0

    total = prestamo.generar_factura_venta(nombre_usuario, nombre_item, precio)
    if item:
        item.actualizar_disponibilidad(True)

    subtotal = precio
    impuesto = precio * 0.23
    print("\n" + "=" * 70)
    print("  FACTURA GENERADA")
    print(f"  Item          : {nombre_item} [{prestamo.item_id}]")
    print(f"  Usuario       : {nombre_usuario}")
    print(f"  Subtotal      : ${subtotal:,.0f}")
    print(f"  Impuesto 23%  : ${impuesto:,.0f}")
    print(f"  TOTAL         : ${total:,.0f}")
    print("=" * 70)
    pausar()


# ═══════════════════════════════════════════════════════════════════════════
#  CONSULTAR ARTICULOS PRESTADOS
# ═══════════════════════════════════════════════════════════════════════════

def menu_consultar_prestados():
    titulo("CONSULTAR ARTICULOS PRESTADOS")

    activos = clsPrestamo.todos_activos()
    if not activos:
        print("  No hay articulos prestados actualmente.")
        pausar()
        return

    # Ordenar por dias (mayor a menor)
    activos.sort(key=lambda p: p.dias_prestado(), reverse=True)

    print(f"  {'ID Item':<12} {'Nombre Item':<20} {'Usuario':<25} {'Dias':>5}  {'Alerta'}")
    separador()
    for p in activos:
        item = clsItem.buscar_por_id(p.item_id)
        usuario = clsUsuarios.buscar_por_documento(p.documento_usuario)
        nombre_item = item.nombre[:18] if item else "Desconocido"
        nombre_u = f"{usuario.nombre} {usuario.apellido}"[:23] if usuario else p.documento_usuario
        alerta = ""
        if p.esta_vencido_venta():
            alerta = "⚠ VENTA"
        elif p.esta_vencido_notificacion():
            alerta = "! Devolucion"
        print(f"  {p.item_id:<12} {nombre_item:<20} {nombre_u:<25} {p.dias_prestado():>5}  {alerta}")

    # Exportar a CSV
    print()
    exportar = input("  Desea exportar a CSV? (s/n): ").strip().lower()
    if exportar == "s":
        _exportar_csv_prestados(activos)

    pausar()


def _exportar_csv_prestados(prestamos):
    os.makedirs(CARPETA_DATA, exist_ok=True)
    ruta = os.path.join(CARPETA_DATA, "reporte_prestamos.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID Item", "Nombre Item", "Categoria", "Precio",
                         "Documento Usuario", "Nombre Usuario", "Fecha Prestamo", "Dias"])
        for p in prestamos:
            item = clsItem.buscar_por_id(p.item_id)
            usuario = clsUsuarios.buscar_por_documento(p.documento_usuario)
            nombre_item = item.nombre if item else ""
            cat = item.nombre_categoria() if item else ""
            precio = item.precio_compra if item else 0
            nombre_u = f"{usuario.nombre} {usuario.apellido}" if usuario else ""
            writer.writerow([p.item_id, nombre_item, cat, precio,
                             p.documento_usuario, nombre_u, p.fecha_prestamo, p.dias_prestado()])
    print(f"  [OK] Exportado a: data/reporte_prestamos.csv")


# ═══════════════════════════════════════════════════════════════════════════
#  ADMINISTRADOR
# ═══════════════════════════════════════════════════════════════════════════

def menu_administrador():
    titulo("MODULO ADMINISTRADOR")

    usuario_admin = input("  Usuario: ").strip()
    clave_admin = input("  Clave  : ").strip()

    if usuario_admin not in ADMINS or ADMINS[usuario_admin] != clave_admin:
        print("\n  [Error] Credenciales incorrectas. Acceso denegado.")
        pausar()
        return

    while True:
        cls()
        print("=" * 70)
        print("  ADMINISTRADOR - MJ Lend-Stuff")
        print("=" * 70)
        print()
        print("  1. Total de prestamos registrados")
        print("  2. Total de items devueltos")
        print("  3. Total de ventas realizadas")
        print("  4. Total pagado en ventas")
        print("  5. Lista de usuarios")
        print("  6. Usuario con mayor y menor prestamos")
        print("  7. Registrar nuevo Item al inventario")
        print("  8. Volver al menu principal")
        print()
        separador()
        op = input("  Seleccione: ").strip()

        if op == "1":
            _admin_total_prestamos()
        elif op == "2":
            _admin_total_devueltos()
        elif op == "3":
            _admin_total_ventas()
        elif op == "4":
            _admin_total_pagado()
        elif op == "5":
            _admin_lista_usuarios()
        elif op == "6":
            _admin_mayor_menor_prestamos()
        elif op == "7":
            menu_registrar_item()
        elif op == "8":
            break
        else:
            print("  Opcion invalida.")
            pausar()


def _admin_total_prestamos():
    titulo("TOTAL DE PRESTAMOS REGISTRADOS")
    todos = clsPrestamo.cargar_todos()
    print(f"  Total de prestamos en el sistema: {len(todos)}")
    pausar()


def _admin_total_devueltos():
    titulo("TOTAL DE ITEMS DEVUELTOS")
    devueltos = [p for p in clsPrestamo.cargar_todos() if not p.activo and not p.vendido]
    print(f"  Total de items devueltos: {len(devueltos)}")
    pausar()


def _admin_total_ventas():
    titulo("TOTAL DE VENTAS REALIZADAS")
    ventas = [p for p in clsPrestamo.cargar_todos() if p.vendido]
    print(f"  Total de ventas: {len(ventas)}")
    pausar()


def _admin_total_pagado():
    titulo("TOTAL PAGADO EN VENTAS")
    ventas = [p for p in clsPrestamo.cargar_todos() if p.vendido]
    total = 0
    for p in ventas:
        item = clsItem.buscar_por_id(p.item_id)
        if item:
            subtotal = item.precio_compra
            total += subtotal * 1.23
    print(f"  Total recaudado en ventas: ${total:,.0f}")
    pausar()


def _admin_lista_usuarios():
    titulo("LISTA DE USUARIOS")
    usuarios = clsUsuarios.cargar_todos()
    if not usuarios:
        print("  No hay usuarios registrados.")
    else:
        for u in usuarios:
            print(u)
            separador()
    pausar()


def _admin_mayor_menor_prestamos():
    titulo("USUARIO CON MAYOR Y MENOR PRESTAMOS")
    todos = clsPrestamo.cargar_todos()
    conteo = {}
    for p in todos:
        conteo[p.documento_usuario] = conteo.get(p.documento_usuario, 0) + 1

    if not conteo:
        print("  No hay prestamos registrados.")
        pausar()
        return

    mayor_doc = max(conteo, key=conteo.get)
    menor_doc = min(conteo, key=conteo.get)
    mayor_u = clsUsuarios.buscar_por_documento(mayor_doc)
    menor_u = clsUsuarios.buscar_por_documento(menor_doc)

    nombre_mayor = f"{mayor_u.nombre} {mayor_u.apellido}" if mayor_u else mayor_doc
    nombre_menor = f"{menor_u.nombre} {menor_u.apellido}" if menor_u else menor_doc

    print(f"  Mayor cantidad de prestamos: {nombre_mayor} ({conteo[mayor_doc]} prestamos)")
    print(f"  Menor cantidad de prestamos: {nombre_menor} ({conteo[menor_doc]} prestamos)")
    pausar()
