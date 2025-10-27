import redis
from redis.exceptions import RedisError
import sys

r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

def main():
    try:
        if r.ping():
            print("Conexión exitosa")
            
            # 1. LPUSH - Agregar tareas a la lista
            r.lpush('tareas', 'dormir', 'comer', 'estudiar')
            
            # 2. LRANGE - Obtener lista completa
            tareas = r.lrange('tareas', 0, -1)
            
            # 3. Imprimir resultado
            print("\nLista de tareas:")
            print(tareas)
            
    except RedisError as e:
        print("Error de conexión a Redis:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()