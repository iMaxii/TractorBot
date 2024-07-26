# TractorBot

TractorBot es un bot de Discord que hace un poco de todo escrito en discord.py diseñado para una micro-comunidad. Proporciona varias características y utilidades para mejorar la experiencia de la comunidad.

## Requerimientos

- [Python](https://www.python.org/downloads/) 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)

## Instalación

1. **Clone el repositorio:**

    ```sh
    git clone https://github.com/iMaxii/TractorBot.git
    cd TractorBot
    ```

2. **Instale las dependencias:**

    - Sin las dependencias de desarrollo:

        ```sh
        poetry install --without dev
        ```

    - Con las dependencias de desarrollo (incluye herramientas para formatear el código):

        ```sh
        poetry install
        ```

## Uso

  - Para ejecutar el bot, utilice el siguiente comando:

    ```sh
    py bot/main.py
    ```

  - Para formatear el código utilizando las dependencias de desarrollo, utilice:

    ```sh
    poetry run format
    ```