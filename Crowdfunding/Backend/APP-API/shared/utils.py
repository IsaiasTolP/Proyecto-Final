import uuid
import os

## Es necesario hacer una función por ruta, debido a que si lo hacemos como si fuera un decorador, tenemos algo funcional, pero que django es incapaz de crear las migraciones en la base de datos.
## It is necessary to make a function per route, because if we do it as if it were a decorator, we have something functional, but Django is unable to create the migrations in the database.

def unique_project_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('project_images/', filename)

def unique_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('profile_pics/', filename)