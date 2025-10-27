import redis
from redis.exceptions import RedisError
import sys

r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

def main():
    try:
        r.ping()  # devuelve True o lanza excepción si falla
        print("Conexión exitosa")
        
        # 1. HSET - Guardar campos del usuario
        r.hset('usuario:1', mapping={
            'nombre': 'José',
            'edad': 20,
            'ciudad': 'Bogotá'
        })
        
        # 2. HGETALL - Recuperar usuario completo
        usuario = r.hgetall('usuario:1')
        
        # 3. Imprimir resultado
        print("\nDatos del usuario:")
        print(usuario)
        
    except RedisError as e:
        print("Error de conexión a Redis:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()