# django_bootstrap

# Get Started
```
curl -i https://raw.githubusercontent.com/kellyxiepei/django_bootstrap/main/project_tools/django_bootstrap.sh -o django_bootstrap.sh

bash django_bootstrap.sh my_new_project
```

# After creating the project 
## 1 Install poetry
```
# Maybe you'd like to create a new virtual env before running this command
pip install poetry
```

## 2 Build project
```
poetry build
```

## 3 Configure local environment
### 3.1 start a mysql server and create a database
```
mysql> create database django_bootstrap charset=utf8;
```
### 3.2 start a redis server
```
#See the redis document or using docker:

docker run -d --name testredis -p 6379:6379 redis:3 --requirepass "123456"
```
### 3.3 update local configuration
```
vim .env
```

### 3.4 update local configuration
```
python manage.py migrate
```

### 3.5 start dev server
```
python manage.py runserver
```

## 4 Create new app
```
python manage.py newapp my-new-app
```
This command creates a new app with pre-defined code structure. Please take a look at the code, and modify it according to your demands. Don't forget to makemigrations and migrate.



## Authentication

### 4.1 Mobile Authentication
```
python manage.py enable_mobile_auth <app_name>
```
And then you will have these two api:
/api/<app_name>/mobile_auth/send_sms
/api/<app_name>/mobile_auth/login


### 4.2 Wechat Mini Authentication
```
python manage.py enable_wechat_mini_auth <app_name>
```
And then you will have this api:
/api/<app_name>/wechat_mini_auth/login

# TODO
## Create a command to deploy django app to alibaba cloud serverless platform.