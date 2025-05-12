# El backend constará de una API en django
Versión de python 3.13.1

## Diseño de la Base de datos relacional

## Aplicaciones

## Modelos

## Uso de librerías


# IMPORTANTE: Para desarrollo en Windows crear un fichero en main llamado windows_worker.py con el contenido siguiente:

```python
from rq import Worker


class BaseDeathPenalty(object):
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        pass


class SimpleWorker(Worker):
    death_penalty_class = BaseDeathPenalty

    def main_work_horse(self, *args, **kwargs):
        raise NotImplementedError("Test worker does not implement this method")

    def execute_job(self, *args, **kwargs):
        """Execute job in same thread/process, do not fork()"""
        return self.perform_job(*args, **kwargs)
```

## Luego descomentar la configuración de RQ en las settings

# Importante para Windows: Es necesario tener unos contenedores de Docker con Django, Redis, Base de datos PostgreSQL, para funcionar en desarrollo.
