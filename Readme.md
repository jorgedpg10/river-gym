
# Poner en Producción en una red local
Instalar git, y clonar el repositorio

crear venv


hacer que la powershell nos deje activar el venv
(normamelte por defecto impide ejecutar scripts)


ejecutar pip install

	pip install -r requirements.txt

definir el estado de produccion en manage.py 

	os.environ.setdefault('DJANGO_SETTINGS_MODULE','funcional_project.settings.prod')

## Instalar PostgreSQL

ir a la web,

descargar instalador ejecutar con permisos de Administrador

poner en el path

levantar server de forma manual si windows no lo permite

postgres -D "C:\Program Files\PostgreSQL\15\data"

crear base 

## Poner secret
	python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Poner la cadena de 50 caracteres, en el `SECRET_KET` de los settings


## Poner tailwind como de produccion

instalar node y npm

moverme a la ubicacion del package.json ( theme/static_src ) y hacer `npm install`

finalmente

	python manage.py tailwind build

Para crear un css optimizado para produccion

# Testing

Las pruenbas han sido escritos usando el Django TestCase. Para ejecutar las pruebas, debemos correr:

	python manage.py test 

y así podemos ir filtrando, si queremos solo los tests dentro de un app:

	python manage.py test <nombre_app>.tests
	ej: 
	python manage.py test client.tests


si queremos solo, ejecutar los tests de una sola clase podemos añadir:

	python manage.py test <nombre_app>.tests.<nombre_de_la_clase>
	ej: 
	python manage.py test client.tests.UpdateClientViewTest

finalmente si queremos ejecutar una única prueba:

	python manage.py test <nombre_app>.tests.<nombre_de_la_clase>.<nombre_de_la_prueba>
	ej: 
	python manage.py test client.tests.UpdateClientViewTest.test_update_client_post_invalid_data
	


