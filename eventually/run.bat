REM Batch file to make database changes and run server
manage.py makemigrations
manage.py migrate
manage.py runserver