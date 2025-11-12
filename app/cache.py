import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Cliente Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

# TTL (Tiempo de vida en segundos)
CACHE_TTL = 60 * 5  # 5 minutos

def get_cache(key: str):
    """Obtiene un valor desde Redis (si existe)."""
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        print(f"[Cache] Error al obtener {key}: {e}")
        return None

def set_cache(key: str, value, ttl: int = CACHE_TTL):
    """Guarda un valor en Redis con TTL."""
    try:
        redis_client.set(key, json.dumps(value), ex=ttl)
    except Exception as e:
        print(f"[Cache] Error al guardar {key}: {e}")

def delete_cache(key: str):
    """Elimina una clave específica."""
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"[Cache] Error al eliminar {key}: {e}")
