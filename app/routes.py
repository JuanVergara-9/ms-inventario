from flask import Blueprint, request, jsonify
from app.services import actualizar_stock, obtener_stock

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/actualizar-stock', methods=['POST'])
def actualizar():
    data = request.json
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    try:
        nuevo_stock = actualizar_stock(producto_id, cantidad)
        return jsonify({"producto_id": producto_id, "nuevo_stock": nuevo_stock}), 200
    except ValueError as e:
        print(f"Error de validación: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error desconocido al actualizar stock: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@inventario_bp.route('/consultar-stock/<int:producto_id>', methods=['GET'])
def consultar_stock(producto_id):
    try:
        stock = obtener_stock(producto_id)
        if stock is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify({"producto_id": producto_id, "stock": stock}), 200
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500