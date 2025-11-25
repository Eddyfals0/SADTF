from sadtf_coordinador.coordinador.tabla_bloques import TablaBloques

def test_asignar_buscar():
    t = TablaBloques()
    t.asignar_bloque('b1', 'n1')
    assert t.buscar_bloque('b1') == 'n1'
