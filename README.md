# TractorBot

TractorBot es un bot de Discord que hace un poco de todo, el cual está escrito en discord.py. Está diseñado para una micro-comunidad. Proporciona varias características y utilidades para mejorar la experiencia de la comunidad.

<details>
  <summary>Tabla de Contenidos</summary>
    <ol>
      <li>
        <a href="#primeros-pasos">Primeros Pasos</a>
        <ul>
          <li><a href="#requerimientos">Requerimientos</a></li>
          <li><a href="#instalacion">Instalación</a></li>
        </ul>
      </li>
      <li><a href="#uso">Uso</a></li>
      <li><a href="#roadmap">Roadmap</a></li>
      <li><a href="#changelog">Changelog</a></li>
    </ol>
</details>

## Primeros Pasos

### Requerimientos

- [Python](https://www.python.org/downloads/) 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)

### Instalación

1. **Clonar el repositorio:**

    ```sh
    git clone https://github.com/iMaxii/TractorBot.git
    cd TractorBot
    ```

2. **Instalar las dependencias:**

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

    > Reemplaza `AQUÍ_DEBE_IR_TÚ_TOKEN` con el token de tu bot, `guildid` con la ID del servidor, `vulneratedroleid` con la ID del rol para las cuentas vulneradas, `vulneratedchannelid` con la ID del canal que verán las personas con cuentas vulneradas y `welcomeroleid` con la ID del rol que tendrán los nuevos miembros que se unan al servidor.

## Uso

  - Activa el entorno virtual:

    ```sh
    poetry shell
    ```

  - Para ejecutar el bot, usa el siguiente comando:

    ```sh
    py bot/main.py
    ```

  - Para formatear el código utilizando las dependencias de desarrollo, utiliza:

    ```sh
    poetry run format
    ```

## Roadmap

**Una lista de cambios para la versión 0.1.1**

- [x] Añadir un README y un CHANGELOG
- [x] Añadir **Poetry** para manejar dependencias y paquetes
- [x] Detectar y cargar automáticamente todos los _cogs_ existentes
- [x] Reorganizar los _cogs_ en diferentes archivos y subcarpetas
- [x] Añadir el comando `coglist` para que liste todos los _cogs_ existentes
- [x] Convertir los comandos normales a `hybrid_commands`
- [ ] Implementar `aiosqlite` para el manejo de bases de datos
- [ ] Mejorar el mensaje del comando `help`

## Changelog

Puedes ver la lista de cambios en las versiones [aquí](CHANGELOG.md).