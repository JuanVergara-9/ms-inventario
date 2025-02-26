import unittest
from unittest.mock import patch, MagicMock
from app.services import actualizar_stock, obtener_stock
from app.models import Inventario

class TestServices(unittest.TestCase):

    @patch('app.services.db.session')
    @patch('app.services.cache')
    @patch('app.services.redis_client')
    def test_actualizar_stock(self, mock_redis, mock_cache, mock_db):
        # Configurar el mock de Redis
        mock_redis.set.return_value = True
        mock_redis.delete.return_value = True

        # Configurar el mock de la base de datos
        mock_inventario = MagicMock(spec=Inventario)
        mock_inventario.stock = 10
        mock_db.execute.return_value.fetchone.return_value = (9,)

        # Llamar a la función
        nuevo_stock = actualizar_stock(1, -1)

        # Verificar que el stock se actualizó correctamente
        self.assertEqual(nuevo_stock, 9)
        mock_db.commit.assert_called_once()
        mock_cache.set.assert_called_once_with('producto_1_stock', 9)

    @patch('app.services.cache')
    @patch('app.services.Inventario')
    def test_obtener_stock(self, mock_inventario, mock_cache):
        # Configurar el mock de la caché
        mock_cache.get.return_value = None

        # Configurar el mock de la base de datos
        mock_inventario.query.filter_by.return_value.first.return_value = Inventario(id=1, stock=10)

        # Llamar a la función
        stock = obtener_stock(1)

        # Verificar que el stock se obtuvo correctamente
        self.assertEqual(stock, 10)
        mock_cache.set.assert_called_once_with('producto_1_stock', 10)

if __name__ == '__main__':
    unittest.main()