import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 5, // Número de usuarios virtuales
    duration: '10s', // Duración de la prueba
};

export default function () {
    let producto_id = 1; // ID del producto a actualizar
    let cantidad = -1; // Cantidad a actualizar (puede ser negativa para disminuir el stock)

    let res = http.post(`http://127.0.0.1:5000/inventario/actualizar-stock`, JSON.stringify({
        producto_id: producto_id,
        cantidad: cantidad
    }), {
        headers: { 'Content-Type': 'application/json' },
    });

    check(res, {
        'is status 200': (r) => r.status === 200,
        'no stock negativo': (r) => {
            if (r.json().error) {
                console.error(`Error en la respuesta: ${r.json().error}`);
                return false;
            }
            return true;
        },
    });

    sleep(1);
}