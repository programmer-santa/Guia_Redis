import redis
from redis.exceptions import RedisError
import sys

class ProductoCRUD:
    def __init__(self):
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
        
    def crear(self, id, nombre, precio, stock):
        """Crear nuevo producto"""
        key = f"producto:{id}"
        return self.r.hset(key, mapping={
            'nombre': nombre,
            'precio': precio,
            'stock': stock
        })
    
    def leer(self, id):
        """Leer producto por ID"""
        key = f"producto:{id}"
        return self.r.hgetall(key)
    
    def actualizar(self, id, datos):
        """Actualizar producto existente"""
        key = f"producto:{id}"
        return self.r.hset(key, mapping=datos)
    
    def eliminar(self, id):
        """Eliminar producto"""
        key = f"producto:{id}"
        return self.r.delete(key)

def listar_todos(r):
    keys = list(r.scan_iter(match='producto:*'))
    if not keys:
        print("No hay productos.")
        return
    for k in keys:
        prod = r.hgetall(k)
        print(f"{k}: {prod}")

def pedir_entero(prompt, default=None):
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        try:
            return int(val)
        except ValueError:
            print("Ingrese un número entero válido.")

def pedir_flotante(prompt, default=None):
    while True:
        val = input(prompt).strip()
        if val == "" and default is not None:
            return default
        try:
            return float(val)
        except ValueError:
            print("Ingrese un número válido (ej: 12.5).")

def main():
    crud = ProductoCRUD()
    
    try:
        if not crud.r.ping():
            print("No se pudo conectar a Redis.")
            sys.exit(1)
    except RedisError as e:
        print("Error de Redis:", e)
        sys.exit(1)

    print("Conexión exitosa a Redis\n")

    while True:
        print("\nMenú CRUD - Productos")
        print("1) Crear producto")
        print("2) Leer producto por ID")
        print("3) Actualizar producto")
        print("4) Eliminar producto")
        print("5) Listar todos los productos")
        print("6) Salir")
        opc = input("Elige una opción (1-6): ").strip()

        if opc == "1":
            id = input("ID del producto: ").strip()
            nombre = input("Nombre: ").strip()
            precio = pedir_flotante("Precio: ")
            stock = pedir_entero("Stock: ")
            crud.crear(id, nombre, str(precio), str(stock))
            print("Producto creado.")

        elif opc == "2":
            id = input("ID del producto a leer: ").strip()
            prod = crud.leer(id)
            if prod:
                print(f"Producto {id}: {prod}")
            else:
                print("Producto no encontrado.")

        elif opc == "3":
            id = input("ID del producto a actualizar: ").strip()
            existente = crud.leer(id)
            if not existente:
                print("Producto no encontrado.")
                continue
            print("Dejar vacío para no modificar un campo.")
            nombre = input(f"Nombre [{existente.get('nombre','')}]: ").strip() or None
            precio_in = input(f"Precio [{existing := existente.get('precio','')}]: ").strip()
            stock_in = input(f"Stock [{existente.get('stock','')}]: ").strip()

            datos = {}
            if nombre:
                datos['nombre'] = nombre
            if precio_in:
                try:
                    float(precio_in)
                    datos['precio'] = precio_in
                except ValueError:
                    print("Precio no válido, se omite.")
            if stock_in:
                try:
                    int(stock_in)
                    datos['stock'] = stock_in
                except ValueError:
                    print("Stock no válido, se omite.")
            if datos:
                crud.actualizar(id, datos)
                print("Producto actualizado.")
            else:
                print("No se realizaron cambios.")

        elif opc == "4":
            id = input("ID del producto a eliminar: ").strip()
            borrados = crud.eliminar(id)
            if borrados:
                print("Producto eliminado.")
            else:
                print("Producto no encontrado.")

        elif opc == "5":
            listar_todos(crud.r)

        elif opc == "6":
            print("Saliendo.")
            break

        else:
            print("Opción no válida. Elige 1-6.")

if __name__ == '__main__':
    main()