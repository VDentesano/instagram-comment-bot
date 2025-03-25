# Instagram Comment Bot 🤖

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Advertencia**: Este proyecto es estrictamente para fines educativos. El uso de bots en Instagram viola sus [Términos de Servicio](https://help.instagram.com/581066165581870). El autor no se hace responsable del mal uso de este software.

## Índice

- [Descripción](#descripción)
- [Características Principales](#características-principales)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Configuración Avanzada](#configuración-avanzada)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Descripción

El **Instagram Comment Bot** es un script en Python que automatiza el proceso de comentar en publicaciones de Instagram. Utilizando Selenium y técnicas avanzadas de simulación de comportamiento humano, el bot reproduce acciones como desplazamientos, clics y movimientos del ratón para disminuir la probabilidad de detección. Además, cuenta con mecanismos de manejo de límites de tasa y rotación de *User-Agents*, haciendo el proceso de automatización más dinámico y realista.

## Características Principales

- **Simulación de Comportamiento Humano**:  
  Emula interacciones naturales, como scroll vertical/horizontal, movimientos aleatorios y hover sobre elementos (enlaces, imágenes y botones).

- **Gestión Inteligente de Delays**:  
  Utiliza una distribución log-normal para generar retardos variables entre acciones, imitando patrones humanos.

- **Rotación de User-Agents**:  
  Alterna entre agentes de usuario móviles y de escritorio para evitar patrones fijos de solicitudes.

- **Persistencia de Sesión con Perfiles de Chrome**:  
  Guarda la sesión en un perfil personalizado de Chrome para mantener autenticaciones y cookies.

- **Manejo de Límites de Tasa (Rate Limits)**:  
  Detecta respuestas con código 429 y realiza pausas automáticas, reintentando la acción tras un intervalo determinado.

- **Actualización Dinámica de Headers**:  
  Genera encabezados dinámicos (incluyendo tokens CSRF y referers) para cada petición, lo que ayuda a simular solicitudes genuinas.

## Requisitos

- **Python 3.8 o superior**  
- **Google Chrome (versión 100 o superior)**
- Cuenta de Instagram activa *(las credenciales no se incluyen, se requiere autenticación manual)*

## Instalación

1. **Clonar el repositorio**:
```bash
   git clone https://github.com/vdentesano/instagram-comment-bot.git
   cd instagram-comment-bot
```

2. **Instalar dependencias**:
```bash
  pip install -r requirements.txt
```

3. **Ejecutar el script**:
```bash
  python ig_comment_bot.py
```

## Uso

1. **Autenticación**:
  Al iniciar el bot, se abrirá una ventana de Chrome. Accede a Instagram y realiza la autenticación manual si es necesario.
  El script esperará hasta que se detecte que la sesión está activa (verifica la presencia del ícono del buzón de mensajes).

1. **Entrada de Datos**:
  Una vez autenticado, se solicitará:
  - La URL de la publicación a comentar.
  - Un mensaje base para los comentarios.
  - El número de comentarios a publicar.

1. **Proceso de Comentarios**:
  El bot cargará la publicación, extraerá el ID correspondiente y comenzará a publicar comentarios de forma escalonada. Durante el proceso, simula interacciones humanas y maneja cualquier error o límite impuesto por Instagram.

## Configuración Avanzada

- **Parámetros de Delay**:
  Dentro de la clase HumanizedDelay se puede ajustar el multiplicador y los parámetros de la distribución log-normal para modificar el tiempo entre acciones.

- **Rotación de User-Agents**:
  Las listas MOBILE_AGENTS y DESKTOP_AGENTS contienen diversos User-Agents. Puedes añadir o modificar estos valores según tus necesidades.

- **Persistencia de Perfil**:
  El script utiliza un directorio específico para almacenar el perfil de Chrome y mantener la sesión. Puedes cambiar la ruta modificando la variable profile_path en el método setup_driver().

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto o corregir algún error, por favor crea un *fork* del repositorio y envía un *pull request*. También puedes abrir un issue para discutir ideas o reportar problemas.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT.
