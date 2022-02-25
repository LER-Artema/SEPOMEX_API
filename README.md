# SEPOMEX_API
SEPOMEX Data Responsive API

Esta aplicación está diseñada con la base de datos de SEPOMEX y el framework Flask, en el desarrolo local maneja una base de datos SQLite
y en el despliegue en Heroku una base de datos PostrgreSQL.

Cuenta con 4 Rutas para solicitar información por CP, Nombre de Colonia, Municipio o Estado y 1 ruta para añadir información a la base de datos.

Devuelve la información en formato JSON.

La base de datos cuenta con 4 tablas: API_KEYS, Colonia, Municipio, Estado, las tres últimas comparten el ID del estado al que pertenecen.

