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

3. **Crear el archivo de configuración:**

    En la carpeta `bot`, crea un archivo llamado `config.json` y copia el siguiente contenido del archivo `example.config.json`:

    ```json
    {
        "token": "AQUÍ_DEBE_IR_TÚ_TOKEN",
        "prefix": "!",
        "guildid": 1234567890,
        "vulneratedroleid": 1234567890,
        "welcomeroleid": 1234567890,
        "vulneratedchannelid": 1234567890
    }
    ```

    Reemplaza `AQUÍ_DEBE_IR_TÚ_TOKEN` con el token de tu bot, `guildid` con la ID del servidor, `vulneratedroleid` con la ID del rol para las cuentas vulneradas, `vulneratedchannelid` con la ID del canal que verán las personas con cuentas vulneradas y `welcomeroleid` con la ID del rol que tendrán los nuevos miembros que se unan al servidor.

## Uso

  - Active el entorno virtual:

    ```sh
    poetry shell
    ```

  - Para ejecutar el bot, utilice el siguiente comando:

    ```sh
    py bot/main.py
    ```

  - Para formatear el código utilizando las dependencias de desarrollo, utilice:

    ```sh
    poetry run format
    ```