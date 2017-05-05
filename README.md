# COMP3297-Fume-Community-Platform

Final Project for the course COMP3297: Introduction to Software Engineering

Release 1

Deatech 5/1/2017

## Deployment
### Pre-conditions and assumptions
 - Windows is strongly recommended, even though the FCP should be able to run on any OS supported by Python.
 - Make sure Python 3.6 and pip are installed and "python" command runs Python 3.6. If "python" runs another version on your machine, replace the "python" in commands below accordingly. 
 - The following commands are assumed to be executed with superuser power. On Windows, run cmd as Administrator. On Linux, add "sudo" at the front for the following commands.
 - The requirements of module versions must be strictly followed or the FCP may not work properly.

### Installation of modules
 1. Install Django version 1.10.6 by `pip install "Django==1.10.6"`
 2. Install Pillow version 4.0.0 by `pip install "Pillow==4.0.0"`
 3. Install django-crispy-forms version 1.6.1 by `pip install "django-crispy-forms==1.6.1"`
 4. Install social-auth-app-django version 1.1.0 by `pip install "social-auth-app-django==1.1.0"`
 5. Install python-social-auth version 0.2.21 by `pip install "python-social-auth==0.2.21"`

### Running the server
 1. Direct to the project directory "vapoursite"
 2. Run it by `python manage.py runserver`
 3. Open the browser (Google Chrome recommended) and visit `127.0.0.1:8000`. Don't fancy the URL using something like "localhost". The social authentication won't work in that way.

## Initial accounts
The superuser has access to /admin/ where he can edit the database at will. The staff account manage the featured games at the drop-down menu beside its avatar.
### Superuser
 - Username: admin
 - Password: deatech123

### Staff
 - Username: staff
 - Password: deatech123
