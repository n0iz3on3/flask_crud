# flask_crud

1. В директории проекта создать файл .env и заполнить его по образцу:

```python
PG_USER:app
PG_PASSWORD:1234
PG_DB:app
PG_HOST:127.0.0.1
PG_PORT:5431
TOKEN_TTL:86400
PASSWORD_LENGTH:12
```
Установить зависимости: 
```python
pip install -r requirements.txt
```
2. Запустить контейнер с базой данных:
```python
docker compose up -d
```
3. Запустить приложение выполнив последовательно:
```python
cd app
```
```python
python main.py
```
