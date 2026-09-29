# Sniffer de Tramas

Un conjunto de herramientas sencillo en Python para capturar tráfico de red,
etiquetar las tramas que grabas y compararlas byte a byte.

Está pensado para ayudar a descubrir cómo está estructurado el protocolo de
un dispositivo sin documentar: se cambia un ajuste en el dispositivo, se captura el
tráfico, se guarda la trama con un nombre descriptivo y se ve qué bytes cambian.

> 🚧 **En desarrollo:** este proyecto está en desarrollo activo.
> Algunas funciones aún no están implementadas y la API puede cambiar.

## Características

- [x] Guardar tramas con un nombre en un archivo de texto
- [ ] Capturar paquetes desde y hacia un equipo concreto
- [ ] Cargar tramas guardadas y compararlas byte a byte

## Requisitos

- Python 3.8 o superior

Capturar paquetes suele requerir privilegios elevados: ejecuta la terminal como
administrador en Windows, o usa `sudo` en Linux / macOS.

## Uso

Todas las funciones viven en `funciones_sniffer.py`. Impórtalas desde tu propio script:

```python
from funciones_sniffer import guardar_trama

# Desde bytes (por ejemplo, el contenido de un paquete capturado con Scapy)
guardar_trama("ganancia_out1_0.1dB", bytes(p[Raw].load, "tramas.txt"))

# Desde un texto hexadecimal (por ejemplo, copiado de Wireshark)
guardar_trama("ganancia_out1_0.2dB", "55 aa 01 03 00 14 5c","tramas.txt")
```

El texto hexadecimal puede llevar espacios, dos puntos, guiones o el prefijo
`0x`: todo lo que no sea un dígito hexadecimal se elimina. Un número impar de
dígitos lanza un `ValueError`.

### Copiar tramas desde Wireshark

Selecciona solo los datos de aplicación (el campo **Data**) y usa
*Copy → …as a Hex Stream*. Los nombres exactos del menú pueden variar según la
versión.

Evita *Hex Dump* y *C Array*: su texto adicional (offsets, nombres de variable)
contiene caracteres que parecen dígitos hexadecimales y acabarían dentro de la
trama guardada. Evita también copiar el paquete entero, porque las cabeceras
Ethernet, IP y de transporte contienen valores (direcciones MAC, checksums,
contadores) que cambian entre capturas.

## Formato del archivo de tramas

Las tramas se guardan en un archivo, una por línea:

```
nombre;bytes en hexadecimal separados por espacios
```

Ejemplo (bytes inventados):

```
ganancia_out1_0.1dB;55 aa 01 03 00 0a 5c
ganancia_out1_0.2dB;55 aa 01 03 00 14 5c
```

Los puntos y coma de los nombres se sustituyen por guiones bajos al guardar,
porque `;` es el separador. Si dos líneas tienen el mismo nombre, las
funciones que lean el archivo deben tratar la última como la vigente.

## Estructura del proyecto

```
├── README.md
├── requirements.txt
├── funciones_sniffer.py     # capturar, guardar, cargar y comparar tramas
└── datos/        # capturas y tramas guardadas
```

Todo el código vive en un único archivo por sencillez, ya que el proyecto es
pequeño y las funciones están relacionadas entre sí. Ejecuta los scripts desde
la carpeta raíz del repositorio para que las rutas relativas funcionen igual
para todos.

## Hoja de ruta

- [x] Guardado de tramas
- [ ] Captura de paquetes
- [ ] Carga y comparación de tramas
- [ ] Interfaz de línea de comandos
- [ ] Detectar bytes fijos y variables a partir de muchas tramas

## Uso responsable

Analiza únicamente dispositivos y redes que sean tuyos o para los que tengas
permiso, y respeta las leyes y las condiciones de licencia que apliquen a tu
caso. No subas a este repositorio manuales, firmware o software propietario de
fabricantes.
