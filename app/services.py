import redis
import logging
from sqlalchemy import text
from app.extension import db, cache
from app.models import Inventario
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)

# Conectar a Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def actualizar_stock(producto_id, cantidad):
    if not isinstance(cantidad, (int, float)):
        raise ValueError("La cantidad debe ser un número válido")

    lock_key = f"lock_producto_{producto_id}"
    lock_acquired = False

    try:
        # Intentar obtener el bloqueo con expiración de 5 segundos
        lock_acquired = redis_client.set(lock_key, "1", nx=True, ex=5)
        if not lock_acquired:
            raise Exception(f"Otro proceso está actualizando el producto {producto_id}. Reintentando...")

        with db.session.begin():  # Transacción segura
            # Verificar y actualizar el stock
            query = text("""
                UPDATE inventario
                SET stock = stock + :cantidad
                WHERE id = :producto_id AND stock + :cantidad >= 0
            """)
            result = db.session.execute(query, {"producto_id": producto_id, "cantidad": cantidad})

            if result.rowcount == 0:
                raise ValueError(f"No hay suficiente stock para el producto {producto_id}")

            # Obtener el nuevo stock
            query = text("SELECT stock FROM inventario WHERE id = :producto_id")
            nuevo_stock = db.session.execute(query, {"producto_id": producto_id}).scalar()

            db.session.commit()  # Confirmar la transacción

            # Actualizar la caché
            cache.set(f'producto_{producto_id}_stock', nuevo_stock)

            return nuevo_stock

    except Exception as e:
        logging.error(f"Error al actualizar stock del producto {producto_id}: {e}")
        db.session.rollback()
        raise

    finally:
        if lock_acquired:
            redis_client.delete(lock_key)  # Liberar el bloqueo

def obtener_stock(producto_id):
    stock = cache.get(f'producto_{producto_id}_stock')
    
    if stock is None:
        inventario = Inventario.query.filter_by(id=producto_id).first()
        if inventario:
            stock = inventario.stock
            cache.set(f'producto_{producto_id}_stock', stock)
        else:
            stock = 0  # O definir un valor por defecto
    
    return stock