import unittest
from app import create_app, db
from app.models import Inventario

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Agregar un producto de prueba
        producto = Inventario(id=1, product_name='Producto A', stock=10)
        db.session.add(producto)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_actualizar_stock(self):
        response = self.client.post('/inventario/actualizar-stock', json={
            'producto_id': 1,
            'cantidad': -1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['nuevo_stock'], 9)

    def test_obtener_stock(self):
        response = self.client.get('/inventario/consultar-stock/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['stock'], 10)

if __name__ == '__main__':
    unittest.main()