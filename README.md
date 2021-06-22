# django_bootstrap

# Get Started
```
curl -i https://raw.githubusercontent.com/kellyxiepei/django_bootstrap/main/project_tools/django_bootstrap.sh -o django_bootstrap.sh

bash django_bootstrap.sh my_new_project
```

# After creating the project 
## 1 Install poetry
```
# Maybe you'd like to create new virtual env before running this command
pip install poetry
```

## 2 Build project
```
poetry build
```

## 3 Configure local environment
### 3.1 create database
```
mysql> create database django_bootstrap charset=utf8;
```
### 3.2 update local configuration
```
vim .env
```

### 3.3 update local configuration
```
python manage.py migrate
```

### 3.4 start dev server
```
python manage.py runserver
```

## 4 Create new app
```
python manage.py newapp my-new-app
```
This command creates a new app with pre-defined code structure. Please take a look at the code, and modify it according to your demands. Don't forget to makemigrations and migrate.


# TODO
## Create a command to deploy django app to alibaba cloud serverless platform.