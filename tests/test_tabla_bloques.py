"""Tests para TablaBloques"""
import pytest
from nodo_descentralizado.tabla_bloques import TablaBloques


def test_asignar_bloques():
    """Test asignar bloques"""
    tabla = TablaBloques(total_bloques=100)
    
    bloques = tabla.asignar_bloques('archivo_1', 5)
    assert len(bloques) == 5
    assert tabla.obtener_bloques_libres() == 95


def test_registrar_replica():
    """Test registrar replica de bloque"""
    tabla = TablaBloques(total_bloques=100)
    bloques = tabla.asignar_bloques('archivo_1', 2)
    
    tabla.registrar_replica(bloques[0], 'nodo_1')
    tabla.registrar_replica(bloques[0], 'nodo_2')
    
    replicas = tabla.obtener_replicas(bloques[0])
    assert len(replicas) == 2
    assert 'nodo_1' in replicas
    assert 'nodo_2' in replicas


def test_liberar_bloques():
    """Test liberar bloques de archivo"""
    tabla = TablaBloques(total_bloques=100)
    
    bloques = tabla.asignar_bloques('archivo_1', 3)
    tabla.registrar_archivo('archivo_1', 'test.txt', 'usuario', bloques, 3000)
    
    bloques_usados_antes = 100 - tabla.obtener_bloques_libres()
    
    tabla.liberar_bloques('archivo_1')
    
    bloques_usados_despues = 100 - tabla.obtener_bloques_libres()
    
    assert bloques_usados_despues == 0
    assert tabla.obtener_archivo('archivo_1') is None


def test_registrar_archivo():
    """Test registrar archivo"""
    tabla = TablaBloques(total_bloques=100)
    bloques = tabla.asignar_bloques('archivo_1', 2)
    
    tabla.registrar_archivo('archivo_1', 'documento.pdf', 'juan', bloques, 2000000)
    
    archivo = tabla.obtener_archivo('archivo_1')
    assert archivo is not None
    assert archivo['nombre'] == 'documento.pdf'
    assert archivo['propietario'] == 'juan'
    assert archivo['size'] == 2000000


def test_espacio_insuficiente():
    """Test error cuando no hay bloques disponibles"""
    tabla = TablaBloques(total_bloques=5)
    
    bloques = tabla.asignar_bloques('archivo_1', 5)
    assert len(bloques) == 5
    
    with pytest.raises(ValueError):
        tabla.asignar_bloques('archivo_2', 1)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
