Все команды запускаются в корневой папке проекта.
Запуск командой:
``docker-compose up``
После запуска сервис доступен по адресу:
``localhost:8000``
Создание учетки админа для доступа в админку:
``docker-compose run web python manage.py createsuperuser``
Запуск тестов:
``docker-compose run web python manage.py test``