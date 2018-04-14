REM Batch file to make database changes and run server
manage.py makemigrations
manage.py migrate
start manage.py runserver
start email_system.py
start local.url