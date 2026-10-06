import socket
import time

DSP_IP = "192.168.1.100"  
DSP_PORT = 1001         
PROTOCOLO = "TCP"

def crear_trama_ganancia(ganancia_db):
    """
    Calcula el byte de ganancia y construye la trama completa.
    0 dB = 88 (0x58), pasos de 0.1 dB = 1 entero.
    """
    # Ecuación: 88 + (Ganancia * 10)
    byte_ganancia = int(88 + (ganancia_db * 10))
    
    # Limitar a los márgenes de 1 byte por seguridad (0 - 255)
    byte_ganancia = max(0, min(255, byte_ganancia))
    
    # Crear el payload con el valor en el índice 7
    trama = bytearray([
        0xF0, 0x91, 0x01, 0x04, 0x01, 0x00, 0x02, 
        byte_ganancia, 
        0x00, 0x00, 0x00, 0x00, 0xF7
    ])
    
    return trama

def enviar_trama(trama, ip, puerto, protocolo):
    """Abre el socket, envía los bytes crudos y cierra la conexión."""
    if protocolo == "UDP":
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(trama, (ip, puerto))
            
    elif protocolo == "TCP":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0) # Evitar cuelgues si el puerto está cerrado
            s.connect((ip, puerto))
            s.send(trama)

if __name__ == "__main__":

    db = float(input("Ganancia : "))
    
    print(f"Destino: {DSP_IP}:{DSP_PORT} ({PROTOCOLO})\n")
    
    trama = crear_trama_ganancia(db)
        
    hex_trama = " ".join([f"{b:02X}" for b in trama])
    print(f"Ganancia: {db:2} dB | Trama generada: {hex_trama}")
        
    try:
        enviar_trama(trama, DSP_IP, DSP_PORT, PROTOCOLO)
        print(" -> Enviada correctamente")
    except Exception as e:
        print(f" -> Error al enviar: {e}")
        
    time.sleep(1)