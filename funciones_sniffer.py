import re
from scapy.all import sniff,IP,TCP

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


def capturar(ip, puerto=None, segundos=5, ignorar=(), archivo=None):
    """
    Captura tramas TCP entre el PC y el dispositivo.
 
    ip  : IP del dispositivo a capturar(se captura el tráfico hacia y desde esta IP)
    puerto   : puerto TCP del dsipositivo (opcional, descarta el resto de tráfico)
    segundos : duración de la captura en vivo
    ignorar  : lista de prefijos (bytes) de tramas que no interesan,
               por ejemplo el sondeo periódico
    archivo  : si se indica un .pcap/.pcapng, lee de ahí en vez de la red
 
    Devuelve una lista de tuplas: (tiempo_en_segundos, sentido, bytes_de_la_trama)
    donde sentido es "PC->dispositivo" o "dispositivo->PC".
    """
 
    def es_valido(p):
        # Solo paquetes TCP con la IP (y el puerto) del dispositivo
        if not (p.haslayer(IP) and p.haslayer(TCP)):
            return False
        if ip not in (p[IP].src, p[IP].dst):
            return False
        if puerto and puerto not in (p[TCP].sport, p[TCP].dport):
            return False
        return True
 
    if archivo:
        paquetes = sniff(offline=archivo, lfilter=es_valido)
    else:
        filtro = f"tcp and host {ip}"
        if puerto:
            filtro += f" and port {puerto}"
        paquetes = sniff(filter=filtro, lfilter=es_valido, timeout=segundos)
 
    resultado = []
    t0 = float(paquetes[0].time) if paquetes else 0
 
    for p in paquetes:
        datos = bytes(p[TCP].payload)
 
        if not datos:                              # ACKs sin datos
            continue
        if any(datos.startswith(pref) for pref in ignorar):
            continue
 
        sentido = "PC->DSP" if p[IP].dst == ip else "DSP->PC"
        resultado.append((float(p.time) - t0, sentido, datos))
 
    return resultado