from sadtf_coordinador.coordinador.tabla_nodos import TablaNodos

def test_register_heartbeat():
    t = TablaNodos()
    t.register('n1', {'capacidad': 1024})
    assert 'n1' in t.nodos
