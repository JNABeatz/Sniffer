"""
Guarda una trama recibida en un archivo de texto.

Formato de archivo:
    - Una línea por trama
    - 'nombre;bytes_en_hexadecimal'

Uso desde otro script:
    from guardar_tramas import guardar_trama
    guardar_trama("ganancia_out1_0.1dB", bytes(p[Raw].load))
"""

import re

ARCHIVO = "tramas.txt"

def limpiar_hex(texto):
    """Convierte la trama en bytes y quita todo lo que no sea hexadecimal"""
    texto = texto.lower().replace("0x", "")
    texto = re.sub(r"[^0-9a-f]", "", texto)
    return bytes.fromhex(texto) #si hay un numero impar de dígitos falla


def guardar_trama(nombre, trama):
    """Recibe una trama y la guarda con su nombre"""
    if isinstance(trama, str):
        trama = limpiar_hex(trama)
    nombre = nombre.strip().replace(";", "_")
    with open(ARCHIVO, "a", encoding="utf-8") as f:
        f.write(f"{nombre};{trama.hex(' ')}\n")
    print("Trama recibida: "+f"{nombre};{trama.hex(' ')}\n")
