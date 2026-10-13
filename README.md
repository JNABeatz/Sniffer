# Funciones Sniffer — Captura y análisis de tramas TCP

## Descripción

Este proyecto contiene un conjunto de funciones en Python para capturar, filtrar y almacenar tramas de datos TCP intercambiadas entre un PC y un dispositivo conectado a la red.

Utiliza la biblioteca **Scapy** para capturar paquetes de red en tiempo real o leer capturas guardadas previamente en archivos `.pcap` o `.pcapng`.

El script permite identificar el sentido de la comunicación, descartar paquetes que no contienen datos útiles e ignorar determinadas tramas mediante prefijos específicos.

## Características principales

- **Captura de tráfico TCP:** captura paquetes intercambiados entre un PC y un dispositivo.
- **Filtrado por dirección IP:** selecciona el tráfico relacionado con la IP del dispositivo.
- **Filtrado por puerto:** permite especificar un puerto TCP para reducir el tráfico capturado.
- **Lectura de capturas existentes:** procesa archivos `.pcap` y `.pcapng`.
- **Filtrado de tramas:** permite ignorar tramas que comiencen con determinados prefijos.
- **Identificación del sentido de comunicación:** distingue entre `PC->Dispositivo` y `Dispositivo->PC`.
- **Conversión de hexadecimal a bytes:** limpia y convierte cadenas hexadecimales en datos binarios.
- **Almacenamiento de tramas:** guarda las tramas en un archivo de texto con su nombre y contenido hexadecimal.

## Requisitos

- Python 3.
- Scapy.
- Permisos adecuados para capturar paquetes de red, según el sistema operativo y el método de captura utilizado.

## Instalación

1. Clona el repositorio:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```

2. Accede al directorio del proyecto:

   ```bash
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

3. Instala la dependencia:

   ```bash
   pip install scapy
   ```

## Funciones disponibles

### 1. `limpiar_hex(texto)`

Convierte una cadena hexadecimal en un objeto `bytes`.

**Funcionamiento:**
- Convierte las letras a minúsculas.
- Elimina el prefijo `0x`.
- Elimina los caracteres que no sean dígitos hexadecimales.
- Convierte el resultado en bytes.

**Ejemplo:**

```python
from funciones_sniffer import limpiar_hex

trama = limpiar_hex("0xAA 0xBB 0x01")
print(trama)
```

Resultado:

```text
b'\xaa\xbb\x01'
```

> **Nota:** la función puede generar un error si, después de la limpieza, la cadena contiene un número impar de dígitos hexadecimales.

### 2. `guardar_trama(nombre, trama, archivo)`

Guarda una trama en un archivo de texto junto con el nombre que la identifica.

**Parámetros:**
- `nombre`: identificador de la trama.
- `trama`: contenido de la trama en bytes o una cadena hexadecimal.
- `archivo`: ruta del archivo donde se almacenará la información.

**Funcionamiento:**
- Convierte el contenido hexadecimal a bytes si recibe una cadena.
- Elimina los espacios al principio y al final del nombre.
- Sustituye los puntos y comas del nombre por guiones bajos.
- Añade la trama al final del archivo, sin sobrescribir las entradas anteriores.
- Muestra por consola la trama almacenada.

**Ejemplo:**

```python
from funciones_sniffer import guardar_trama

trama = bytes.fromhex("AA BB 01 02")
guardar_trama("Comando_01", trama, "tramas.txt")
```

El archivo `tramas.txt` contendrá:

```text
Comando_01;aa bb 01 02
```

Cada línea representa una trama y separa su nombre de los bytes mediante un punto y coma.

### 3. `capturar(ip_dispositivo, puerto=None, segundos=5, ignorar=(), archivo=None)`

Captura y filtra tramas TCP intercambiadas con un dispositivo, ya sea desde la red en tiempo real o desde un archivo de captura existente.

**Parámetros:**

| Parámetro | Descripción |
|---|---|
| `ip_dispositivo` | Dirección IP del dispositivo. |
| `puerto` | Puerto TCP del dispositivo. Es opcional. |
| `segundos` | Duración de la captura en vivo, en segundos. Por defecto, `5`. |
| `ignorar` | Iterable de prefijos en bytes para descartar determinadas tramas. Por defecto, está vacío. |
| `archivo` | Ruta de un archivo `.pcap` o `.pcapng`. Si se indica, se leen los paquetes del archivo en lugar de capturar tráfico en vivo. |

**Funcionamiento:**

1. Selecciona paquetes que contienen capas IP y TCP.
2. Filtra los paquetes relacionados con la dirección IP del dispositivo y, si se indica, con el puerto especificado.
3. Captura tráfico en vivo durante el tiempo establecido o lee una captura existente.
4. Descarta los paquetes TCP que no contienen datos de aplicación.
5. Ignora las tramas que comienzan con alguno de los prefijos indicados.
6. Identifica el sentido de la comunicación.
7. Devuelve una lista con el tiempo relativo, el sentido y los bytes de cada trama válida.

**Ejemplo de captura en vivo:**

```python
from funciones_sniffer import capturar

tramas = capturar(
    ip_dsp="192.168.1.100",
    puerto=5000,
    segundos=10
)

for tiempo, sentido, datos in tramas:
    print(tiempo, sentido, datos.hex(" "))
```

**Ejemplo de lectura de un archivo de captura:**

```python
from funciones_sniffer import capturar

tramas = capturar(
    ip_dsp="192.168.1.100",
    puerto=5000,
    archivo="captura.pcap"
)

for tiempo, sentido, datos in tramas:
    print(f"{tiempo:.6f}s | {sentido} | {datos.hex(' ')}")
```

**Ejemplo de filtrado de tramas:**

Para ignorar las tramas que comienzan con los bytes `AA BB`:

```python
tramas = capturar(
    ip_dsp="192.168.1.100",
    puerto=5000,
    segundos=10,
    ignorar=(bytes.fromhex("AA BB"),)
)
```

**Formato de retorno:**

La función devuelve una lista de tuplas con la siguiente estructura:

```python
(tiempo_en_segundos, sentido, bytes_de_la_trama)
```

Por ejemplo:

```python
[
    (0.0, "PC->Dispositivo", b"\xaa\xbb\x01"),
    (0.125, "Dispositivo->PC", b"\x10\x20\x30")
]
```

Los tiempos son relativos al primer paquete capturado o leído que cumple el filtro de paquetes. El sentido puede ser:

- `PC->Dispositivo`: paquete enviado desde el PC hacia el dispositivo.
- `Dispositivo->PC`: paquete enviado desde el dispositivo hacia el PC.

## Estructura del proyecto

```text
.
├── funciones_sniffer.py
├── README.md
└── tramas.txt          # Archivo de salida opcional
```

Los archivos de captura utilizados como entrada (`.pcap` o `.pcapng`) pueden ubicarse en cualquier ruta accesible desde el script.

## Consideraciones

- La captura en vivo requiere acceso a la interfaz de red y puede necesitar permisos elevados.
- La función `capturar()` trabaja con paquetes TCP que contienen capas IP y TCP.
- El filtrado por prefijos se aplica a los datos transportados por TCP, no a la trama Ethernet completa.
- El parámetro `segundos` solo controla la duración de la captura en vivo; al leer un archivo, se procesa la captura disponible.
- El archivo de salida de `guardar_trama()` se abre en modo de anexado, por lo que las entradas anteriores se conservan.
- `limpiar_hex()` elimina los caracteres que no son hexadecimales. Por tanto, está pensada para cadenas que representan datos hexadecimales, no para validar formatos arbitrarios.

## Uso responsable

Utiliza estas funciones únicamente en redes y dispositivos para los que tengas autorización. Las capturas pueden contener información sensible, por lo que deben almacenarse y compartirse de forma segura.
