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
        "token": "AQUÍ DEBE IR TU TOKEN",
        "prefix": "!",
        "guildid": 1234567890,
        "vulneratedroleid": 1234567890,
        "welcomeroleid": 1234567890,
        "vulneratedchannelid": 1234567890,
        "suggestionschannelid": 1234567890,
        "supportchannelid": 1234567890
    }
    ```

    | Clave                | Descripción                                          |
    | -------------------- | ---------------------------------------------------- |
    | token                | Reemplaza con el token de tu bot                     |
    | prefix               | Define el prefijo para los comandos normales del bot |
    | guildid              | ID del servidor donde se utilizará el bot            |
    | vulneratedroleid     | ID del rol asignado a las cuentas vulneradas         |
    | welcomeroleid        | ID del rol asignado a los miembros nuevos            |
    | vulneratedchannelid  | ID del canal visible para las cuentas vulneradas     |
    | suggestionschannelid | ID del canal donde se recibirán sugerencias          |
    | supportchannelid     | ID del canal de soporte para el servidor             |

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

**Una lista de cambios para la versión 0.3.0**

- [x] Utilizar un _dropdown_ para ver las páginas en el comando `help category general`
- [x] Implementar una nueva serie de comandos `jiudadeath` con nuevas funcionalidades
- [ ] Reemplazar algunas bases de datos JSON por una base de datos SQL usando aiosqlite

## Changelog

Puedes ver la lista de cambios en las versiones [aquí](CHANGELOG.md).