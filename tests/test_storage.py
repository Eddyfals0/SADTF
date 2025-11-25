"""Tests para StorageManager"""
import os
import tempfile
import pytest
from nodo_descentralizado.storage_manager import StorageManager


def test_guardar_leer_bloque():
    """Test guardar y leer un bloque"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = StorageManager(tmpdir)
        
        datos_original = b"Este es un bloque de datos de prueba"
        exito, hash_bloque = manager.guardar_bloque(0, datos_original)
        
        assert exito
        assert hash_bloque is not None
        
        datos_leidos = manager.leer_bloque(0)
        assert datos_leidos == datos_original


def test_eliminar_bloque():
    """Test eliminar un bloque"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = StorageManager(tmpdir)
        
        manager.guardar_bloque(0, b"datos")
        assert manager.leer_bloque(0) is not None
        
        exito = manager.eliminar_bloque(0)
        assert exito
        assert manager.leer_bloque(0) is None


def test_obtener_bloques_locales():
    """Test obtener lista de bloques locales"""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = StorageManager(tmpdir)
        
        manager.guardar_bloque(0, b"bloque 0")
        manager.guardar_bloque(1, b"bloque 1")
        manager.guardar_bloque(2, b"bloque 2")
        
        bloques = manager.obtener_bloques_locales()
        assert len(bloques) == 3
        assert 0 in bloques
        assert 1 in bloques
        assert 2 in bloques


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
