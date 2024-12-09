from app.extension import db, cache
from app.models import Inventario
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def actualizar_stock(producto_id, cantidad):
    try:
        # Iniciar una transacción
        with db.session.begin():
            # Obtener el inventario con bloqueo para actualización
            inventario = Inventario.query.filter_by(id=producto_id).with_for_update().first()
            if not inventario:
                raise ValueError('Producto no encontrado')
            
            nuevo_stock = inventario.stock + cantidad
            if nuevo_stock < 0:
                raise ValueError('El stock no puede ser negativo')
            
            inventario.stock = nuevo_stock
            db.session.commit()
            
            # Actualizar el cache
            cache.set(f'producto_{producto_id}_stock', nuevo_stock)
            
            return nuevo_stock
    except Exception as e:
        db.session.rollback()
        raise e

def obtener_stock(producto_id):
    # Intentar obtener el stock del cache
    stock = cache.get(f'producto_{producto_id}_stock')
    if stock is None:
        # Si no está en el cache, obtener de la base de datos
        inventario = Inventario.query.filter_by(id=producto_id).first()
        if inventario:
            stock = inventario.stock
            # Guardar en el cache
            cache.set(f'producto_{producto_id}_stock', stock)
    return stock