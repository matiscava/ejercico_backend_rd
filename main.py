from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import databases
import sqlalchemy

app = FastAPI()

# URL base de datos
DATABASE_URL = "sqlite:///./test.db"

# Configuracion de base de datos
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
# Creamos la tabla authors
authors = sqlalchemy.Table(
  "authors",
  metadata,
  sqlalchemy.Column("ID", sqlalchemy.Integer, primary_key=True),
  sqlalchemy.Column("field_1",sqlalchemy.String),
  sqlalchemy.Column("author", sqlalchemy.String),
  sqlalchemy.Column("description", sqlalchemy.String),
  sqlalchemy.Column("my_numeric_field", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(
  DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

# Configuracion de seguridad
security = HTTPBasic()

class UserCredentials( BaseModel ):
  username: str
  password: str

# Función para verificar las credenciales de usuario
def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    # En este ejemplo, verifica las credenciales de usuario aquí.
    # Puedes reemplazar esta lógica con tu propia autenticación.
    if credentials.username == "admin" and credentials.password == "admin":
        return True
    return False



class AuthorDto(BaseModel):
  field_1: str
  author: str
  description: str
  my_numeric_field: int

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/data/{id}")
async def get_author(id: int, verified: bool = Depends(verify_user)):
  query = authors.select().filter(authors.c.ID == id)
  author_data = await database.fetch_one(query)

  if author_data is not None:
    author = AuthorDto(**author_data)
    return author
  else:
    return {"error": f"No existe el registro con el ID: {id}"}

@app.post("/input/{my_target_field}")
async def post_author(my_target_field: str, author: AuthorDto, verified: bool = Depends(verify_user)):
  if my_target_field == "my_numeric_field":
    return {"error": f"{my_target_field} no es un campo válido para convertir a mayúscula"}
  if hasattr(author, my_target_field):
    field_to_upper = getattr(author, my_target_field)
    setattr(author, my_target_field, field_to_upper.upper())

    query = authors.insert().values(
      field_1=author.field_1,
      author = author.author,
      description = author.description,
      my_numeric_field = author.my_numeric_field
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}
  else:
    return {"error": f"{my_target_field} no es un campo válido para convertir a mayúscula"}


