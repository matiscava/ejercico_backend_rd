# Ejercico propuesto para dasarrollador Backend

Desarrollar un microservicio rest-api en python fast-api con conexión a una base de datos sqlite.

## Para correr el microservicion ingrese por consola la siguiente linea:

````
uvicorn main:app --reload
````


El mismo cuenta con 2 endpoints

### POST /input/{my_target_field}

Obtiene un json del body con la siguiente configuracion:

```
{ 
    "field_1": "somedata...",
    "author":"someauthordata...",
    "description":"evenmoredata...", 
    "my_numeric_field":123 
}
```

Crea un nuevo author en la base de datos, convirtiendo el valor del campo ingresado en my_target_field en mayuscula.

En caso de no ingresar ningún campo, un campo que no existe o el campo my_numeric_field, salta un error, ya que no se puede hacer que un número sea mayúscula o modificar un valor que no existe.


Al crear el author se devuelvo un json con el id del registro.


### GET /data/{id}

Realiza una consulta a la base de datos con el id ingresado por parametro.
Y devuelve la información ingresado. Por ejemplo:
```
{ 
    "field_1": "pedro",
    "author":"JORGE LUIS BORGES",
    "description":"autor literario", 
    "my_numeric_field": 45
}
```

En caso de que se ingrese un id que no está asignado, se devuelve un mensaje de error informando que no existe ese author. 


## Peticiones de prueba
### /docs
Para testear las peticiones ingrese a localhost:8000/docs donde se abrira una vista de Swagger con los endpoints definidos.