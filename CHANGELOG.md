# Changelog

## v0.2.0

### Añadido
- Creado un entorno virtual con Poetry y añadido un script para formatear el código.
- Detectar y cargar automáticamente todos los cogs existentes independientemente de su subdirectorio.
- Añadido un comando para listar todos los cogs existentes.
- Añadido un README con una guía de instalación.
- Añadido un CHANGELOG.
- Creado un constructor de paginación para un código más compacto y fácil de usar.
- Añadidos algunos datos necesarios a `config.json`.

### Cambiado
- Reorganizados los cogs en nuevos archivos y subdirectorios.
- Convertidos los comandos normales a hybrid commands.
- Mejorado y compactado el código de los comandos `help` y `tag`.
- Mejorados los mensajes de ayuda.
- Actualizado el mensaje de error estándar.

### Corregido
- Asegurado que no se cree un `paginated_embed` si no hay más de una página.
- Hecho que los comandos `tag` sean insensibles a mayúsculas y minúsculas al buscar la etiqueta correspondiente.
- Varios correcciones de errores y cambios menores.

### Eliminado
- Eliminado un evento innecesario de `core.events`.
- Eliminado un condicional innecesario del comando `gayrate`.
- Eliminadas dependencias innecesarias.

## v0.1.0

### El proyecto ha sido publicado en GitHub ;)