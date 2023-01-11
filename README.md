# QuestionsAnswers

1- Crear bd en PgAdmin con nombre 'questionsanswers'
2- Verificar si tiene diferente usuario y contraseña en la conexion a bd: 'QuestionsAnswers/settings.py', si es el caso editarlo
2- Ejecutar python manage.py makemigrations
3- Ejecutar python manage.py migrate
4- Para usar autenticación ejecutar: 'python manage.py createsuperuser' y crear crear usuario
5- ingresar a: 'http://localhost:8000/admin/' loguearse con el usuario creado y agregar un grupo nombrar Admin al grupo   
6- Ejecutar python manage.py runserver

requerimientos
psycopg2==2.9.3