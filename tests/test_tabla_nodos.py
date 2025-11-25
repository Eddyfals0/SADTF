"""Tests para TablaNodos"""
import pytest
from nodo_descentralizado.tabla_nodos import TablaNodos


def test_registrar_nodo():
    """Test registrar un nodo"""
    tabla = TablaNodos()
    tabla.registrar_nodo('nodo_1', {
        'host': '127.0.0.1',
        'puerto': 9001,
        'capacidad_mb': 50
    })
    
    nodo = tabla.obtener_nodo('nodo_1')
    assert nodo is not None
    assert nodo['id'] == 'nodo_1'
    assert nodo['host'] == '127.0.0.1'
    assert nodo['puerto'] == 9001


def test_obtener_nodos_activos():
    """Test obtener nodos activos"""
    tabla = TablaNodos(timeout_segundos=10)
    tabla.registrar_nodo('nodo_1', {
        'host': '127.0.0.1',
        'puerto': 9001,
        'capacidad_mb': 50
    })
    
    activos = tabla.obtener_nodos_activos()
    assert len(activos) == 1
    assert 'nodo_1' in activos


def test_actualizar_heartbeat():
    """Test actualizar heartbeat"""
    tabla = TablaNodos()
    tabla.registrar_nodo('nodo_1', {
        'host': '127.0.0.1',
        'puerto': 9001,
        'capacidad_mb': 50
    })
    
    # No debería lanzar excepción
    tabla.actualizar_heartbeat('nodo_1')
    
    # Nodo inexistente
    with pytest.raises(KeyError):
        tabla.actualizar_heartbeat('nodo_inexistente')


def test_obtener_nodo_con_espacio():
    """Test obtener nodo con espacio suficiente"""
    tabla = TablaNodos()
    tabla.registrar_nodo('nodo_1', {
        'host': '127.0.0.1',
        'puerto': 9001,
        'capacidad_mb': 50
    })
    tabla.registrar_nodo('nodo_2', {
        'host': '127.0.0.1',
        'puerto': 9002,
        'capacidad_mb': 100
    })
    
    # Actualizar espacio libre
    tabla.actualizar_espacio_libre('nodo_1', 20)
    tabla.actualizar_espacio_libre('nodo_2', 80)
    
    # Debe retornar nodo_1 (20 MB >= 10)
    nodo = tabla.obtener_nodo_con_espacio(10)
    assert nodo in ['nodo_1', 'nodo_2']
    
    # No hay suficiente espacio
    nodo = tabla.obtener_nodo_con_espacio(1000)
    assert nodo is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
