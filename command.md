# add path for homebrew
export PATH="/opt/homebrew/bin:$PATH"

# creation django project
## BY python virtual environment

# create virtual environment
python -m venv venv

# activate and enters python virtual envrionment
source venv/bin/activate

## django pip installs
# install django
pip install django

# install django rest framework
pip install djangorestframework

# libraries
pip install markdown django-filter Pillow django-cors-headers django-environ

# update requirements.txt file libraries
pip freeze > requirements.txt

# Dango project

# create django project
django-admin startproject sbm-django


# docker
docker-compose --env-file .env up --build


# sonar-scanner add PATH (download sonar-scanner from Sonar official website)
export PATH="/Users/franciscomendoza/Documents/DEV/SBM-SUITE/SBM-API/sonar-scanner/bin:$PATH"

# scan project SBM-SUITE-API (cd test folder for coverage)
sonar-scanner \
  -Dsonar.projectKey=SBM-suite-API \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqp_305ecccfa26e27436b148cac77f3a9a3302f0540
  


# pytest / coverage 
pip install pytest-django
pip install pytest
pip install coverage 

# coverage code (cd project folder) (ex: coverage run tests/test_main.py)
coverage run "python test file" 

# coverage prompt report (cd test folder)
coverage report

# coverage export xml (cd test folder)
coverage xml

# sonar scanner properties
## set props
sonar.projectKey=SBM-suite-API
sonar.projectName=SBM-suite-API
sonar.projectVersion=1.0
sonar.projectBase=/Users/franciscomendoza/Documents/DEV/SBM-SUITE/SBM-API
sonar.sources=SBM-API
sonar.python.coverage.reportPaths=/Users/franciscomendoza/Documents/DEV/SBM-SUITE/SBM-API/core/tests/coverage.xml





# sonar-scanner DB add PATH (download sonar-scanner from Sonar official website)
export PATH="/Users/franciscomendoza/Documents/DEV/SBM-SUITE/SBM-API/mysql/sonar-scanner/bin:$PATH"

# scan project SBM-SUITE-API-DB (root folder)
sonar-scanner \
  -Dsonar.projectKey=SBM-suite-API-DB \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqp_6f5d5ea7fa107b156e15f4a19a80cbcb0d30273c




# Command to create superuser (run this if superuser doesn't exist):
docker-compose exec api python manage.py createsuperuser --username sbm-admin --email operacione@ditalypasta.cl --noinput
 
docker-compose exec api python manage.py shell -c "from django.contrib.auth.models import User; user = User.objects.get(username='sbm-admin'); user.set_password('sbm123'); user.save(); print('Contraseña establecida: sbm123')"