# django_bootstrap

# 1.Install poetry
```
pip install poetry
```

# 2.Build project
```
poetry build
```

# 3.Configure local environment
## 3.1 create database
```
create database django_bootstrap charset=utf8;
```
## 3.2 update local configuration
```
vim .env
```

## 3.3 update local configuration
```
python manage.py migrate
```

## 3.4 start dev server
```
python manage.py runserver
```

