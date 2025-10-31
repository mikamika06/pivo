1. **Встановити залежності:**
    ```bash
    pip install Django==5.2.7 sqlparse==0.5.3
    ```

2. **У файлі silpo_monitor/settings.py виставити конфігурацію для SQLite:**
    ```python
    DATABASES = {
         "default": {
              "ENGINE": "django.db.backends.sqlite3",
              "NAME": BASE_DIR / "db.sqlite3",
         }
    }
    ```

3. **Виконати міграції та запустити демо:**
    ```bash
    python manage.py migrate
    python main.py
    ```

4. **Перевірка у Django shell:**
    ```bash
    python manage.py shell -c "from monitoring.repositories import repository_registry as repo; print(list(repo.products.get_all()))"
    ```

## Запуск з MongoDB

1. **Запустити MongoDB Server (7.0.x):**
    ```bash
    ~/mongodb/mongodb-macos-aarch64-7.0.25/bin/mongod \
         --dbpath ~/mongodb/data/db \
         --logpath ~/mongodb/logs/mongod.log \
         --fork
    ```
    Переконатися, що порт 27017 вільний:
    ```bash
    lsof -Pni :27017
    ```

2. **Встановити Python-пакети (сумісні з djongo):**
    ```bash
    pip install "django==3.1.12" "sqlparse==0.2.4" djongo==1.3.7 pymongo==3.11.4
    ```

3. **У файлі silpo_monitor/settings.py налаштувати DATABASES для djongo:**
    ```python
    DATABASES = {
         "default": {
              "ENGINE": "djongo",
              "NAME": "silpo_monitor",
              "ENFORCE_SCHEMA": False,
              "CLIENT": {
                    "host": "127.0.0.1",
                    "port": 27017,
                    "tz_aware": False,
              },
         }
    }
    ```

4. **За потреби очистити дані та виконати міграції:**
    ```bash
    rm -rf ~/mongodb/data/db/*
    ~/mongodb/mongodb-macos-aarch64-7.0.25/bin/mongod --dbpath ~/mongodb/data/db --logpath ~/mongodb/logs/mongod.log --fork
    python manage.py migrate
    ```

5. **Запустити демо-скрипт:**
    ```bash
    python main.py
    ```

6. **Перевірити дані:**
    ```bash
    python manage.py shell -c "from monitoring.repositories import repository_registry as repo; print(list(repo.products.get_all()))"
    ```
    Якщо встановлений mongosh, переглянути колекції напряму:
    ```bash
    mongosh "mongodb://127.0.0.1:27017/silpo_monitor" \
         --eval "db.monitoring_product.find({}, {name:1, sku:1, _id:0})"
    ```

7. **Зупинити MongoDB:**    ```bash    pkill mongod    ```## Корисні команди- Переглянути статус міграцій для додатку monitoring:  ```bash  python manage.py showmigrations monitoring  ```- Запустити оболонку бази даних (для SQLite):  ```bash  python manage.py dbshell  ```
- Переглянути вміст таблиці в SQLite:
  ```bash
  sqlite3 db.sqlite3 "SELECT name FROM monitoring_product;"
  ```
- Очистити таблиці (обережно):
  ```bash
  python manage.py flush
  ```
