import re

def limpiar_hex(texto):
    """Convierte la trama en bytes y quita todo lo que no sea hexadecimal"""
    texto = texto.lower().replace("0x", "")
    texto = re.sub(r"[^0-9a-f]", "", texto)
    return bytes.fromhex(texto) #si hay un numero impar de dígitos falla


def guardar_trama(nombre, trama, archivo):
    """Recibe una trama y la guarda con su nombre"""
    if isinstance(trama, str):
        trama = limpiar_hex(trama)
    nombre = nombre.strip().replace(";", "_")
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(f"{nombre};{trama.hex(' ')}\n")
    print("Trama recibida: "+f"{nombre};{trama.hex(' ')}\n")
