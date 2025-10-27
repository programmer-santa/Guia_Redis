import redis
from redis.exceptions import RedisError
import sys

r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

def main():
    try:
        if r.ping():
            print("Conexión exitosa")
            
            # 1. SADD - Agregar amigos al conjunto (incluyendo duplicado)
            r.sadd('amigos', 'Ana', 'Luis', 'Ana')
            
            # 2. SMEMBERS - Obtener todos los miembros
            amigos = r.smembers('amigos')
            print("\nLista de amigos (sin duplicados):")
            print(amigos)
            
            # 3. SISMEMBER - Verificar si existe 'Luis'
            existe_luis = r.sismember('amigos', 'Luis')
            print(f"\n¿'Luis' está en el conjunto?: {existe_luis}")
            
            # --- Ejercicio 4: Ranking de Puntuaciones (Conjuntos Ordenados) ---
            # 1. ZADD - Agregar miembros con sus puntuaciones
            # Agregamos: Ana (100), Luis (200), Carlos (150)
            r.zadd('ranking', {'Ana': 100, 'Luis': 200, 'Carlos': 150})

            # 2. ZREVRANGE - Obtener ranking del mayor al menor, incluyendo puntuaciones
            # start=0, end=-1, withscores=True
            ranking = r.zrevrange('ranking', 0, -1, withscores=True)

            # 3. Imprimir el resultado
            print("\nRanking (de mayor a menor, con puntuaciones):")
            for member, score in ranking:
                print(f"{member}: {int(score) if isinstance(score, float) else score}")
            
    except RedisError as e:
        print("Error de conexión a Redis:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()