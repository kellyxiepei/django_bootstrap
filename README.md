# django_bootstrap

# Get Started
```
curl -i https://raw.githubusercontent.com/kellyxiepei/django_bootstrap/main/project_tools/create_new_project.sh -o create_new_project.sh

bash create_new_project.sh my_new_project
```

# After creating the project 
## 1 Install poetry
```
# Maybe you'd like to create a new virtual env before running this command
pip install poetry
```

## 2 Build project
```
poetry install
poetry build
```

## 3 Configure local environment
### 3.1 start a mysql server and create a database
```
docker run -d --name django_bootstrap-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:8
docker exec -it django_bootstrap-db bash
mysql -u root -p123456
mysql> create database django_bootstrap charset=utf8;
```
### 3.2 start a redis server
```
#See the redis document or using docker:

docker run -d --name django_bootstrap-redis -p 6379:6379 redis:3 --requirepass "123456"
```
### 3.3 update local configuration
```
cp .env.example .env 
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
python manage.py makemigrations
python manage.py migrate
```
This command creates a new app with pre-defined code structure. Please take a look at the code, and modify it according to your demands. Don't forget to makemigrations and migrate.



## 5 Authentication

### 5.1 Mobile Authentication
```
python manage.py enable_mobile_auth <app_name>
```
And then you will have these two api:
/api/<app_name>/mobile_auth/send_sms
/api/<app_name>/mobile_auth/login

And you need implement MobileUserStoreBase and replace MobileUserStoreDemo.

### 5.2 Wechat Mini Authentication
```
python manage.py enable_wechat_mini_auth <app_name>
```
And then you will have this api:
/api/<app_name>/wechat_mini_auth/login

And you need implement UnionIdUserStoreBase and replace MobileUserStoreDemo.

### 5.3 Username & Password Authentication
```
python manage.py enable_wechat_mini_auth <app_name>
```
And then you will have this api:
/api/<app_name>/username_password_auth/login

And you need implement UsernameUserStoreBase and replace UsernameUserStoreDemo.

## 6 Deploy to Alibaba cloud function computing.


# TODO
## Create a command to deploy django app to alibaba cloud serverless platform.