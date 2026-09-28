# Sniffer de Tramas

Un conjunto de herramientas sencillo en Python para capturar tráfico de red,
etiquetar las tramas que grabas y compararlas byte a byte.

Está pensado para ayudarte a descubrir cómo está estructurado el protocolo de
un dispositivo sin documentar: cambias un ajuste en el dispositivo, capturas el
tráfico, guardas la trama con un nombre descriptivo y ves qué bytes cambian.

> 🚧 **En desarrollo:** este proyecto está en desarrollo activo.
> Algunas funciones aún no están implementadas y la API puede cambiar.

Por ahora solo está disponible el módulo de guardado de tramas. Para importarlo desde
tu propio script:
``python
from guardar_tramas import guardar_trama
`` 

## Formato del archivo de tramas

Las tramas se guardan en `tramas.txt`, una por línea:

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
herramientas que lean el archivo deben tratar la última como la vigente.

## Estructura del proyecto

Estructura prevista (los archivos con ✓ ya existen):

```
├── README.md
├── requirements.txt
├── config.py            # IP del equipo objetivo, ruta de tramas.txt
├── captura.py           # captura de paquetes con Scapy
├── guardar_tramas.py    # ✓ guardar tramas con nombre
├── cargar_tramas.py     # cargar y comparar tramas
├── main.py              # une las piezas
└── datos/               # capturas y tramas guardadas
```

Ejecuta todo desde la carpeta raíz del repositorio para que las rutas
relativas funcionen igual para todos.

## Hoja de ruta

- [x] Guardado de tramas
- [ ] Captura de paquetes
- [ ] Carga y comparación de tramas
- [ ] Interfaz de línea de comandos
- [ ] Detectar bytes fijos y variables a partir de muchas tramas

## Uso responsable

Analiza únicamente dispositivos y redes que sean tuyos o para los que tengas
permiso, y respeta las leyes y las condiciones de licencia que apliquen a tu
caso.
