# Проект Yatube #

## Как запустить проект ##

Клонировать репозиторий, перейти в него в командной строке.
Создать и активировать виртуальное окружение.

```
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости из файла requirements.txt
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции
```bash
python manage.py migrate
```
Запустить проект
```bash
python manage.py runserver
```


