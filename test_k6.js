import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 10, // Aumentamos a 10 usuarios virtuales para más concurrencia
    duration: '15s', // Extendemos la duración de la prueba
};

export default function () {
    let producto_id = Math.ceil(Math.random() * 4); // Simular diferentes productos (IDs del 1 al 4)
    let cantidad = -1; // Disminuir stock con cada solicitud

    // Enviar solicitud POST para actualizar el stock
    let res = http.post(`http://127.0.0.1:5000/inventario/actualizar-stock`, JSON.stringify({
        producto_id: producto_id,
        cantidad: cantidad
    }), {
        headers: { 'Content-Type': 'application/json' },
    });

    // Validar la respuesta del POST
    check(res, {
        'is status 200': (r) => r.status === 200,
        'no stock negativo': (r) => {
            if (r.json().error) {
                console.error(`Error en la respuesta: ${r.json().error}`);
                return false;
            }
            let nuevo_stock = r.json().nuevo_stock; // Asegúrate de que tu API devuelva el stock actualizado
            console.log(`Producto ${producto_id} - Stock actual: ${nuevo_stock}`);
            return nuevo_stock >= 0; // Validar que el stock nunca sea negativo
        },
    });

    sleep(1);
}